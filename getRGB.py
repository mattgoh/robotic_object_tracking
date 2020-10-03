import sys;
import os;
from PIL import Image;

def print_help():
    print "USAGE: getRGB";
    print "  --i imagefile";
    return 0;

class getRGB:
    def __init__(self, fname):
        self.fname = fname; # not sure this is needed
        #self.pixVal = pixVal
        
    def imRGB(self, pixVal=list("")):
        im = Image.open('%s', ' r') % self.fname
        self.pixVal = list(im.getdata())
        return self.pixVal

nargs = len(sys.argv) - 1;
if(nargs == 0):
    print_help();
    sys.exit(0);