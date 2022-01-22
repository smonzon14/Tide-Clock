# Tide Clock

A clock that tells the tide.
Prototype project that uses a specified beach (among a list of beaches and their harmonics) to approximate the time until the next high/low tide, and display it on a dial style clock.

![alt text](https://github.com/smonzon14/Tide-Clock/blob/main/tide_clock/tide_clock.png?raw=true)
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
