# nand2tetris-nand-counter
Count how many nand gates each chip uses.

I was curious how many nand gates each of my chips used, and whether I could
use fewer with different implementations.

This script will parse the hdl files and recursively count the number of nand
gates per chip.

e.g.,

$ ./counter.py  *.hdl
And: 2
Mux16: 64
And16: 32
Or8Way: 21
Mux4Way16: 192
Mux8Way16: 448
DMux8Way: 35
Nand: 1
DMux4Way: 15
Not: 1
Not16: 16
HalfAdder: 7
Add16: 262
Or16: 48
FullAdder: 17
Xor: 5
Or: 3
ALU: 772
Inc16: 262
Mux: 4
DMux: 5
