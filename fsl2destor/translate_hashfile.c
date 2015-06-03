/*
 * Copyright (c) 2014 Sonam Mandal
 * Copyright (c) 2014 Vasily Tarasov
 * Copyright (c) 2014 Will Buik
 * Copyright (c) 2014 Erez Zadok
 * Copyright (c) 2014 Geoff Kuenning
 * Copyright (c) 2014 Stony Brook University
 * Copyright (c) 2014 Harvey Mudd College
 * Copyright (c) 2014 The Research Foundation of the State University of New York
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <sys/types.h>
#include <errno.h>
#include <time.h>
#include <string.h>

/* Use this macros if libhashfile library is installed on your system */
// #include <libhashfile.h>

/* Use this macros if libhashfile library is NOT installed on your system */
#include "libhashfile.h"

#define MAXLINE	4096

void hash2code(unsigned char hash[20], char code[40]) {
	int i, j, b;
	unsigned char a, c;
	i = 0;
	for (i = 0; i < 20; i++) {
		a = hash[i];
		for (j = 0; j < 2; j++) {
			b = a / 16;
			switch (b) {
			case 10:
				c = 'A';
				break;
			case 11:
				c = 'B';
				break;
			case 12:
				c = 'C';
				break;
			case 13:
				c = 'D';
				break;
			case 14:
				c = 'E';
				break;
			case 15:
				c = 'F';
				break;
			default:
				c = b + 48;
				break;

			}
			code[2 * i + j] = c;
			a = a << 4;
		}
	}
}

static void print_chunk_hash(uint64_t chunk_count, const uint8_t *hash,
					int hash_size_in_bytes)
{
	int j;

	printf("Chunk %06"PRIu64 ": ", chunk_count);

	printf("%.2hhx", hash[0]);
	for (j = 1; j < hash_size_in_bytes; j++)
		printf(":%.2hhx", hash[j]);
	printf("\n");
}

static int translate_hashfile(char *hashfile_name)
{
	char buf[MAXLINE];
	struct hashfile_handle *handle;
	const struct chunk_info *ci;
	uint64_t chunk_count;
	time_t scan_start_time;
	int ret;

    /* outputfile for dumping destor trace */
    char* outputfilename = malloc(strlen(hashfile_name)+strlen(".destor")+1);
    strcpy(outputfilename, hashfile_name);
    strcat(outputfilename, ".destor");

    FILE* output = fopen(outputfilename, "a");
    if(output == NULL){
		fprintf(stderr, "Error opening output file: %s, with %d!", outputfilename, errno);
        return -1;
    }

	handle = hashfile_open(hashfile_name);
	if (!handle) {
		fprintf(stderr, "Error opening hash file: %d!", errno);
		return -1;
	}

	/* Print some information about the hash file */
	scan_start_time = hashfile_start_time(handle);
	printf("Collected at [%s] on %s",
			hashfile_sysid(handle),
			ctime(&scan_start_time));

	ret = hashfile_chunking_method_str(handle, buf, MAXLINE);
	if (ret < 0) {
		fprintf(stderr, "Unrecognized chunking method: %d!", errno);
		return -1;
	}

	printf("Chunking method: %s", buf);

	ret = hashfile_hashing_method_str(handle, buf, MAXLINE);
	if (ret < 0) {
		fprintf(stderr, "Unrecognized hashing method: %d!", errno);
		return -1;
	}

	printf("Hashing method: %s\n", buf);

	/* Go over the files in a hashfile */
	printf("== List of files and hashes ==\n");
	while (1) {
		ret = hashfile_next_file(handle);
		if (ret < 0) {
			fprintf(stderr,
				"Cannot get next file from a hashfile: %d!\n",
				errno);
			return -1;
		}

		/* exit the loop if it was the last file */
		if (ret == 0)
			break;

		printf("File path: %s\n", hashfile_curfile_path(handle));
		printf("File size: %"PRIu64 " B\n",
				hashfile_curfile_size(handle));
		printf("Chunks number: %" PRIu64 "\n",
				hashfile_curfile_numchunks(handle));

		fprintf(output, "file start %zd\n", strlen(hashfile_curfile_path(handle)));
		fprintf(output, "%s\n", hashfile_curfile_path(handle));

		/* Go over the chunks in the current file */
		chunk_count = 0;
		while (1) {
			ci = hashfile_next_chunk(handle);
			if (!ci) /* exit the loop if it was the last chunk */
				break;

			chunk_count++;

			print_chunk_hash(chunk_count, ci->hash,
					hashfile_hash_size(handle) / 8);

            /*
             * Need some padding.
             */
            char hash[20], code[41];
            memset(hash, 0, 20);
            memcpy(hash, ci->hash, hashfile_hash_size(handle) / 8);
            hash2code(hash, code);
            code[40] = 0;
			fprintf(output, "%s %" PRId64 "\n", code, ci->size);
		}

		fprintf(output, "file end\n");
	}

	hashfile_close(handle);

	fprintf(output, "stream end");
	fclose(output);

    free(outputfilename);

	return 0;
}

int main(int argc, char *argv[])
{
	if (argc != 2) {
		fprintf(stderr, "Wrong usage!\n");
		fprintf(stderr, "Usage: %s <hashfile>\n", argv[0]);
		return -1;
	}

	return translate_hashfile(argv[1]);
}
