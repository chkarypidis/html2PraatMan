from bs4 import BeautifulSoup
import string, os

############################################
############################################
def doubleQuotes(s, number=1):
	""" ............."""
	return "\""*number + s + "\""*number
############################################
############################################
############################################
############################################
def bold(s):
	return "##" + s + "#"
############################################
############################################
def italics(s):
	# listWords = string.split(s)
	# if len(listWords) == 1:
	# 	return "%%" + listWords[0] + "%"
	# else:
	# 	for x in range(0,len(listWords)):
	# 		listWords[x] = "%%" + listWords[x]
	# 	return string.join(listWords)
	return "%%" + s + "%"
############################################
############################################
def monospace(s):
	return "$$" + s + "$"
############################################
############################################
def subscript(s):
	return "__" + s + "_"
############################################
############################################
def superscript(s):
	return "^^" + s + "^"
############################################
############################################
def link(s):
	target = s['href']
	filenameOnly = target.split('.')[0]
	extension = target.split('.')[1]
	linkText = s.string
	audioExtension = ['wav', 'aiff', 'aifc', 'au', 'nist', 'flac', 'mp3']
	if extension == "man":
		return "@@" + filenameOnly + "|" + linkText + "@"
	elif extension == "praat":
		if s['alt']:
			args = string.split(s['alt'], "|")
			for x in range(0,len(args)):
				args[x] = doubleQuotes(args[x],2)
			argsStr = string.join(args, " ")
			return "@@\\SC" + doubleQuotes(target,2) + " " + argsStr + " " + "|" + linkText + "@"
		else:
			return "@@\\SC" + doubleQuotes(target,2) + " " + "|" + linkText + "@"
	elif extension in audioExtension:
		return "@@\\FI" + target + " " + "|" + linkText + "@"
############################################
############################################
allFiles = []
htmlList = []

for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
	allFiles.extend(filenames)

for x in range(0,len(allFiles)-1):
	if allFiles[x].endswith("html",len(allFiles[x])-4):
		htmlList.append(allFiles[x])

for inputFilename in htmlList:
	input = BeautifulSoup(open(inputFilename))

	address = input.address.string
	addressCleaned = address.strip()
	addressComps = addressCleaned.split('\n')

	intro = input.cite.string

	if len(addressComps) == 3:
		recordTime = addressComps[2]
	else:
		recordTime = '0'

	intro = input.cite.string

#####################################
	outputFilename = inputFilename.split('.')[0] + ".man"
	output = open(outputFilename,"w")
###########################

	output.write("ManPagesTextFile\n")
	output.write(doubleQuotes(inputFilename.split('.')[0].capitalize()) + " " + doubleQuotes(addressComps[0]) + " " + addressComps[1] + " " + addressComps[2] + '\n')

	for child in input.body:
		if child.name is not None:
			if child.name == "cite":
				listChildren = []
				for x in child:
					if x.name == "b":
						temp = bold(x.string)
						listChildren.append(temp)
					elif x.name == "a":
						temp = link(x)
						listChildren.append(temp)
					elif x.name == "i":
						temp = italics(x.string)
						listChildren.append(temp)
					elif x.name == "kbd":
						temp = monospace(x.string)
						listChildren.append(temp)
					elif x.name == "sub":
						temp = subscript(x.string)
						listChildren.append(temp)
					elif x.name == "sup":
						temp = superscript(x.string)
						listChildren.append(temp)
					else:
						listChildren.append(str(x))
				output.write("<intro> " + doubleQuotes(string.join(listChildren, '')) + '\n')
			elif child.name == "h1":
				listChildren = []
				for x in child:
					if x.name == "b":
						temp = bold(x.string)
						listChildren.append(temp)
					elif x.name == "a":
						temp = link(x)
						listChildren.append(temp)
					elif x.name == "i":
						temp = italics(x.string)
						listChildren.append(temp)
					elif x.name == "kbd":
						temp = monospace(x.string)
						listChildren.append(temp)
					elif x.name == "sub":
						temp = subscript(x.string)
						listChildren.append(temp)
					elif x.name == "sup":
						temp = superscript(x.string)
						listChildren.append(temp)
					else:
						listChildren.append(str(x))
				output.write("<entry> " + doubleQuotes(string.join(listChildren, '')) + '\n')
			elif child.name == "blockquote":
				output.write("<definition> " + doubleQuotes(child.string) + '\n')
			elif child.name == "p":
				listChildren = []
				for x in child:
					if x.name == "b":
						temp = bold(x.string)
						listChildren.append(temp)
					elif x.name == "a":
						temp = link(x)
						listChildren.append(temp)
					elif x.name == "i":
						temp = italics(x.string)
						listChildren.append(temp)
					elif x.name == "kbd":
						temp = monospace(x.string)
						listChildren.append(temp)
					elif x.name == "sub":
						temp = subscript(x.string)
						listChildren.append(temp)
					elif x.name == "sup":
						temp = superscript(x.string)
						listChildren.append(temp)
					else:
						listChildren.append(str(x))
				output.write("<normal> " + doubleQuotes(string.join(listChildren, '')) + '\n')
			elif child.name == "address":
				continue
			elif child.name == "ul":
				if child.get('class') == ["noBullet"]:
				# if child.get('class'):
					for item in child.find_all("li"):
						listChildren = []
						for x in item:
							if x.name == "b":
								temp = bold(x.string)
								listChildren.append(temp)
							elif x.name == "a":
								temp = link(x)
								listChildren.append(temp)
							elif x.name == "i":
								temp = italics(x.string)
								listChildren.append(temp)
							elif x.name == "kbd":
								temp = monospace(x.string)
								listChildren.append(temp)
							elif x.name == "sub":
								temp = subscript(x.string)
								listChildren.append(temp)
							elif x.name == "sup":
								temp = superscript(x.string)
								listChildren.append(temp)
							else:
								listChildren.append(str(x))
						output.write("<list_item> " + "\"" + string.join(listChildren, '') + "\"" + '\n')
				else:
					for item in child.find_all("li"):
						listChildren = []
						for x in item:
							if x.name == "b":
								temp = bold(x.string)
								listChildren.append(temp)
							elif x.name == "a":
								temp = link(x)
								listChildren.append(temp)
							elif x.name == "i":
								temp = italics(x.string)
								listChildren.append(temp)
							elif x.name == "kbd":
								temp = monospace(x.string)
								listChildren.append(temp)
							elif x.name == "sub":
								temp = subscript(x.string)
								listChildren.append(temp)
							elif x.name == "sup":
								temp = superscript(x.string)
								listChildren.append(temp)
							else:
								listChildren.append(str(x))
						output.write("<list_item> \"\\bu " + string.join(listChildren, '') + "\"" + '\n')
			elif child.name == "code":
				width = child.get('width')
				height = child.get('height')
				output.write("<script> " + width + " " + height + " " + doubleQuotes(child.string) + '\n')
			else:
				continue

	output.close()