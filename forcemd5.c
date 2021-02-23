/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. */

#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>

#include <openssl/evp.h>

static inline int f3(const char *fname, const void *one, const void *two,
                     const void *three) {
    int (*f)(void *, void *, void *);

    f = dlsym(RTLD_NEXT, fname);
    if (!f)
        exit(2);

    return f((void *)one, (void *)two, (void *)three);
}

static void interfere(EVP_MD_CTX *ctx, const EVP_MD *type) {
    char *e;

    e = getenv("OPENSSL_FIPS_NON_MD5_ALLOW");
    if (!e || e[0] == '\0' || e[0] == '0' || e[0] == 'n')
        return;

    if (type != EVP_md5() || !FIPS_mode())
        return;

    EVP_MD_CTX_set_flags(ctx, EVP_MD_CTX_FLAG_NON_FIPS_ALLOW);
}

int EVP_DigestInit_ex(EVP_MD_CTX *ctx, const EVP_MD *type, ENGINE *impl) {
    interfere(ctx, type);
    return f3(__func__, ctx, type, impl);
}

/* EVP_Digest() and EVP_DigestInit() are both implemented in terms of
 * EVP_DigestInit_ex().  Cheating?  Kinda, but there's no other way to handle
 * EVP_Digest() without reimplementation here becuse the context is
 * function-internal. */
