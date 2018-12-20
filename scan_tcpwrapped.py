'''
to find tcpwrapped ports (do this in directory with all nmap results):
for file in $(ls | grep nmap_tcp);do echo $file | cut -d "_" -f 6;cat $file | grep tcpwrapped | grep -E '443|3389' | cut -d "/" -f 1;done > tcpwrapped_ssl_ports
'''

import os,sys,time,subprocess,shlex,re
#from caller import run_sslscan,run_testssl

filename = 'tcpwrapped_ssl_ports' #change filename to your list of tcpwrapped ports

def reader(filename):
    ip_add_pattern = '\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'
    with open(filename,'r') as list_raw:
        curr_line = list_raw.readline().rstrip()
        curr_ip = ""
        while curr_line != "":
            if re.match(ip_add_pattern,curr_line):
                #print (curr_line)
                curr_ip = curr_line.rstrip()
            else:
                #print (curr_ip+':'+curr_line)
                #print (curr_line)
                run_sslscan(curr_ip,[curr_line],"tcpwrapped_windows_p3_CNC")
                run_testssl(curr_ip,[curr_line],"tcpwrapped_windows_pc_CNC")
            curr_line = list_raw.readline()

def run_command(command,name_of_output):
    process = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        output_file = open(name_of_output,'r')
        os.system('mv '+name_of_output+' '+name_of_output+'.old')
        output_file.close()
    except:
        os.system('touch '+name_of_output)
    while 1:
        shell_output = process.stdout.readline().rstrip()
        if re.findall('nmap|testssl',command) and shell_output == "" and process.poll() is not None:
            break
        if shell_output != "":
            print (shell_output)
            os.system('echo "'+shell_output+'" >> '+name_of_output)
            if re.findall("testssl",command) and re.findall("doesn't seem to be a",shell_output):
                process.stdin.write("yes")
                process.stdin.close()
    try:
        rc = process.communicate()
    except:
        rc = process.poll()
    #rc = process.poll()
    return rc

def run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list):
    ip_add_of_focus = ip_add_of_focus.rstrip()
    for ssl_port in list_of_ssl_ports:
        print ("[*]running sslscan on " + ip_add_of_focus + " on port " + str(ssl_port))
        cmd = "sslscan "+ip_add_of_focus+":"
        cmd += str(ssl_port)
        name_of_output = curr_list+"_sslscan_"+ip_add_of_focus+":"+str(ssl_port)
        #run_command(cmd,name_of_output)
        try:
            output_file = open(name_of_output,'r')
            os.system('mv '+name_of_output+' '+name_of_output+'.old')
            output_file.close()
        except:
            os.system('touch '+name_of_output)
        os.system(cmd+" >> "+name_of_output)
    pass

def run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list):
    ip_add_of_focus = ip_add_of_focus.rstrip()
    for ssl_port in list_of_ssl_ports:
        print ("[*]running testssl on " + ip_add_of_focus + " on port " + str(ssl_port))
        cmd = "/root/Desktop/tools/scripts/testssl.sh/testssl.sh " +ip_add_of_focus+":"
        cmd += str(ssl_port)
        name_of_output = curr_list+"_testssl_"+ip_add_of_focus+":"+str(ssl_port)
        run_command(cmd,name_of_output)
    pass


reader(filename)
