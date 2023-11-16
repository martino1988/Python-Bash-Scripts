import sys

print("NOTE: document_parser is only tested with .txt and .csv files\nPlease note that the search is case sensitive")
if len(sys.argv) != 4:
    print("Invalid number of arguments")
    print("Syntax: python.exe pdf_parser.py [document to parse] [term to search] [name of outputdocument]")
    print("For example: python.exe pdf_parser.py presentation.pdf 'top secret' output.txt")
    sys.exit()
    

dok = sys.argv[1]
param = sys.argv[2]
new_file = sys.argv[3]
lines = []

with open(dok, 'r', newline="") as file:
    for line in file:
        if param in line:
            lines.append(line)
            
with open (new_file, "w", newline="") as file:
    for line in lines:
        file.write(line)
