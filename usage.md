# Usage

## Installation

Running `mlu_map.py` requires python and the following packages:
- svgwrite
- pyyaml

These can be installed with pip:
```
pip install svgwrite pyyaml
```

or with conda:
```
conda env create -f environment.yaml
conda activate mlu
```

## Running

Use `mlu_map.py` to generate the level:

```
python mlu_map.py levels/test.yaml docs/maps/test.svg
```

## Level syntax

Levels are defined by a yaml file. See `levels/` for examples.

### Example

Here is the `test.yaml` example. Some aspects are expanded on below.

```yaml
# Define anchors that can be reused later with `<<: *anchor`
defs:
- &platform
  type: platform
  height: 20
- &ocean
  type: ocean
  height: 0
- &wall
  type: wall
  height: 30
- &plain
  type: plain
  height: 10

# List of levels
# Usually the first level is used, but others can be selected with `--levels`
levels:
- name: testlvl
  # Defaults for all regions.
  defaults: *ocean
  # Tile width. Default: 100
  spacing: 100
  # Customize background. Should match the CSS background
  background: white
  # Settings for the triangular grid
  grid:
    origin: [0,-1]  # Grid origin (any major-major intersection)
    major: 2  # Spacing between major grid lines
    minor: 1  # Spacing between minor grid lines

  # Group tiles by region (aka biome) for easy styling
  regions:
  - name: home
    # Override level defaults with region-specific ones
    defaults: *plain
    # List of all tiles
    tiles:
    # Full tile definition
    - coord: [0,0]  # (required)
      # tile type, for styling
      type: plain
      # tile height
      height: 15
      # (optional) list of sprites. Includes resources and mobs
      resources:
      - Rock
      - Spider
      - Acorn
      - Sulphur Deposit 2
      - Sandstone Rock
      - Rock Monster
      # Currently ignored, but may be used for extra graphics eventually
      decor:
      - bridge_e_w
    # Concise tile using a pre-defined type
    - coord: [0,1]
      <<: *wall
    - coord: [1,1]
      <<: *wall
    # Even more concise tile using all defaults
    - coord: [-1,0]
    - coord: [1,0]
    - coord: [-1,-1]
      <<: *ocean
    - coord: [0,-1]
      <<: *ocean

# CSS styles
# Each tile polygon is annotated with class="tile r-<region> t-<type> tile-[top|left|right]"
# Be careful not to include any blank lines to end the yaml multi-line string
styles: |
  svg {
    background-color: grey;
  }
  .grid-major {
    stroke-width:1.5;
  }
  .grid-minor {
    stroke-width:.5;
  }
  /* Defaults for all tiles */
  .tile {
    stroke: black;
    stroke-width: 0.5;
  }
  /* Override for "ocean" type */
  .t-ocean {
    stroke: none;
    fill: #0000aa;
  }
  /* Colors for "wall" type */
  .t-wall.tile-top {
    fill: #514660;
  }
  .t-wall.tile-left {
    fill: #20182E;
  }
  .t-wall.tile-right {
    fill: #20182E;
  }
  /* Colors for "plain" type */
  .t-plain.tile-top {
    fill: #F5B908;
  }
  .t-plain.tile-left {
    fill: #351709;
  }
  .t-plain.tile-right {
    fill: #6C3319;
  }

```

### Tile attributes

Most of the configuration consists of the `tiles` array. Each hexagon is assigned an
[x,y] coordinate, where the x-axis goes horizontally and the y-axis is at a 120° angle
increasing to the top left.

Each tile is assigned a type. The types are arbitrary strings, but are used for styling
each tile using CSS.

Tiles are grouped into levels and regions. Defaults for attributes such as `type` and 
`height` can be defined in the `defaults` dictionary for levels and regions and then
overridden.

The example uses [anchors and aliases](https://yaml.org/spec/1.2.2/#3222-anchors-and-aliases)
and [merge keys](https://yaml.org/type/merge.html) to be more compact, but you could
also specify `type` and `height` for each tile explicitly and omit the `defs` section.

### Styles

Each tile consists of a set of polygons, usually a "top" (the hexagon) and two
parallelograms ("left" and "right"). (Some orientations of pentagons also have a third
"mid" parallelogram, but it can be ignored for styling.) Each polygon is annotated with

    class="tile r-<region> t-<type> tile-<direction>"

This allows each face to be colored independently using css rules based on region, type,
and direction.

## Website

The website is served statically from the `docs` folder.

Javascript for dynamically showing SVG content only works when accessing the files
from a web server (eg not with `file://`). An easy way to serve the pages is with docker:

```
docker run --name mlu -v $PWD/docs:/usr/share/nginx/html:ro -p 8080:80 -d nginx
```

