import re

filename = "test"

def reader(filename):
    ports_ssl = []
    ports_smb = []
    ports_http = []
    with open(filename,'r') as nmap_out:
        line = nmap_out.readline()
        while line != "":
            pattern = r'\d{1,5}'+"/tcp"
            match = re.match(pattern,line)
            port_service = ""
            if match:
                this_line = re.sub(' +',' ',line)
                this_line = this_line.split(' ')
                port_service = this_line[2]
                if re.findall("ssl",port_service) or re.findall("443|3389",this_line[0]):
                    ports_ssl.append(int(line.split('/')[0]))
                if re.findall("smb",port_service):
                    ports_smb.append(int(line.split('/')[0]))
                if re.findall("http",port_service):
                    ports_http.append(int(line.split('/')[0]))
            line = nmap_out.readline()
        pass
    print ("[*]reading nmap ports... done.")
    return (ports_ssl,ports_smb,ports_http)
