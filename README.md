photo-webpage
=============

Webpage code for http://photo.mofo.ca

Commands
--------

To regenerate gallery, put images in photo-webpage/gallery, then run:

    grunt gengallery

To rename images to start with numbers:

    find . -name '*.jpg' | awk 'BEGIN{ a=0 }{ printf "mv %s %04d.jpg\n", $0, a++ }' | bash

Then they can be reordered with

    ./bin/reorder_files.py <jpg path> <new position>
