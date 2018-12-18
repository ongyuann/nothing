#!/bin/python

import os,time
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
wait = int(raw_input("time in mins: "))
wait = wait*60

lists = lists.split(',')

'''
file organization / main calling
'''
def check_files(each_list_of_files):
    try:
        file = open(each_list_of_files,'r')
        return True
    except FileNotFoundError:
        print (each_list_of_files + " not found. quitting.")

def action_on_files(list_of_files):
    for each_list in list_of_files:
        if not check_files(each_list):
            break
        action_on_list(each_list)

def action_on_list(curr_list):
    curr_list=curr_list.rstrip()
    with open(curr_list,'r') as list_of_focus:
        ip_add = list_of_focus.readline()
        while ip_add != "":
            #print (ip_add)
            run_nmap_tcp(ip_add,curr_list)
            ip_add = list_of_focus.readline()
    pass

'''
script 'runners' below
'''
def run_nmap_tcp(ip_add_of_focus,curr_list):
    #print(ip_add_of_focus)
    ip_add_of_focus = ip_add_of_focus.rstrip()
    nmap_output = curr_list+"_nmap_tcp_"+ip_add_of_focus
    nmap_output = nmap_output.rstrip()
    nmap_cmd = "nmap -sS -sV -oN "+nmap_output+" "+ip_add_of_focus
    print ("running nmap ...")
    os.system(nmap_cmd)
    rn.reader(nmap_output)
    list_of_ssl_ports = rn.output_ssl()
    print (list_of_ssl_ports)
    run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list)
    run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list)
    pass

def run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list):
    #print("hello")
    #print(ip_add_of_focus)
    #print(list_of_ssl_ports)
    ip_add_of_focus = ip_add_of_focus.rstrip()
    cmd = "sslscan " +ip_add_of_focus+":"
    for ssl_port in list_of_ssl_ports:
        print ("running sslscan on " + ip_add_of_focus + " on port " + str(ssl_port))
        cmd += ssl_port
        cmd += " > "+curr_list+"_sslscan_"+ip_add_of_focus
        os.system(cmd)
    pass

def run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list):
    #print("hello testssl here")
    ip_add_of_focus = ip_add_of_focus.rstrip()
    cmd = "/root/Desktop/tools/scripts/testssl.sh/testssl.sh " +ip_add_of_focus+":"
    for ssl_port in list_of_ssl_ports:
        print ("running testssl on " + ip_add_of_focus + " on port " + str(ssl_port))
        cmd += ssl_port
        cmd += " > "+curr_list+"_testssl_"+ip_add_of_focus
        os.system(cmd)
    pass

'''
final actions
'''
time.sleep(wait)
action_on_files(lists)

#rn.reader("nmap0-test_127.0.0.1")
#rn.output()
