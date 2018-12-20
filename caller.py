#!/bin/python

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
print("\nPlease enter time delay till scan starts (in minutes)")
try:
    wait = int(raw_input("time in mins: "))
except:
    wait = 0
wait = wait*60
print("\nScan all ports? if 'yes', we go, if no, skip")
try:
    nmap_allports = str(raw_input("decision: "))
except:
    nmap_allports = False

lists = lists.split(',')

'''
file organization / main calling
'''
def check_files(each_list_of_files):
    try:
        file = open(each_list_of_files,'r')
        return True
    except:
        print (each_list_of_files + " not found. quitting.")

def action_on_files(list_of_files):
    for each_list in list_of_files:
        if not check_files(each_list):
            break
        action_on_list(each_list)

def action_on_list(curr_list):
    curr_list=curr_list.rstrip()
    border = "\n****************************************************************************************"
    with open(curr_list,'r') as list_of_focus:
        ip_add = list_of_focus.readline()
        while ip_add != "":
            print (border)
            border_content = "** current list: " + curr_list + " , ip: "+ip_add.rstrip()
            border_content += " "*(len(border)-len(border_content)-3)
            border_content += "**"
            print (border_content)
            print ("****************************************************************************************")
            run_nmap_tcp(ip_add,curr_list)
            ip_add = list_of_focus.readline()
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

'''
script 'runners' below
'''
def run_nmap_tcp(ip_add_of_focus,curr_list):
    #print(ip_add_of_focus)
    ip_add_of_focus = ip_add_of_focus.rstrip()
    name_of_output = curr_list+"_nmap_tcp_"+ip_add_of_focus
    name_of_output = name_of_output.rstrip()
    cmd = "nmap -v -sS -sC -sV -T4 --max-rtt 300ms --max-retries 3 "
    if nmap_allports:
        cmd += "-p- "
    cmd += ip_add_of_focus
    print ("[*]running nmap ...")
    run_command(cmd,name_of_output)
    list_of_ssl_ports = rn.reader(name_of_output)[0]
    #list_of_ssl_ports = rn.output_ssl()
    #print ("[*]BREAK")
    #print (list_of_ssl_ports)
    #sys.exit()
    run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list)
    run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list)
    pass

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

'''
final actions
'''
time.sleep(wait)
action_on_files(lists)

#rn.reader("nmap0-test_127.0.0.1")
#rn.output()
