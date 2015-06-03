CC=gcc

read_hashfile: translate_hashfile.c libhashfile.c
	$(CC) -Wall translate_hashfile.c libhashfile.c -o translate_hashfile

clean:
	rm -f read_hashfile
