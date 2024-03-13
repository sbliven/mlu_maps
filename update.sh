#!/bin/bash
# Update SVG and PNG from the YAML file
# usage: update.sh [levelnames|yaml_files...]

script_dir="$(dirname "$0")"

# Default to processing all levels
if [ "$#" -eq 0 ]; then
    levels=("$script_dir/levels/"*.yaml)
else
    levels=("$@")
fi

for level in "${levels[@]}"; do
    if [[ ! -f "$level" && -f "$script_dir/levels/$level.yaml" ]]; then
        level="$script_dir/levels/$level.yaml"
    fi
    echo "Processing $(basename "${level%.*}")"
    out="$script_dir/docs/maps/$(basename "${level%.*}")"
    python "$script_dir/mlu_map.py" "$level" "${out}.svg"
    magick convert "${out}.svg" -strip "${out}.png"
done
