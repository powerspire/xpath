import sys, getopt, ntpath
# sys.setdefaultencoding('utf8')



def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        filename = ntpath.basename(argv[0])                         # lop off the path from the file name
        opts, args = getopt.getopt(argv[1:], "hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print '-i <inputfile> -o <outputfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print "Usage: {} -i <inputfile> -o <outputfile>".format(filename)
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
    print "Input file is {}".format(inputfile)
    print "Output file is {}".format(outputfile)

if __name__ == "__main__":
   main(sys.argv[0:])