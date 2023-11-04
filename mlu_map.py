import svgwrite
from math import pi, sqrt, sin, cos
from cmath import exp
import yaml
import itertools
from io import StringIO,BytesIO
import base64
import pathlib

camera_angle = pi/4  # camera angle from zenith
spacing = 40  # width of one hex


def append_class(elem, *classes):
    """Append new classes to an SVG element"""
    allclasses = itertools.chain(elem.attribs.get("class","").split(" "),classes)
    allclasses = list(dict.fromkeys(allclasses)) # remove duplicates
    elem.attribs["class"] = " ".join(allclasses)
    return elem

def hexagon(center, apothem=spacing/2*1.02, height=0, **attrs):
    "Create SVG group representing a hexagon"
    # points of the base hexagon
    pts = [
        (-1,1),  # bottom left
        (0, 2),  # bottom
        (1, 1),
        (1, -1),
        (0, -2),
        (-1,-1),
    ]
    pts = [[x*apothem+center[0], y*apothem*cos(camera_angle)/sqrt(3) + center[1]] for x,y in pts]
    
    doc = svgwrite.container.Group()
    if height <= 0:
        doc.add(
            append_class(svgwrite.shapes.Polygon(pts, **attrs), "tile", "tile-top")
        )
    else:
        height_proj = height*sin(camera_angle)
        top = [[x,y-height_proj] for x,y in pts]
        doc.add(
            append_class(svgwrite.shapes.Polygon(top, **attrs), "tile", "tile-top")
        )
        doc.add(
            append_class(svgwrite.shapes.Polygon(top[:2]+[pts[1],pts[0]], **attrs), "tile", "tile-left")
        )
        doc.add(
            append_class(svgwrite.shapes.Polygon(top[1:3]+[pts[2],pts[1]], **attrs), "tile", "tile-right")
        )
    return doc
  
def pentagon(center, side=spacing/sqrt(3), height=0, rotation=1, **attrs):
    """Create SVG group representing a pentagon
    Args:
    - side: side length
    - rotation: [0-5] orientation of the pentagon, with 0 to the east, 1 to the NE, etc.
    """
    # pentagon center, assuming touching east
    x0 = (sqrt(3)/2-1/2/sqrt(5-sqrt(20)))*side
    circumradius = sqrt((5+sqrt(5))/10)*side
    #import pdb; pdb.set_trace()
    pts = [(x0 + circumradius*cos(2*pi*(2*i+1)/10),
            circumradius*sin(2*pi*(2*i+1)/10))
           for i in range(5)]
    c = cos(-pi*rotation/3)
    s = sin(-pi*rotation/3)
    pts = [(x*c-y*s, y*c + x*s) for x,y in pts]
    pts = [(center[0]+x,center[1]+y*cos(camera_angle)) for x,y in pts]
    
    #pts = [[x*side+center[0], y*side*cos(camera_angle)/sqrt(3) + center[1]] for x,y in pts]
    
    doc = svgwrite.container.Group()
    if height <= 0:
        doc.add(
            append_class(svgwrite.shapes.Polygon(pts, **attrs), "tile", "tile-top")
        )
    else:
        left = 5*rotation//6
        right = int(5*rotation/6+7/5)
        height_proj = height*sin(camera_angle)
        top = [[x,y-height_proj] for x,y in pts]
        doc.add(
            append_class(svgwrite.shapes.Polygon(top, **attrs), "tile", "tile-top")
        )
        doc.add(
            append_class(
                svgwrite.shapes.Polygon(
                    [top[left%5],top[(left+1)%5],pts[(left+1)%5],pts[left%5]],
                    **attrs),
                "tile", "tile-left"
            )
        )
        if 1 == rotation%6:
            doc.add(
                append_class(
                    svgwrite.shapes.Polygon(
                        [top[1],top[2],pts[2],pts[1]],
                        **attrs),
                    "tile",
                    "tile-right",  # slightly right-facing
                    "tile-mid"
                )
            )
        elif 2 == rotation%6:
            doc.add(
                append_class(
                    svgwrite.shapes.Polygon(
                        [top[2],top[3],pts[3],pts[2]],
                        **attrs),
                    "tile", "tile-left", "tile-mid"
                )
            )
        doc.add(
            append_class(svgwrite.shapes.Polygon(
                [top[right%5],top[(right+1)%5],pts[(right+1)%5],pts[right%5]], **attrs), "tile", "tile-right")
        )
    return doc
  
