# convert.c and convert.py
# Convert an obsolete trace file generated by destor 0.1 
#  into a trace file recognized by a new version of destor.

import sys

# sys.argv[1] is the path of the input file that is converted.

infile = sys.argv[1]
outfile = infile+".new"

print "read from file:", infile
print "write to file:", outfile

try:
    infd = open(infile, "r")
    outfd = open(outfile, "w")

    i=0
    for line in infd:
        if line[0:len("fileindex=")] == "fileindex=":
            name = "_file"+str(i)
            outfd.write("file start %d\n" % len(name))
            outfd.write("%s\n" % name) 
        elif line == "STREAM_END":
            outfd.write("stream end")
        elif line == "FILE_END\n":
            outfd.write("file end\n")
            i=i+1
        else:
            outfd.write("%s %d\n" % (line[0:40],int(line[41:])))

    infd.close()
    outfd.close()
except IOError, e:
    print e
except Exception, ex:
    print 'Somthing goes wrong!\n',ex
else:
    print 'Success'

