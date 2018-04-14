//gcc -o xoroshift xoroshift.c && ./xoroshift $(python xoroshift.py " Daniel Lemire  ") |hexdump -C|more
 #include <ctype.h>
 #include <stdio.h>
 #include <stdlib.h>
 #include <unistd.h>
 #include <getopt.h>
 #include <stdint.h>
// xoroshiro generator taken from
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

int main(int argc, char **argv) {
    freopen(NULL, "wb", stdout);
    if(argc != 3) {
      printf("please provide two 64-bit unsigned integers in hexadecimal as arguments.\n");
      return -1;
    }
    s[0] = strtoull(argv[1], NULL, 16); //UINT64_C(10532447193056740057);
    s[1] = strtoull(argv[2], NULL, 16); //UINT64_C(15725061932195978535);
    while (1) {
        uint64_t value = next();
        fwrite((void*) &value, sizeof(value), 1, stdout);
    }
}
