import subprocess
import time
print "\nEnter the text file consist of the IP Address List (if more than 1 list, please separate by ,)"
ipAddressList = str(raw_input('list: '))
print "\nPlease enter the name of the file (if more than 1 list, please separate by ,)"
AllFile = str(raw_input('file: '))
print "\nPlease enter time)"
wait = int(raw_input('time in mins: '))
ipAddress = ipAddressList.split(",")
File = AllFile.split(",")
wait = wait * 60
i = 0
def Scanning(sIP,sFile):

	NMAP = "for ip_address in $(cat "+sIP+");do nmap -v -sS -sV -sC -oN  nmap0-"+sFile+"_$ip_address $ip_address;done"
	SSL = "for ip_address in $(cat "+sIP+");do /root/Desktop/tools/scripts/testssl.sh/testssl.sh $ip_address > "+sFile+"ssl_$ip_address;done"
	SSLScan = "for ip_address in $(cat "+sIP+");do sslscan $ip_address > "+sFile+"scanssl_$ip_address;done"
	subprocess.call(NMAP+"; "+SSL+";"+SSLScan ,shell=True)


for x in ipAddress :
		Scanning(x,File[i])
        #print x+". File name is "+File[i]
        i = i+1
        time.sleep(wait)
		wait = wait + wait
else:
	print "Finish Testing"
