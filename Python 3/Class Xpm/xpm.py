# Version 20160609: Doesn't use comments to locate sections (deletes 
#	 comments instead).
# Version 20160628: Doesn't delete comments; copyXpm() modifies name).
# 20170408: copyXpm() simplified using copy.deepcopy()
# 20170908: getOrAddColorDef(rgb) added
# 20180604: getOrAddColorDef() deleted. 
# 20200224: read() added, replaces readXpmFile().

import re, sys

class Xpm:
	"""A class for XPM graphics files"""
	def __init__(self):
		self.verbose = False
		self.inputLines = 0		 # 0-based; total # lines in input file
		self.xpmName = "Stdin"
		self.width = 0
		self.height = 0
		self.ncolors = 0
		self.chars_per_pixel = 0
		self.colorDefs = {}		 # dict: color labels + 6-digit RGB strings
									# SHOULD REVERSE LABELS AND STRINGS
		self.pixels = []			# array of color labels
		self.sourceFile = []
		self.labelChars = [
			'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
			'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
			'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
		]

	def getPixelColor(self, x, y):
		""" Gets the color label of the pixel at (x, y) """
		return self.pixels[x][y]
	
	def setPixelColor(self, x, y, pixelLabel):
		"""Sets a pixel by its color label."""
		if isValidPixelLabel(pixelLabel):
			self.pixels[x][y] = pixelLabel
		else:
			raise badPixelLabel(pixelLabel)
		
	def getOrAddColorDef(self, rgb):
		"""Finds/adds a color label for RGB string rgb;
			returns the key for the color definition."""
		self.errprint('getOrAddColorDef(): Add ' + rgb)
		for k in iter(self.colorDefs):
			if self.colorDefs[k] == rgb:
				return k
		labelSet = set(self.colorDefs.keys())
#	self.errprint("Current label strings: " + str(labelSet))

#	self.errprint(labelSet)