def embed_image(filename):
    """Converts a file to base64"""
    out = BytesIO()
    with open(pathlib.Path(filename).expanduser(),'rb') as f:
        base64.encode(f,out)
    data = out.getvalue().decode().replace('\n','')
    return f"data:image/png;base64,{data}"

def line_to_bb(pt, normal, xmin, ymin, xmax, ymax):
    "Line segment going through pt perpendicular to normal and cropped to the bounding box"
    x0, y0 = pt
    nx, ny = normal
    if ny == 0:  # vertical
        if nx == 0:
            raise ValueError("Invalid normal")
        if xmin <= x0 <= xmax:
            return (x0, ymin), (x0, ymax)
        return None
    elif nx == 0:  #horizontal
        if ymin <= y0 <= ymax:
            return (xmin, y0), (xmax, y0)
        return None
    else:
        crossings = [
            (xmin, y0-(xmin-x0)*nx/ny),
            (xmax, y0-(xmax-x0)*nx/ny),
            (x0-(ymin-y0)*ny/nx, ymin),
            (x0-(ymax-y0)*ny/nx, ymax)
        ]
        crossings = {(x,y) for (x,y) in crossings if xmin <= x <= xmax and ymin <= y <= ymax}
        if len(crossings) == 2:
            return tuple(crossings)
        return None
assert line_to_bb((0,0),(1,1),-100,-100,100,100) is not None

def make_axes(xmin, ymin, xmax, ymax, **attribs):
    "Show origin with simple axes"
    
    attribs = dict(stroke="#eee").update(attribs)
    
    slope = sqrt(3)*cos(camera_angle)

    axes = svgwrite.container.Group(id_="axes")
    endpoints = line_to_bb((0,0), (0, 1), xmin, ymin, xmax, ymax)
    if endpoints:
        axes.add(svgwrite.shapes.Line(*endpoints, **attribs))

    endpoints = line_to_bb((0,0), (slope,-1), xmin, ymin, xmax, ymax)
    if endpoints:
        axes.add(svgwrite.shapes.Line(*endpoints, **attribs))

    return axes

