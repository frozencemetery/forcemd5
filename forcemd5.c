/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. */

#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>

#include <openssl/evp.h>

static inline int three(const char *fname, const void *one, const void *two,
                        const void *three) {
    int (*f)(void *, void *, void *);

    f = dlsym(RTLD_NEXT, fname);
    if (!f)
        exit(2);

    return f((void *)one, (void *)two, (void *)three);
}

int EVP_DigestInit_ex(EVP_MD_CTX *ctx, const EVP_MD *type, ENGINE *impl) {
    return three(__func__, ctx, type, impl);
}
