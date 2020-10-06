OPTS = -Og -ggdb -shared -fPIC -Wall -Wextra
UFLAGS = $(env CPPFLAGS) $(env CFLAGS) $(env LDFLAGS)

forcemd5.so: forcemd5.c Makefile
	clang $(OPTS) -ldl $(FLAGS) -o forcemd5.so forcemd5.c
