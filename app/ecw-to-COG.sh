#!/bin/bash
set -exu -o pipefail

MAP_TO_CONVERT=$1
UPLOAD_FOLDER=$2

# Taking out the extension name
COG_MAP=`echo $MAP_TO_CONVERT | cut -d '.' -f 1`

docker run --rm -v $UPLOAD_FOLDER:/data geodata/gdal:latest /bin/bash -c "gdal_translate -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=2 -co ZLEVEL=9 -co BIGTIFF=YES $MAP_TO_CONVERT $COG_MAP'_converted.tiff'"
