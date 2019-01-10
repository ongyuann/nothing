# nothing now runs on Python 3 thanks to ma man the self-declared useless worker
Instructions:\
First make sure you’re using our Kali with the testssl stored at ~/Desktop/tools/scripts/testssl.sh/testssl.sh\
(Otherwise the script cannot find testssl) (but if you think you can adapt the script to work testssl anyhow anyway, you're welcome to do so yourself, bij)\
\
Recommended way to use:
1. Folder first. Make a new folder for your scans – recommended to mkdir by date for organization, e.g. *mkdir 8_Jan_2019*
2. U then prepare a list/many lists of IP addresses you want to scan.
  * a. Can prepare multiple lists: the script allows you to specify multiple lists, will scan each IP address in sequence one by one
  * b.	Keep calm and discover that you can also open a new tab and run another instance of the script: this allows you to run multiple scans simultaneously
  * c.	Just FYI: how to create list: *vi targets_list_1* , then just copy and paste the IP addresses in, separated by newline
  * d.	Eu can also prepare lists from windows, just make sure the IP addresses are separated by newline
3. Rekt yet? Type: _git clone https://github.com/oya10/nothing_ (if this doesn't work, browse to the same URL, download the damn thing, and put it in the same directory)
4. Eh? Not working yet? Cos you gotta copy out the contents first you little byayayach: _cp nothing/* ._ (including the full-stop!) (if you downloaded nothing manually, the thing would be called _nothing-master_ , so adapt, beeeeeatch).
5. Me hombre, now run the main script, caller.py: _python3 caller.py_
6. Yes, now the script should be asking you to enter the filenames of the lists. Just enter, can separate by comma/space, e.g. *list1, list2*
7. Look if you want to delay the scan, enter no. of minutes you want to script to wait. If scan now, just skip
8. **If you want to scan just the top 1000 ports, enter “yes”.** If All Port scan (which you should do by default), just skip
9. My friend, now you choose between UDP, TCP, both, honey, tea, or me. no just choose first 3 (instructions will be shown anyway). if scan both, just skip
10. Then hit another enter, and wait for the results – results will be stored in folders named in this way: _list1_results_udp_ , _list2_results_tcp_ , etc …
11. Zonks wubba lub dub, peace out.

**Have fun**

no biatches were harmed in the making of this readme. only @5sh073s.

# changelog
ver 133.7 : please just use this latest version you mangy parrot.
