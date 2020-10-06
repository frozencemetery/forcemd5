FLAGS = $(env CPPFLAGS) $(env CFLAGS) $(env LDFLAGS)

forcemd5.so: forcemd5.c Makefile
	clang -Og -ggdb -shared -fPIC -ldl $(FLAGS) -o forcemd5.so forcemd5.c
