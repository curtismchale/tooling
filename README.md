# Tooling

A collection of scripts to do things like optimize images or pdfs or...who knows what will come.

## Usage

Clone the repository. Make the scripts executable with `chmod +x <file>.sh` move it to directory you want to run it on and then run `sh <file>.sh`.

Install [`pngcrush`](https://pmt.sourceforge.io/pngcrush/), [`advpng`](https://github.com/imagemin/advpng-bin), [`optipng`](https://optipng.sourceforge.net/), [`jpegoptim`](https://github.com/tjko/jpegoptim), and [`ghostscript`](https://www.ghostscript.com/).

This can take a long time to run. I ran it on 12 sample customer folders and the `png` compression alone took 2 days to run on my biggest folders of 42GB.

The `pdf` compression also takes a while to go through all your directories if you're working with a lot of files.

## License

Do whatever you want with this.
