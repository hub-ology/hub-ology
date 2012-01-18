import os

path = "//tcsdc2/PROJECTS/Issued"
extension = ".txt"

# Get all of the files that we need to check
list_of_files = [file for file in os.listdir(path) if file.lower().endswith(extension)]
for file2 in list_of_files:
	# Open the file
	shopcard = open(path + "/" + file2, "r+")
	# Read in all of the lines
	lines = shopcard.readlines()
	# Remove any lines that don't have a part number on them
	to_remove = []
	for line in lines:
		items = line.split(",")
		if cmp(items[3], "") == 0:
			to_remove.append(line)

	for line2 in to_remove:
		lines.remove(line2)

	# remove the last \n if one exists
	lines.reverse()
	lines[0] = lines[0].rstrip('\r\n')
	lines.reverse()

	# Write the modified lines back to the text file
	shopcard.seek(0)
	shopcard.truncate()
	shopcard.writelines(lines)
	shopcard.close
