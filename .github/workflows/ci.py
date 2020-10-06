#!/usr/bin/python3

import subprocess

from typing import Dict, Optional

def run(c: str, env: Optional[Dict[str, str]] = None,
        fail: bool = False) -> None:
    proc = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          shell=True, input=b"hi", env=env)
    if proc.returncode == 0 and not fail:
        print(f"[expected pass] `{c}` with env {e}")
    elif proc.returncode != 0 and fail:
        print(f"[expected fail] `{c}` with env {e}")
    elif proc.returncode == 0 and fail:
        print(f"[unexpected pass] `{c}` with env {e}")
        print(f"Output:\n{proc.stdout.decode('utf-8')}")
        exit(-1)
    else:
        print(f"[unexpected fail] `{c}` with env {e}")
        print(f"Output:\n{proc.stdout.decode('utf-8')}")
        exit(-1)

run("fips-finish-install --complete")

env = {"LD_PRELOAD": "./forcemd5.so"}

print("Sanity checks first:")
run("openssl md5", env)
run("openssl md4", env)

print("These are both forbidden under FIPS:")
env["OPENSSL_FORCE_FIPS_MODE"] = "1"
run("openssl md5", env, fail=True)
run("openssl md4", env, fail=True)

print("The env var should only control MD5:")
env["OPENSSL_FIPS_NON_MD5_ALLOW"] = "1"
run("openssl md5", env)
run("openssl md4", env, fail=True)

print("The env var shouldn't break non-FIPS runs:")
del(env["OPENSSL_FORCE_FIPS_MODE"])
run("openssl md4", env)
run("openssl md5", env)
