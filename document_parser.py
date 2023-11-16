print("NOTE: document_parser is only tested with .txt and .csv files\n")

dok = input('Dateiname eingeben: ')
param = input('Suchparameter eingeben: ')
new_file = input('Zieldatei definieren: ')
lines = []

with open(dok, 'r', newline="") as file:
    for line in file:
        if param in line:
            lines.append(line)
            
with open (new_file, "w", newline="") as file:
    for line in lines:
        file.write(line)
            
