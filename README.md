# Tide Clock

### Contains xtide-2.15.3

Added a new mode (-m n) for spitting out next high and low tide in chronological order. Requires libtcd-2.2.7 and .tcd harmonics file

```bash
export HFILE_PATH=[directory/file name for .tcd]
./configure
make
make install
```

### tide_clock

For tesing use -t (this will exclude the EDP library and export the bitmap to PNG format)
Make sure to run while in the tide_clock folder if using terminal. (clock.bmp path will change)