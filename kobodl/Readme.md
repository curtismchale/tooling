## Kobodl

This is [kobodl](https://github.com/subdavis/kobo-book-downloader) which lets you download your Kobo books. If you use `direnv` then this can be set up to load automatically with `echo "use nix" > .envrc` and then `direnv allow`. Now when you change into this directory it will automatically load kobodl and python.

See full documentation check out [kobodl](https://github.com/subdavis/kobo-book-downloader) but here are a few commands.

```bash
# Get started by adding one or more users
kobodl user add

# List books
kobodl book list

# List all books, including those marked as read
kobodl book list --read

# Download a single book with default options when only 1 user exists
# default output directory is `./kobo_downloads` 
kobodl book get c1db3f5c-82da-4dda-9d81-fa718d5d1d16
```
