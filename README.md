# MLU Maps

Editor for 2D maps for worlds based on
[Goldberg polyhedra](https://en.wikipedia.org/wiki/Goldberg_polyhedron), such as
[My Little Universe](https://say.games/games/my-little-universe/) by SayGames.

**[View Maps](https://sbliven.github.io/mlu_maps/)**

![Diamond Mine](docs/maps/diamond_mine.svg)

## How to read maps

MLU planets are Goldberg polyhedra, meaning they are composed of hexagons placed at the
vertices of a [geodesic sphere](https://en.wikipedia.org/wiki/Geodesic_polyhedron).
All planets have exactly 12 pentagons, located at the points of an icosohedron. Large
planets have seven hexagons between each pentagon, while small planets have three.

To form a map, the 3D shape is "unrolled" by adding gaps between tiles until it lies
flat. This is called a [net](https://en.wikipedia.org/wiki/Net_(polyhedron)) and can be
pictured like this:

![Animation of an icosohedral net rolling up](https://upload.wikimedia.org/wikipedia/commons/a/a2/Icosaedro_desarrollo.gif)

*Image Credit: [Unfolding an icosahedron](https://en.wikipedia.org/wiki/Regular_icosahedron#/media/File:Icosaedro_desarrollo.gif)
by Rectas. Wikimedia Commons. CC0*

This means that all edges in the map will wrap around to join up somewhere else. Paths
in the world may cross gaps, and straight lines change direction when crossing an edge.
Where possible, edges have been chosen in oceans or mountains to make it easier to
navigate.

## Creating maps

Using the tool is described [here](usage.md). It describes how to change level contents
and styles. Contributions of official MLU maps are welcome! See
[Contributing](CONTRIBUTING.md) for more information.

## Contributing

There are many ways to contribute! Most don't require any coding skills, but rather the patience to encode maps into a readable format.

Please see [CONTRIBUTING](CONTRIBUTING.md) for information on how to contribute.

## Level Progress

| Level                  | Tiles | Resources | Numbers |
| ---------------------- | ----- | --------- | ------- |
| 1. Gaia                | ❌    | ❌        | ❌      |
| 2. Trollheim           | ✅    | ⚠️         | ⚠️       |
| 2.1 Azurite Cavern     | ⚠️     | ⚠️         | ❌      |
| 2.2 Stufurs Lair       | ❌    | ❌        | ❌      |
| 2.3 Skellirs Lair      | ⚠️     | ⚠️         | ❌      |
| 3. Dimidium            | ✅    | ✅        | ⚠️       |
| 3.1 Shipwreck Shallows | ❌    | ❌        | ❌      |
| 3.2 Molten Abyss       | ❌    | ❌        | ❌      |
| 3.3 Diamond Mine       | ✅    | ✅        | ❌      |
| 3.4 Crash Site         | ❌    | ❌        | ❌      |
| 3.5 Crabster Zone      | ❌    | ❌        | ❌      |
| 3.6 Rise of Tentacles  | ❌    | ❌        | ❌      |
| 4. Factorium           | ❌    | ❌        | ❌      |
| 4.1 Mystery Keep       | ❌    | ❌        | ❌      |
| 4.2 Engine Room        | ❌    | ❌        | ❌      |
| 4.3 Einhar             | ❌    | ❌        | ❌      |
| 4.4 A 69               | ⚠️     | ⚠️         | ❌      |
| 5. Wadirum             | ❌    | ❌        | ❌      |
| 6. Odysseum            | ❌    | ❌        | ❌      |
| 7. Dragonora           | ❌    | ❌        | ❌      |
| 8. Egyptium            | ❌    | ❌        | ❌      |
| 9. Asium               | ❌    | ❌        | ❌      |

✅ Finished
⚠️ Started (often on paper)
❌ Not started

## License

Copyright Spencer Bliven and released under the GPL 3.0 or later license.

Game artwork copyright SayGames.
