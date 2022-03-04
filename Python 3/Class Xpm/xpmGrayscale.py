import xpm
from xpm import *

class XpmGrayscale(Xpm):
    """XPM graphics files whose colors are all grayscale """
    def __init__(self):
        Xpm.__init__(self)
        self.brightnesses = {}    # "brightness" of gray colors (common integer
                                  # value of colors' R, G, B components) indexed 
                                  # by label
    
    def verifyGrayscaleAndCreateBrightnesses(self):
        """Verify that all colors are gray; create brightnesses table """
        for k in list(self.colorDefs.keys()):
            rgbStr = self.colorDefs[k]
            if rgbStr[:2] != rgbStr[2:4] or rgbStr[:2] != rgbStr[4:]:
                raise(invalidGrayscaleRgbDefError(rgbStr))
            self.brightnesses[k] = int(rgbStr[:2], 16)
    
    def fileToObject(self):
        """ Creates object's attributes; also verifies self.grayscale, 
            creates brightnesses table. """
        Xpm.fileToObject(self)
        self.verifyGrayscaleAndCreateBrightnesses()

class invalidGrayscaleRgbDefError(Exception):
    def __init__(self, value):
        self.value = value
