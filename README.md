# forcemd5

A simple shared library which approximates the old behavior of
`$OPENSSL_FIPS_NON_MD5_ALLOW=1`.

To use (for example):

```sh
make
LD_PRELOAD=./forcemd5.so OPENSSL_FIPS_NON_MD5_ALLOW=1 /path/to/your/application
```

Caveats:

- This requires your application to be using the EVP interface, which it's
  "supposed to" be doing already for compliance.  Porting to that is easy.
- You are responsible for keeping your system in FIPS compliance.
  Specifically, this library, you only remain in compliance with FIPS if
  either all MD5 is non-cryptographic, or all MD5 communication takes place
  over an otherwise secured channel.
- Note that the previous caveat is necessary but not sufficient for
  compliance.  Talk to your vendor if you need specific guidance.
