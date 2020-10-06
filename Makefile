FLAGS = $(env CPPFLAGS) $(env CFLAGS) $(env LDFLAGS)

forcemd5.so: forcemd5.c
	gcc -Og -ggdb -shared $(FLAGS) -o forcemd5.so forcemd5.c
