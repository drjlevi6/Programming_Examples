In 2000, I created a bitmap font, "HexDump" whose characters would show the 
hexadecimal numbers from 0 to 255 (i.e., "FF" for the hexadecimal number 
0xFF). 

I began with text versions of the images to be shown, consisting of letters 
"X" and " ", i.e.,

 XXX                 XXXXX
X   X                    X
X   X                   X
X   X                   X
X   X                  X
X   X                  X
X   X                 X
 XXX       ,          X
    XXX                 XXXXX
   X   X                X
   X   X                X
   X   X                XXX
   X   X                X
   X   X                X
   X   X                X
    XXX                 X

I then converted them to a Mac Classic resource description file, HexDump.drez;
these I converted this to a Classic Macintosh bitmap font, "HexDump", using the
Rez resource-compilation program.

This repository folder contains the HexDump font, its resource-description 
precursor HexDump.drez, a snapshot of its characters using the Classic Mac 
KeyCaps application, and some samples of its output at differing sizes, "Key 
Caps - Hexdump And Arial.png".