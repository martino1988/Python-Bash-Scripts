import os
import requests
import re
import csv



contents = []
input_file = "relevant.txt"
temp_file = "new_file.txt"

annex = input("Verfüger eingeben:")
output_file = "actrislogs_" + str(annex) + ".csv"

print("Text aus Arctis kopieren und Ctrl+C eingeben:")



# Main methode
def main():
    read()
    save()
    startnummer = extract("Detail ")
    endnummer = extract("Gefunden ") - 2
    create_relevant_file(startnummer, endnummer)
    parse_log_file(input_file, output_file)
    os.remove(temp_file)
    os.remove(input_file)

def read():
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        contents.append(line)


# speichern der daten
def save():
    
    with open (temp_file, "w", newline="") as file:
        for line in contents:
            file.write(line)
            file.write("\n")


def extract(suchwort):
    counter = 1
    linenumber = 0
    with open (temp_file, "r", newline="") as file:
        for line in file:
            if line.startswith(suchwort):
                linenumber = counter
                return linenumber
                break
            else:
                if linenumber > 0:
                    break
                else:
                    counter = counter + 1

def create_relevant_file(sn, en):
    counter = 0
    lines = []
    with open (temp_file, "r", newline="") as file:
        for line in file:
            if counter >= sn and counter < en:
                lines.append(line)
            else:
                pass
            counter += 1
    with open(input_file, "w", newline="") as f:
        for line in lines:
            f.write(line)
 
def ipinfo(ipaddr):
    # Get geo ip information
    url = f"http://ip-api.com/csv/{ipaddr}"
    response = requests.get(url)
    infoarray = response.text.split(",")
    sep = ","
    #print("lenghts: ", len(infoarray))
    return sep.join([infoarray[1], infoarray[4], infoarray[5], infoarray[10], infoarray[11], infoarray[12].replace('"', '')])

def find_public_ip(text):
    # Regular expression pattern to match an IPv4 address
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # Find all matches of IP addresses in the text
    ip_addresses = re.findall(ip_pattern, text)

    # Check each IP address if it's public
    public_ip = ""
    for ip in ip_addresses:
        if not ip.startswith('10.') and not ip.startswith('192.168.') and not ip.startswith('172.'):
            public_ip = ip

    return public_ip


def parse_log_file(input_file, output_file):
        # Write to CSV file
    with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        line = ["LdfNr","Zeitstempel","Logquelle","Aktion","Logtext 1","Logtext 2","IP-Adresse","Geo Info","Check for report"]
        writer.writerow(line)
        
    with open(input_file, 'r', encoding='latin-1') as file:
        lines = file.readlines()
        # Declaration

        
        logzeile = ""
        logzeilenliste = []

        for line in lines:
            line = line.strip()
        
            # wenn Zeile mit Datum beginnt:
            if re.match(r"\d{2}\.\d{2}\.\d{4} ", line):
                # alte Logzeile in LogzeilenListe speichern und neue logzeile anlegen
                if len(logzeile)>0:
                    logzeilenliste.append(logzeile)
                
                # neue Logzeile anlegen
                logzeile = line + "|-|-|"

            
            # ansonsten so lange anhängen bis wieder eine Zeile mit Datum beginnt:
            else:
                logzeile += " " + line
        
        #Hängt letzte logzeile an
        logzeilenliste.append(logzeile)
        
        
        counter = 1  
        ip_list = {}
        for log in logzeilenliste:
            lstamp = ""
            ltype = ""
            lsubtype = ""
            logtext2 = ""
            ipaddr = ""
            geoinfo = ""
            logtext1 = ""
            
            iline = log.replace(';',',')
            
            # Subtyp definieren:
            if "Lesen" in iline or "gelesen" in iline or "lesen" in iline:
                lsubtype = "Lesen"
            else:
                lsubtype = "Ausführen"
            
            # get Date:
            if re.match(r"\d{2}\.\d{2}\.\d{4} ", iline):
                lstamp = iline[:19]
                ltype = iline[20:24]
            else:
                lstamp = ""
                ltype = ""
                
            # get logtext 1:
            first_part = iline.split("|-|-|")[0]            
            logtext1 = first_part[25:].strip()
            
            # get logtext 2:
            second_part = iline.split("|-|-|")[1]
            logtext2 = second_part.strip()
            
            # get IP:
            if "IP: " in iline:
                ipaddr = logtext2.split("IP: ")[1].split(",")[0]
                
                if ipaddr in ip_list:
                    geoinfo = ip_list[ipaddr]
                                
                else:
                    geoinfo = ipinfo(ipaddr)
                    
                ip_list.update({ipaddr: geoinfo})
            else:
                ipaddr = ""
                geoinfo = ""
            
            line = [counter, lstamp, ltype, lsubtype, logtext1, logtext2, ipaddr, geoinfo]
        
            # Write to CSV file
            with open(output_file, mode='a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(line)
            
            counter += 1
    
main()
