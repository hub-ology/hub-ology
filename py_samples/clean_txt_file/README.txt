shopcards_cleaner is a simple script to modify text files
to be in the proper format for uploading to another system

Main Features:
* opens a directory and finds all of the text files within that directory
* splits each line and checks to see if the fourth element is empty, and if so, removes the line
* removes the last line feed character from the last line in the file
* writes the changed file back to the original file name