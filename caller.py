#!/bin/python
'''
important: replacing file names with ":" with "-" so they can be read in windows:
for file in $(ls | grep ":");do mv -- "$file" "${file//:/-}";done
'''
import os,sys,time,subprocess,shlex,re
import read_nmap as rn
'''
setting up
'''
print("****************************************************************************************")
print("** Please first ensure text files that contain IP addresses are in the same directory **")
print("****************************************************************************************")
print("\nEnter the text files that contains the IP addresses (if more than 1 list, please separate by comma, e.g. list1,list2)")
lists = str(raw_input("list: "))
print("\nPlease enter time delay till scan starts (in minutes) - if no, skip")
try:
    wait = int(raw_input("time in mins: "))
except:
    wait = 0
wait = wait*60
print("\nScan 1000 ports only? if 'yes', we go, if All Ports, skip")
try:
    nmap_1000ports = str(raw_input("decision: "))
except:
    nmap_1000ports = False
print("\nUDP or TCP? if UDP, type 'yes', if TCP, skip")
try:
    nmap_udp = str(raw_input("protocol: "))
    if "udp" in nmap_udp or "yes" in nmap_udp:
        nmap_udp = True
    else:
        nmap_udp = False
except:
    nmap_udp = False
print("\nOK no more questions\n") 

lists = lists.replace(" ","").split(',')

'''
file organization / main calling
'''
def check_files(each_list_of_files):
    try:
        file = open(each_list_of_files,'r')
        return True
    except:
        print ("[*]"+each_list_of_files + " not found. quitting.")

def action_on_files(list_of_files):
    check_output_cmd = ['wc','-l']
    no_of_lines_in_all_files = 0
    try:
        for each_list in list_of_files:
            check_output_cmd.append(each_list.rstrip())
        no_of_lines_in_all_files = str(subprocess.check_output(check_output_cmd)).split(' ')[-2]
    except:
        print ("[*]you sure the files exist / are entered correctly? quitting.")
    
    for each_list in list_of_files:
        if not check_files(each_list):
            break
        action_on_list(each_list,no_of_lines_in_all_files)

def action_on_list(curr_list,no_of_lines_in_all_files):
    curr_list=curr_list.rstrip()
    folder_name=curr_list+'_results'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    else:
        os.system('mv '+folder_name+' '+folder_name+'.old')
        os.makedirs(folder_name)
    border = "\n****************************************************************************************"
    with open(curr_list,'r') as list_of_focus:
        no_of_lines_in_file = str(subprocess.check_output(['wc','-l',curr_list])).split(' ')[0]
        count = 1
        ip_add = list_of_focus.readline().rstrip()
        while ip_add != "":
            print (border)
            border_content = "** current list: " + curr_list + " , ip: "+ip_add.rstrip()
            count_tracker = str(count) + "/" + str(no_of_lines_in_file) + "/" + str(no_of_lines_in_all_files)
            border_content += " "*(len(border)-len(border_content)-3-len(count_tracker)-1)
            border_content += count_tracker
            border_content += " **"
            print (border_content)
            print ("****************************************************************************************")
            run_nmap_tcp(ip_add,curr_list,folder_name)
            count += 1
            ip_add = list_of_focus.readline().rstrip()
    pass

'''
special runner + writer function
'''
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
        if shell_output == "" and process.poll() is not None:
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
    return rc

'''
script 'runners' below
'''
def run_nmap_tcp(ip_add_of_focus,curr_list,folder_name):
    ip_add_of_focus = ip_add_of_focus.rstrip()
    name_of_output = folder_name+"/"+curr_list+"_nmap"
    name_of_output = name_of_output.rstrip()
    cmd = "nmap -v -sC -sV -T4 --max-rtt 300ms --max-retries 3 "
    if nmap_udp:
        cmd += "-sU "
        name_of_output += "_udp_"
    else:
        cmd += "-sS "
        name_of_output += "_tcp_"
    if not nmap_1000ports:
        cmd += "-p- "
    name_of_output += ip_add_of_focus
    cmd += ip_add_of_focus
    print ("[*]running nmap ...")
    run_command(cmd,name_of_output)
    list_of_ssl_ports = rn.reader(name_of_output)[0]
    run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name)
    run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name)
    pass

def run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name):
    ip_add_of_focus = ip_add_of_focus.rstrip()
    for ssl_port in list_of_ssl_ports:
        print ("[*]running sslscan on " + ip_add_of_focus + " on port " + str(ssl_port))
        cmd = "sslscan "+ip_add_of_focus+":"
        cmd += str(ssl_port)
        name_of_output = folder_name+"/"+curr_list+"_sslscan_"+ip_add_of_focus+"-"+str(ssl_port)
        #run_command(cmd,name_of_output)
        try:
            output_file = open(name_of_output,'r')
            os.system('mv '+name_of_output+' '+name_of_output+'.old')
            output_file.close()
        except:
            os.system('touch '+name_of_output)
        os.system(cmd+" >> "+name_of_output)
    pass

def run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name):
    ip_add_of_focus = ip_add_of_focus.rstrip()
    for ssl_port in list_of_ssl_ports:
        print ("[*]running testssl on " + ip_add_of_focus + " on port " + str(ssl_port))
        cmd = "/root/Desktop/tools/scripts/testssl.sh/testssl.sh " +ip_add_of_focus+":"
        cmd += str(ssl_port)
        name_of_output = folder_name+"/"+curr_list+"_testssl_"+ip_add_of_focus+"-"+str(ssl_port)
        run_command(cmd,name_of_output)
    pass

'''
final actions
'''
time.sleep(wait)
action_on_files(lists)