# Search for string built from label characters but not already a label
		if self.chars_per_pixel == 1:
			for c in self.labelChars:
				self.errprint("Checking char " + c + " as a label")
				if c not in labelSet:
					#insert new def and return new label
					self.colorDefs[c] = rgb
					self.ncolors += 1
					self.errprint('Label assigned: ' + c)
					return c
		elif self.chars_per_pixel == 2:
			for c in self.labelChars:
				for d in self.labelChars:
					c2Chars = c + d
					self.errprint("Checking " + c2Chars + " as a label")
					if c2Chars not in labelSet:
						#insert new def and return new label
						self.colorDefs[c2Chars] = rgb
						self.ncolors += 1
						self.errprint('Label assigned: ' + c2Chars)
						return c2Chars
		else:	 # For pixel labels with an arbitrary number of characters: 
				# since self.labelChars contains len(self.labelChars) characters, there 
				# are (len(self.labelChars) ** self.chars_per_pixel) possible 
				# strings. We set an index i to run from 0 to this number 
				# minus 1; we take the modulus of i by len(self.labelChars), use 
				# this this to choose the next character from self.labelChars, and 
				# divide i by len(self.labelChars) using integer division; we 
				# repeat the process (self.chars_per_pixel) times. 
			maxLabels = len(self.labelChars) ** self.chars_per_pixel
			if self.ncolors >= maxLabels:
				raise labelDictionaryFull("Cannot add color \"" + rgb + \
				"\" to the colorDefs dictionary, because the dictionary " + \
				"is full.")
				
			for i in range(maxLabels):
				itemp, label = [i, ""]
				# prepend j-th char to label
				for j in range(self.chars_per_pixel):	
					label = self.labelChars[itemp % len(self.labelChars)] + \
						label
					itemp //= len(self.labelChars)
				if label not in labelSet:
					self.colorDefs[label] = rgb
					self.ncolors += 1
					self.errprint('getOrAddColorDef(): Label assigned to ' + 
						rgb + ': ' + label)
					self.errprint()
					return label

	def addWhitePixelColorDef(self):
		""" Adds white pixel definition to Xpm object if none exists.
			(Modifies the existing object.) """
		pass			# come back and finish!
		# to xpm_colorDefs
			
	def copyDict(self, sourceDict, destDict):
		""" copy a dictionary's elements """
		return # short-circuit
		for k in sourceDict.keys():
			self.errprint("Key " + k + ": " + str(type(sourceDict[k])))
			if type(sourceDict[k]) in [int, str, bool]:
				destDict[k] = sourceDict[k]
			elif type(sourceDict[k]) == list:
				self.copyList(sourceDict[k], destDict[k])
				if k == 'pixels': self.errprint("len(pixels) after copy:" + \
					str(len(destDict[k])))
			elif type(sourceDict[k]) == dict:
					self.copyDict(sourceDict[k], destDict[k])
			else:
				raise unknownTypeError(sourceDict[k])

	def copyList(self, sourceList):
		""" copy and return a list's elements """
		destList = []
		for i in range(len(sourceList)):
			if type(sourceList[i]) in [int, str, bool]:
				self.errprint("copyList(): Copying list element " + 
					str(i) + ", " + str(sourceList[i]))
				destList.append(sourceList[i])
			elif type(sourceList[i]) == list:
				destList.append([])
				self.copyList(sourceList[i], destList[i])
			elif type(sourceList[i]) == dict:
				self.copyDict(sourceList[i], destList[i])
			else:
				raise unknownTypeError(sourceList[i])
		return destList

	def copyXpm(self):
		"""Copy Xpm (_assuming_ there's a source file) and rebuild."""
		self.errprint("copyXpm(): entered")
		import copy
		return copy.deepcopy(self)

	def errprint(self, *args):
		if self.verbose: print("errprint:", *args, file=sys.stderr, 
			flush=True)

	def expandXpm(self, scalefac):
		""" returns a copy of (self) expanded by (scalefac) """
		scaledXPM = Xpm()
		scaledXPM = self.copyXpx()
		
	def fileToObject(self):
		""" create new Xpm object's attributes from source file """
		self.errprint("fileToObject(): Entered")
		self.verifyXPM()
		self.getXpmName()
		self.getFileParameters()
		self.getColors()
		self.getPixels()

	def getColors(self):
		""" processes, counts color defs """
		self.errprint("getColors(): Entered")
		colorDefPat = '(?:\"\s*)(' + '.' * self.chars_per_pixel + ')' + \
			'(?: c #)([0-9a-fA-F]+)(?:\",\s*)'
		colorDefRE = re.compile(colorDefPat)
		for i in range(len(self.sourceFile)):
			if colorDefRE.search(self.sourceFile[i]):	# got first color def
				colorDefEntry = colorDefRE.split(self.sourceFile[i])
				colorDefsFound = 1
				self.errprint("getColors(): First def is line", i, 
					colorDefEntry)
				self.colorDefs[colorDefEntry[1]] = colorDefEntry[2]
				
				# loop through lines, adding defs and incrementing def count
				# until match fails.
				for j in range(i + 1, len(self.sourceFile)):
					if colorDefRE.search(self.sourceFile[j]):
						colorDefEntry = colorDefRE.split(self.sourceFile[j])
						colorDefsFound = colorDefsFound + 1
						self.errprint("getColors(): Additional def: line", j, 
							colorDefEntry)
						self.colorDefs[colorDefEntry[1]] = colorDefEntry[2]
						
					# Check that actual no. defs == self.ncolors, then return.
					elif colorDefsFound == self.ncolors:
						self.errprint("getColors(): Colors are:", self.colorDefs)
						return
					else:
						raise(badColorLineError("Specified no. color defs, " +
							str(self.ncolors) + ", doesn't match actual " +
							"no. color defs found, " + str(colorDefsFound)))
	
	def getFileParameters(self):
