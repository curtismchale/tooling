#!/bin/bash
find . -name '*.pdf' -execdir sh -c '
for f do
    filename=${f##*/} && extension=${f##*.} \
        && filename=${filename%.*} && outpt=$filename-compressed.pdf
    gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile="$outpt" "$filename.pdf";
    echo "original $filename"
    echo "output $outpt"
    mv "$outpt" "$filename.pdf"
    # rm "$filename.pdf" # remove original
done' find-sh {} +