def make_grid(spacing, xmin, ymin, xmax, ymax, origin=[0,0], major=1, minor=0, **line_attrs):
    "Triangular grid"
    attribs = dict(stroke="#eee")
    attribs.update(line_attrs)
    
    x0 = (origin[0]-origin[1]/2)*spacing
    y0 = -(origin[1]*sqrt(3)/2)*spacing*cos(camera_angle)
    
    slope = sqrt(3)*cos(camera_angle)
    

    grid = svgwrite.container.Group(id_="grid")
    
    yspacing = spacing*sqrt(3)/2*cos(camera_angle)
    for y in itertools.chain(
        range(1, int(ymax//yspacing)+1),
        range(0, int(ymin//yspacing)-2, -1)):
        endpoints = line_to_bb((x0,y0 + y*yspacing), (0, 1), xmin, ymin, xmax, ymax)
        if endpoints:
            class_ = "grid-major" if y%major == 0 else "grid-minor"
            grid.add(svgwrite.shapes.Line(*endpoints, class_=class_, **attribs))

    #import pdb; pdb.set_trace()
    extension = max((ymax - y0)/slope, (y0-ymin)/slope)

    for x in itertools.chain(
        range(1, int((xmax+extension)//spacing)+1),
        range(0, int((xmin-extension)//spacing)-1, -1)):
        class_ = "grid-major" if x%major == 0 else "grid-minor"

        endpoints = line_to_bb((x0+x*spacing,y0), (slope,-1), xmin, ymin, xmax, ymax)
        if endpoints:
            grid.add(svgwrite.shapes.Line(*endpoints, class_=class_, **attribs))
        endpoints = line_to_bb((x0+x*spacing,y0), (slope,1), xmin, ymin, xmax, ymax)
        if endpoints:
            grid.add(svgwrite.shapes.Line(*endpoints, class_=class_, **attribs))
    
#     endpoints = line_to_bb((x0,y0), (slope,1), xmin, ymin, xmax, ymax)
#     if endpoints:
#         grid.add(svgwrite.shapes.Line(*endpoints, **attribs))
    
    return grid

def svg_identifier(cleartext):
    return cleartext.lower().encode('ascii',errors='ignore').decode().strip().replace(" ","-")

def make_level(config, level_name):
    level = [l for l in config["levels"] if l["name"] == level_name][0]
    level_id = f"l-{svg_identifier(level_name)}"

    
    svg = svgwrite.Drawing(
        filename="test.svg",
        # size=("400px", "300px"), #("297mm", "210mm"),
        viewBox="-100 -100 200 200",
        #style="background:white",
        id_=level_id
    )
    
    if "styles" in config:
      svg.add(svg.style(config["styles"]))



    level_defaults = {"stroke":"black"}
    if "defaults" in level:
      level_defaults.update(level["defaults"])
    
    bounds = [0,0,0,0]  # xmin, ymin, xmax, ymax
        
    tiles = {}
    images = {}
    for region in level["regions"]:
        region_defaults = dict(level_defaults)
        if "defaults" in region:
          region_defaults.update(region["defaults"])
        region_id = f"r-{svg_identifier(region['name'])}"
        for tile in region["tiles"]:            
            attrs = dict(region_defaults)
            attrs.update(tile)
            x,y = attrs.pop("coord")
            icons = attrs.pop("resources",[])
            type_ = attrs.pop("type",None)
            decor = attrs.pop("decor",[])
            sides = attrs.pop("sides",6)
            rotation = attrs.pop("rotation",0)
            tile_id = f"tile-{x}-{y}"
            #attrs["class"] = f"tile t-{region['name']}"

            center = ((x - y/2)*spacing, (-y)*sqrt(3)/2*spacing*cos(camera_angle))
            
            #print(f"hex {x,y} at {center}")
            
            bounds[0] = min(bounds[0], center[0]-spacing)
            bounds[1] = min(bounds[1], center[1]-spacing-attrs.get("height",0)*sin(camera_angle))
            bounds[2] = max(bounds[2], center[0]+spacing)
            bounds[3] = max(bounds[3], center[1]+spacing)
            
            
            group = svg.g(id_=tile_id)
            sort_key = (-y,attrs.get("height",0), x)
            tiles[sort_key] = group
            if sides == 5:
              geom = pentagon(center, class_=f'tile {region_id} {"t-"+svg_identifier(type_) if type_ else ""}'.strip(), rotation=rotation, **attrs)
            else:
              geom = hexagon(center, class_=f'tile {region_id} {"t-"+svg_identifier(type_) if type_ else ""}'.strip(), **attrs)
            group.add(geom)
            for i, resource in enumerate(icons):
                # import pdb;pdb.set_trace()
                #size = (spacing*(.85-.1*len(icons)), spacing*(.85-.1*len(icons)))
                size = (spacing*.8/sqrt(len(icons)),spacing*.8/sqrt(len(icons)))
                insert = [center[0] - size[0]/2,
                          center[1] - size[1]/2 - attrs.get("height",0)*sin(camera_angle)]
                if len(icons) == 1:
                    radius = 0
                elif 2 <= len(icons) <4:
                    radius = spacing/4
                else:
                    radius = spacing/3
                    
                insert[0] += radius*cos(2*pi*(i)/len(icons))
                insert[1] += radius*sin(2*pi*(i)/len(icons))*cos(camera_angle)
     
                img_id = svg_identifier(f"img-{resource}-{len(icons)}")
                if img_id not in images:
                    img = svg.image(id_=img_id, href=embed_image(f"sprites/{resource}.png"), size=size)
                    svg.defs.add(img)
                    images[img_id] = img
                
                img = svg.use(href=f"#{img_id}", insert=insert)  # note that use doesn't support size
                group.add(img)
            
            
    svg.viewbox(bounds[0],bounds[1],bounds[2]-bounds[0], bounds[3]-bounds[1])
    # svg.width = f"bounds[2]-bounds[0]
    # svg.height = bounds[3]-bounds[1]
    # Background and axes
    if level.get("background", False):
        svg.add(svg.rect((bounds[0],bounds[1]),(bounds[2]-bounds[0], bounds[3]-bounds[1]), fill=level["background"]))
    if level.get("grid", False):
        svg.add(make_grid(spacing, *bounds, **level["grid"] ))

    # Tiles
    tilegroup = svg.g(id_=f"{level_id}-tiles")
    svg.add(tilegroup)
    for k in sorted(tiles.keys()): #, key=lambda x:(x[1],, reverse=True):
        tilegroup.add(tiles[k])
    
    return svg