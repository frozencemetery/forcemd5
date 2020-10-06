#!/usr/bin/python3

import shlex
import subprocess
import sys

from typing import Dict, Optional

def p(s: str) -> None:
    sys.stdout.write(f"{s}\n")
    sys.stdout.flush()

def r(c: str, e: Optional[Dict[str, str]] = None, fail: bool = False) -> None:
    proc = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          shell=True, input=b"hi", env=e)
    if proc.returncode == 0 and not fail:
        p(f"[expected pass] `{c}` with env {e}")
    elif proc.returncode != 0 and fail:
        p(f"[expected fail] `{c}` with env {e}")
    elif proc.returncode == 0 and fail:
        p(f"[unexpected pass] `{c}` with env {e}")
        p(f"Output:\n{proc.stdout.decode('utf-8')}")
        exit(-1)
    else:
        p(f"[unexpected fail] `{c}` with env {e}")
        p(f"Output:\n{proc.stdout.decode('utf-8')}")
        exit(-1)

r("fips-finish-install --complete")

env = {"LD_PRELOAD": f"./forcemd5.so"}

p("Sanity checks first:")
r("openssl md5", env)
r("openssl md4", env)

p("These are both forbidden under FIPS:")
env["OPENSSL_FORCE_FIPS_MODE"] = "1"
r("openssl md5", env, fail=True)
r("openssl md4", env, fail=True)

p("The env var should only control MD5:")
env["OPENSSL_FIPS_NON_MD5_ALLOW"] = "1"
r("openssl md5", env)
r("openssl md4", env, fail=True)

p("The env var shouldn't break non-FIPS runs:")
del(env["OPENSSL_FORCE_FIPS_MODE"])
r("openssl md4", env)
r("openssl md5", env)
