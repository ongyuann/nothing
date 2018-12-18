import re

filename = "nmap0-test_127.0.0.1"

ports_ssl = []
ports_smb = []
ports_http = []

def reader(filename):
    with open(filename,'r') as nmap_out:
        line = nmap_out.readline()
        while line != "":
            pattern = r'\d{1,4}'+"/tcp"
            match = re.match(pattern,line)
            port_service = ""
            if match:
                this_line = line.split(' ')
                port_service = this_line[3]
                if re.findall("ssl",port_service):
                    ports_ssl.append(int(line.split('/')[0]))
                if re.findall("smb",port_service):
                    ports_smb.append(int(line.split('/')[0]))
                if re.findall("http",port_service):
                    ports_http.append(int(line.split('/')[0]))
#               print (this_line[3]) //service information in 4th element
#               for i in this_line:
#                   print (i)
            line = nmap_out.readline()
        pass
#    print (ports_ssl)
#    print (ports_smb)
#    print (ports_http)
    print ("reading nmap ports... done.")

def output_all():
    return (ports_ssl,ports_smb,ports_http)

def output_ssl():
    return (ports_ssl)

def output_smb():
    return (ports_smb)

def output_http():
    return (ports_http)
#output()