#		pat = re.compile('(?:"\s*)(\d+)\s+(\d+)\s+(\d+)\s+(\d+)(?:\",$)')
		pat = re.compile('(?:"\s*)(\d+)\s+(\d+)\s+(\d+)\s+(\d+)(?:\s*\",$)')
		for aLine in self.sourceFile:
			if pat.match(aLine):
				parmsList = pat.split(aLine)
				self.errprint("getFileParameters(): Parameters, untrimmed:", 
					parmsList)
				while "" in parmsList: parmsList.remove("")
				self.errprint("getFileParameters(): Parameters, trimmed:", 
					parmsList)
				self.width, self.height, self.ncolors, self.chars_per_pixel =\
					[int(parmsList[0]), int(parmsList[1]), int(parmsList[2]), 
					int(parmsList[3])]
				self.errprint("getFileParameters(): self.width:", self.width)
				self.errprint("getFileParameters(): self.height:", 
					self.height)
				self.errprint("getFileParameters(): self.ncolors:", 
					self.ncolors)
				self.errprint("getFileParameters(): self.chars_per_pixel:", \
					self.chars_per_pixel)
				return
		raise missedParamLineError("No valid definitions line found")
	
	def getPixels(self):
		"""splits strings of pixel labels into arrays"""
		self.errprint("getPixels(): Entered")
		
		# Create RE to find (width * chars_per_pixel) characters
		# surrounded by double-quotes:
		
		# find (width * cpp) non-" chars
		pixCharsRE = '([^"]{' + \
			str(self.width * self.chars_per_pixel) + '})' 
		self.errprint("getPixels(): pixCharsRE is:", pixCharsRE)
		
		# trim stuff before/after pixel characters.
		pixLineRE = r'(?:^.*?\")' + pixCharsRE + '(?:\\".*$)'	
		self.errprint("getPixels(): pixLineRE is:", pixLineRE)
		
		# RE to trim non-pixel characters.
		stripPixelsRE = re.compile(pixLineRE)
		
		# Split chunks of (c.p.p) characters from trimmed string;
		# append each to pixel array	 
		cppInt = int(self.chars_per_pixel)
		for i in range(len(self.sourceFile)):
			self.errprint("getPixels(): Line", i, self.sourceFile[i])
			strippedPixLine = re.sub(stripPixelsRE, "\\1", 
				self.sourceFile[i])
			self.errprint("getPixels(): trimmed line:", strippedPixLine)
			
			# (pix-chars found, sub made)
			if strippedPixLine != self.sourceFile[i]:	
				pixArray = []
				while len(strippedPixLine):
					pixArray.append(strippedPixLine[:cppInt])
					strippedPixLine = strippedPixLine[cppInt:]
				self.pixels.append(pixArray)
				self.errprint("getPixels(): Line " + str(i) + 
					" converted to pixels", pixArray)
		self.errprint("getPixels(): pixels array created.")

	def getWhitePixelLabel(self):
		"""Returns label of white pixels ("" if none.)"""
		whiteRGBPat = '^[fF]+$'	# recognizes white (all f/F) color def
		self.errprint("getWhitePixelLabel(): in iter(self.colorDefs) is", 
			iter(self.colorDefs))
		for colorLabel in iter(self.colorDefs):
			self.errprint("getWhitePixelLabel(): Color label is", colorLabel)
			self.errprint("getWhitePixelLabel(): Color is", 
				self.colorDefs[colorLabel])
			self.errprint("getWhitePixelLabel(): match result is", \
				re.match(whiteRGBPat, self.colorDefs[colorLabel]))
			if (re.match(whiteRGBPat, self.colorDefs[colorLabel]) != None):
				return colorLabel
		return ''	

	def getXpmName(self):
		for aLine in self.sourceFile:
			if isXpmNameLine(aLine):
				self.xpmName = self.getXpmNameFromXpmNameLine(aLine)
				self.errprint("getXpmName(): self.xpmName was set to:", 
					self.xpmName)
				return
		raise(badStaticNameError("getXpmName(): No valid name line found"))

	def getXpmNameFromXpmNameLine(self, nameLine):
		self.errprint("getXpmNameFromXpmNameLine(): nameline:", nameLine)
		
		# name is string between * and [ in nameLine
		xpmName = re.sub(r'.+\*(.+)\[.+', r'\1', nameLine)
		self.errprint("getXpmNameFromXpmNameLine(): xpmName is", xpmName)
		return xpmName

	def input(self):
		"""Read an XPM file from standard input (redirected file 
			 presumed).
		"""
		self.errprint('input(): Entered')
		if self.verbose: lineno = 0	
		while True:
			try:
				ip = input()
				ip = re.sub('\r', '', ip)	# if infile has Windows linebreaks
			except(EOFError):
				break
			self.sourceFile.append(ip)
			if self.verbose:
				self.errprint('input(): Read line ' + str(lineno) + ":", ip)
				lineno = lineno + 1

	def insertIntoName(self, insert):
		"""Insert insertion pre suffix (at end if no suffix)."""
		patNoSuf = r'^([^.]+)$' # matches whole line if no '.'
		
		# should match line with 1 or more periods
		patSuf = r'^(.*[^.])(\.[^.]*)$' 
		if re.match(patNoSuf, self.xpmName):
			return re.sub(patNoSuf, '\\1' + insert, self.xpmName)
		elif re.match(patSuf, self.xpmName):
			return re.sub(patSuf, '\\1' + insert + '\\2', self.xpmName)
		else:
			raise nameNotSubbedError("Can't insert '" + insert + 
				"' into name", self.xpmName)

	def objectToFile(self):
		"""Write (or rewrite) Xpm object's source data from attributes."""
		self.sourceFile = ['/* XPM */']
		self.sourceFile.append('static char *' + str(self.xpmName) + '[] = {')
		self.sourceFile.append('/* width height ncolors chars_per_pixel */')
		# Make info line:
		self.sourceFile.append('"' + str(self.width) + ' ' + 
			str(self.height) + ' ' + str(self.ncolors) + ' ' + 
			str(self.chars_per_pixel) + '",')
		self.sourceFile.append('/* colors */')
		for k in sorted(list(self.colorDefs.keys())):
			self.sourceFile.append('"' + k + ' c #' + self.colorDefs[k] + 
				'",')
		self.sourceFile.append('/* pixels */')
		for l in self.pixels:
			self.sourceFile.append('"' + ''.join(l) + '",')
		self.sourceFile.append("};")

	def print(self):
		"""Prints the source file (needs to have been created 
			 from the object.)
		"""
		for l in self.sourceFile:
			print(l)

	def getRgbLabelFromString(self, rgbString):
		for theLabel, aString in self.colorDefs.items():
			if aString == rgbString:
				return theLabel
		return False	

	def read(self, fpathi):
		"""Reads a file into a newly constructed Xpm object."""
		self.errprint("Xpm.read(): Entered")
		try:
			with open(fpathi) as fd:
				self.sourceFile = re.split(r'[\r\n]+', fd.read(), 
					flags=re.S)[:-1]
