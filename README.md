# crackingxoroshiro128plus
[![Build Status](https://travis-ci.org/lemire/crackingxoroshiro128plus.png)](https://travis-ci.org/lemire/crackingxoroshiro128plus)

Xoroshiro128+ is a popular random generator. Given a couple of outputs of xoroshiro128+, you can often derive the seed necessary to generate the desired output. See my post  [“Cracking” random number generators (xoroshiro128+)](https://lemire.me/blog/2017/08/22/cracking-random-number-generators-xoroshiro128/)

## Usage

- I assume you have either macOS or a Linux shell.
- Install z3, the theorem prover, make sure to include Python support. If you have pip, type ``pip install z3-solver --user``. If you do not have pip, you should [install it](https://pip.readthedocs.io/en/stable/installing/).
- Have some 16-byte string you wish to generate (such as " Daniel Lemire  ").
- Type
```
cc -o xoroshift xoroshift.c && ./xoroshift $(python xoroshift.py " Daniel Lemire  ") |hexdump -C|more
```
- It works with " Daniel Lemire  ", but it is not possible to generate all outputs. When it is not possible to generate the desired output, a seed to generate the output "Sorry,  I can't." will be generated instead.
- There could be several possible 128-bit seeds able to generate a given 64-bit output. The script solves for one possible seed, but a modification of the script could generate all of the solutions.

- The script ``xoroshiftall.py`` finds all possible seeds for a given output sequence of numbers. Try ``python xoroshiftall.py 0 0xdeadbeef``.

## Source code of the generator

```C
// http://vigna.di.unimi.it/xorshift/xoroshiro128plus.c

uint64_t s[2];

static inline uint64_t rotl(const uint64_t x, int k) {
        return (x << k) | (x >> (64 - k));
}

uint64_t next(void) {
        const uint64_t s0 = s[0];
        uint64_t s1 = s[1];
        const uint64_t result = s0 + s1;

        s1 ^= s0;
        s[0] = rotl(s0, 55) ^ s1 ^ (s1 << 14); // a, b
        s[1] = rotl(s1, 36); // c
        return result;
}
```

## Further Work


We could also use [cryptol](https://github.com/GaloisInc/cryptol).
