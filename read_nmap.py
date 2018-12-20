import re

filename = "nmap0-test_127.0.0.1"

#ports_ssl = []
#ports_smb = []
#ports_http = []

def reader(filename):
    ports_ssl = []
    ports_smb = []
    ports_http = []
    with open(filename,'r') as nmap_out:
        line = nmap_out.readline()
        while line != "":
            pattern = r'\d{1,4}'+"/tcp"
            match = re.match(pattern,line)
            port_service = ""
            if match:
                this_line = re.sub(' +',' ',line)
                this_line = this_line.split(' ')
                port_service = this_line[2]
                if re.findall("tcpwrapped",this_line):
                    if re.findall("443|3389",this_line):
                        ports_ssl.append(int(line.split('/')[0]))
                if re.findall("ssl|443|3389",port_service):
                    ports_ssl.append(int(line.split('/')[0]))
                if re.findall("smb",port_service):
                    ports_smb.append(int(line.split('/')[0]))
                if re.findall("http",port_service):
                    ports_http.append(int(line.split('/')[0]))
            line = nmap_out.readline()
        pass
    print ("[*]reading nmap ports... done.")
    return (ports_ssl,ports_smb,ports_http)

def clear_all_lists():
    ports_ssl = []
    ports_smb = []
    ports_http = []
    pass

def output_all():
    return (ports_ssl,ports_smb,ports_http)

def output_ssl():
    return (ports_ssl)

def output_smb():
    return (ports_smb)

def output_http():
    return (ports_http)
#output()
