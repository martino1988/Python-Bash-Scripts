import sys
import re
from py_pdf_parser.loaders import load_file

def start():
    document = load_file('Servicekatalog.pdf')
    elms = document.elements

    information_list = []
    regex = "^[A-Z]{%d}[0-9]{3}" % 1
    regex1 = "^nicht geschäftskritisch"
    regex2 = "^geschäftskritisch"
    appendstring = ""

    for item in elms:
        txt = item.text()
        match = re.findall(regex, txt)
        match1 = re.findall(regex1, txt)
        match2 = re.findall(regex2, txt)
        if match:
            appendstring = txt
        if match1:
            appendstring += ";nicht geschäftskritisch"
            information_list.append(appendstring)
            appendstring = ""

        if match2:
            appendstring += ";geschäftskritisch"
            information_list.append(appendstring)
            appendstring = ""

    new_list = []
    for info in information_list:
        if " - " in info:
            new_string = "".join(info.splitlines())
            no_minus = new_string.replace(" - ", ";", 1)
            new_list.append(no_minus)

    with open("Services.csv", "w", newline="") as file:
       for e in new_list:
           file.write(e)
           file.write("\n")



if len(sys.argv) != 1:
    print("Invalid number of arguments")
    print("Syntax: python.exe pdf_parser.py ")
    print("For example: python.exe pdf_parser.py")
    sys.exit()
else:
    start()

