#!/bin/bash
image="$1"
draw=$(convert $image                              \
   -threshold 50%                                  \
   -define connected-components:verbose=true       \
   -define connected-components:area-threshold=10  \
   -connected-components 8                         \
   -auto-level objects.png | \
   awk 'BEGIN{command=""}
        /\+0\+0/||/id:/{next}
        {
          geom=$2
          gsub(/x/," ",geom)
          gsub(/\+/," ",geom)
          split(geom,a," ")
          d=sprintf("-draw \x27rectangle %d,%d %d,%d\x27 ",a[3],a[4],a[3]+a[1],a[4]+a[2])
          command = command d
          #printf "%d,%d %d,%d\n",a[3],a[4],a[3]+a[1],a[4]+a[2]
        }
        END{print command}')

eval convert "$image" -fill none -strokewidth 2 -stroke red $draw result.png
