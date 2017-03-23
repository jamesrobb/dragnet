#!/bin/bash
image="$1"
draw=$(convert $image                              \
   -threshold 50%                                  \
   -define connected-components:verbose=true       \
   -define connected-components:area-threshold=10  \
   -connected-components 8                         \
   -auto-level objects.png )

echo "$image" $draw
#eval convert "$image" -fill none -strokewidth 2 -stroke red $draw result.png
