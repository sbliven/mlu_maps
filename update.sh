#!/bin/bash
# Update all levels

for level in levels/*.yaml; do
    out="docs/maps/$(basename "${level%.*}")"
    python mlu_map.py "$level" "${out}.svg"
    magick convert "${out}.svg" "${out}.png"
done
