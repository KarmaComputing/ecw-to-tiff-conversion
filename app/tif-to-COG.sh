#!/bin/bash
set -exu -o pipefail

MAP_TO_CONVERT=$1
UPLOAD_FOLDER=$2

# Taking out the extension name
COG_MAP=$(echo "$MAP_TO_CONVERT" | cut -d '.' -f 1)

docker run --rm -v "$UPLOAD_FOLDER":/data osgeo/gdal:latest /bin/bash -c "cd data; gdal_translate -of COG -co NUM_THREADS=ALL_CPUS  -co LEVEL=9 -co COMPRESS=DEFLATE -co BIGTIFF=YES -co PREDICTOR=2 $MAP_TO_CONVERT $COG_MAP'_converted.tiff'"