#		self.errprint("Xpm.read(): Xpm.sourceFile:", self.sourceFile)
		except OSError:
			print("Xpm.read(): Cannot open/read file '" + fpathi + "'",
				file = sys.stderr)
			exit(1)
#		self.errprint("Xpm.read(): Xpm.sourcefile:", self.sourceFile)

	def readXpmFile(self, fpathi):
		"""Has been replaced by read(); prints error message and exits."""
		print("readXpmFile(): Has been replaced by Xpm.read(); please " + 
			"convert.", file=sys.stderr)
		raise Exception

	def setQuiet(self):
		self.verbose = False

	def setVerbose(self):
		self.verbose = True

	def transpose(self):
		"""Transpose (interchange x-, y-coordinates of) Xpm object;
			return new Xpm.
		"""
		xtrpos = Xpm()
		xtrpos = self.copyXpm()
		xtrpos.fileToObject()
		xtrpos.xpmName = self.insertIntoName('-trpos')
		[xtrpos.width, xtrpos.height, xtrpos.ncolors, \
			xtrpos.chars_per_pixel] = \
			[self.height, self.width, self.ncolors, self.chars_per_pixel]
		xtrpos.colorDefs = self.colorDefs
		self.errprint("transpose(): self.pixels:", self.pixels)
		
		# transpose in 1 line (with thanks to The Python Tutorial)
		xtrpos.pixels = [[row[i] for row in self.pixels] \
			for i in range(len(self.pixels[0]))]	,
		xtrpos.objectToFile()
		return xtrpos
	
	def isValidPixelLabel(self, pixelLabel):
		return (pixelLabel in self.colorDefs.keys())

	def verifyXPM(self):	# Only verifies first line
		self.errprint("verifyXPM(): First source line is:", 
			self.sourceFile[0])
		if self.sourceFile[0] == "/* XPM */":
			self.errprint("verifyXPM(): Matched first line.")
		else:
			raise badXpmError("Line 1: " + self.sourceFile[0])

	def write(self, fpatho):
		"""Writes the source file to fpatho (file needs to have 
			 been created from the object.)
		"""
		self.errprint("Xpm.write(): Entered")
		with open(fpatho) as fd:
			for l in self.sourceFile:
				fd.write(l)

# Functions not in class Xpm:------------------------------------------
def isXpmNameLine(aLine):
	return (re.match('static', aLine) != None)

def tripletToRGBString(aTriplet):
	"""Converts triplet of integers, all ranging from 0-255, 
		 to hex string.
	"""
	hexStr = ""
	for i in range(3):
		hexStr += f'{aTriplet[i]:02X}'
	return hexStr
	
# Exceptions:----------------------------------------------------------
class badStaticNameError(Exception):
	def __init__(self, value):
		self.value = value

class badXpmError(Exception):
	def __init__(self, value):
		self.value = value

class missedParamLineError(Exception):
	def __init__(self, value):
		self.value = value

class badColorLineError(Exception):
	def __init__(self, value):
		self.value = value
		
class unknownTypeError(Exception):
	def __init__(self, value):
		self.value = value
		
class nameNotSubbedError(Exception):
	def __init__(self, value):
		self.value = value

class setKeyLabelError(Exception):
	def __init__(self, value):
		self.value = value

class badPixelLabel(Exception):
	def __init(self, value):
		self.value = value

class labelDictionaryFull(Exception):
	def __init__(self, value):
		self.value = value
