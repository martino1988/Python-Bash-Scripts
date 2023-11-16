import sys
from py_pdf_parser.loaders import load_file

if len(sys.argv) != 4:
    print("Invalid number of arguments")
    print("Syntax: python.exe pdf_parser.py [document to parse] [term to search] [name of outputdocument]")
    print("For example: python.exe pdf_parser.py presentation.pdf 'top secret' output.txt")
    sys.exit()

searchdoc = sys.argv[1]
searchtext = sys.argv[2]
new_file = sys.argv[3]

document = load_file(searchdoc)

searchterm = document.elements.filter_by_text_contains(searchtext)

information_list = []

for item in searchterm:
	page = item.page_number
	txt = item.text()
	bd = item.bounding_box
	information_list.append("\n------------\n")
	information_list.append("Seite: " + str(page) + "\n")
	information_list.append("Relevanter Text:\n\n" + str(txt))

with open (new_file, "w", newline="") as file:
    for line in information_list:
        file.write(line)
	

