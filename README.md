# crackingxoroshiro128plus

Given a couple of outputs of xoroshiro128+, you can derive the seed and thus predict the outcome at will.

## Usage

- I assume you have either macOS or a Linux shell.
- Install z3, the theorem prover, make sure to include Python support.
- Type
```
gcc -o xoroshift xoroshift.c && ./xoroshift $(python xorshift.py " Daniel Lemire  ") |hexdump -C|more
```
