#!usr/bin/python3
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
lists = input("list: ")
print("\nPlease enter time delay till scan starts (in minutes) - if immediate, skip")
try:
    wait = input("time in mins: ")
    wait = int(wait)
except:
    wait = 0
wait = wait*60
print("\nScan [1]1000 ports or [2]All Ports?\n[*]if 1000, type '1', if All Ports, type '2' [default=1000 ports]")
try:
    nmap_1000ports = input("decision: ")
    if re.findall("2",nmap_1000ports):
        nmap_1000ports = False
    else:
        nmap_1000ports = True
except:
    nmap_1000ports = True
print("\n[1]TCP [2]UDP [3]both? [**WARNING: BOTH TAKES FOREVER**]\n[*]if TCP, type '1' or 'tcp', if UDP, type '2' or 'udp', if both, type '3' or 'both'. [default=TCP]")
try:
    nmap_option = input("option: ")
    if re.findall("1|tcp",nmap_option):
        nmap_option = "tcp"
    elif re.findall("2|udp",nmap_option):
        nmap_option = "udp"
    elif re.findall("3",nmap_option):
        nmap_option = "both"
    else:
        nmap_option = "tcp"
except:
    nmap_option = "tcp"
print("\nChoose if you want [1]with colour or [2]no colour for sslscan / testssl scans\n[*][default=with colour]")
try:
    want_colour = input("option: ")
    if re.findall("2",want_colour):
        want_colour = False
    else:
        want_colour = True
except:
    want_colour = True
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
        no_of_lines_in_all_files = str(subprocess.check_output(check_output_cmd,encoding='UTF-8')).split(' ')[-2]
    except:
        print ("[*]you sure the files exist / are entered correctly? quitting.")
    
    for each_list in list_of_files:
        if not check_files(each_list):
            break
        action_on_list(each_list,no_of_lines_in_all_files)

def action_on_list(curr_list,no_of_lines_in_all_files):
    curr_list=curr_list.rstrip()
    folder_name=curr_list+'_results'
    options = ["_tcp","_udp"]
    if nmap_option == 'both':
        pass
    if nmap_option == 'udp':
        options.pop(0)
    if nmap_option == 'tcp':
        options.pop(1)
    for option in options:
        folder_name += option
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        else:
            if os.path.exists(folder_name+".old"):
                os.system('rm -r '+folder_name+'.old')
            os.system('mv '+folder_name+' '+folder_name+'.old')
            os.makedirs(folder_name)
        border = "\n****************************************************************************************"
        with open(curr_list,'r') as list_of_focus:
            no_of_lines_in_file = str(subprocess.check_output(['wc','-l',curr_list],encoding='UTF-8')).split(' ')[0]
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
    process = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='UTF-8')
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
    if not nmap_1000ports:
        cmd += "-p- "
    if nmap_option == "both":
        cmd_tcp = cmd + "-sS " + ip_add_of_focus
        name_of_output_tcp = name_of_output + "_tcp_" + ip_add_of_focus + ".txt"
        cmd_tcp += " -oN " + name_of_output_tcp + "_backup.txt"
        cmd_udp = cmd + "-sU " + ip_add_of_focus
        name_of_output_udp = name_of_output + "_udp_" + ip_add_of_focus + ".txt"
        cmd_udp += " -oN " + name_of_output_udp + "_backup.txt"
        print ("[*]running nmap tcp ...")
        run_command(cmd_tcp,name_of_output_tcp)
        list_of_ssl_ports = rn.reader(name_of_output_tcp)[0]
        run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name)
        run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name)
        print ("[*]running nmap udp ...")
        run_command(cmd_udp,name_of_output_udp)
        pass
    else:
        if nmap_option == "udp":
            cmd += "-sU "
            name_of_output += "_udp_"
            #cmd += "-oN " + name_of_output + "_backup.txt "
        elif nmap_option == "tcp":
            cmd += "-sS "
            name_of_output += "_tcp_"
            #cmd += "-oN " + name_of_output + "_backup.txt "
        name_of_output += ip_add_of_focus + ".txt"
        cmd += ip_add_of_focus
        cmd += " -oN " + name_of_output + "_backup.txt"
        print ("[*]running nmap "+nmap_option+" ...")
        run_command(cmd,name_of_output)
        list_of_ssl_ports = rn.reader(name_of_output)[0]
        if nmap_option == "udp":
               pass
        else:
            run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name)
            run_testssl(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name)
    pass

def run_sslscan(ip_add_of_focus,list_of_ssl_ports,curr_list,folder_name):
    ip_add_of_focus = ip_add_of_focus.rstrip()
    for ssl_port in list_of_ssl_ports:
        print ("[*]running sslscan on " + ip_add_of_focus + " on port " + str(ssl_port))
        #ssl --no-colour
        if want_colour:
            cmd = "sslscan "+ip_add_of_focus+":"
        else:
            cmd = "sslscan --no-colour "+ip_add_of_focus+":"
        cmd += str(ssl_port)
        name_of_output = folder_name+"/"+curr_list+"_sslscan_"+ip_add_of_focus+"-"+str(ssl_port)+".txt"
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
        # --color 0
        print ("[*]running testssl on " + ip_add_of_focus + " on port " + str(ssl_port))
        if want_colour:
            cmd = "/home/kali/Desktop/tools/testssl.sh/testssl.sh " +ip_add_of_focus+":"
        else:
            cmd = "/home/kali/Desktop/tools/testssl.sh/testssl.sh --color 0 " +ip_add_of_focus+":"
        cmd += str(ssl_port)
        name_of_output = folder_name+"/"+curr_list+"_testssl_"+ip_add_of_focus+"-"+str(ssl_port)+".txt"
        run_command(cmd,name_of_output)
    pass

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print("[*]scan starts now.")

'''
final actions
'''
#time.sleep(wait)
countdown(wait)
action_on_files(lists)
