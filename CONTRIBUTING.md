# Contributing

Thanks for helping! Contributions are welcome. All code is released under GPL3.0 or later.

## How to contribute

### Report mistakes

Please report any mistakes in the maps on the
[issues](https://github.com/sbliven/mlu_maps/issues) page! This can also be used
for problems with the tool itself or feature requests.

### Add a level

The biggest need currently is to add additional levels. This doesn't require
any coding knowledge, just a copy of the game and the patience to annotate tiles.

To start, read [usage](usage.md) for information about the yaml syntax and how
to convert yaml files into images. Then choose a new level and open up the game.

I usually make levels on paper first, then convert them to yaml. You can use
[hex graph paper](hex_grids/hexagonal-a4.pdf) for this. An example sketch of the
A69 dungeon is [here](hex_grids/a69_sketch.png).

The next step is to convert the level to yaml format. You can start with
[blank_8.yaml](levels/blank_8.yaml) (or [blank_4.yaml](levels/blank_4.yaml) for
dungeons). Then rearrange the `coord:` lines into different regions and tile
types.

### Add resource, enemy, and tile number annotations

After the tiles are layed out they should be annotated with `resources:` and
`tilenum:` annotations. The `resources` list includes both enemies and minable
resources. Tile numbers correspond to the order in which tiles are unlocked.
The [MLU Master Document](https://docs.google.com/spreadsheets/d/1PMukpen36T8nkHwEiYptsNPJVqO0srnOsDSn8ijunc8/edit?usp=sharing)
is useful for gathering resource names and tile numbers.

### Improve styling

The levels are converted to SVG images. You can help by improving the stylesheet
used for these images so that the results look more like the game. For instance,
the colors for each region and tile type can be customized individually. A
CSS stylesheet is defined at the end of each yaml file in the `styles:` string.

### Code fixes & features

Additional bug fixes and new features may require modifying the map generation
code. See the [issues](https://github.com/sbliven/mlu_maps/issues) page for
open bugs and feature requests.

## Pull Requests

To contribute changes, please fork this repository and make a pull request.

Please add your name or usename to [AUTHORS](AUTHORS.md) for attribution.

## Code style

Python code should use[black](https://black.readthedocs.io) code conventions.
