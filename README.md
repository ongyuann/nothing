# nothing is now run by Python 3 thanks to the useless worker
Instructions:\
First make sure you’re using our Kali with the testssl stored at ~/Desktop/tools/scripts/testssl.sh/testssl.sh\
(Otherwise the script cannot find testssl)\
\
Recommended way to use:
1. Mkdir a folder for your scans – recommended to mkdir by date for organization, e.g. *mkdir 8_Jan_2019*
2. Prepare a list/many lists of IP addresses you want to scan.
  * a. You can prepare multiple lists: the script allows you to specify multiple lists, will scan each IP address in sequence one by one
  * b.	You can also open a new tab and run another instance of the script: this allows you to run multiple scans simultaneously
  * c.	Example of how to create list: *vi targets_list_1* , then just copy and paste the IP addresses in, separated by newline
  * d.	Can also prepare lists from windows, just make sure the IP addresses are separated by newline
3. Type: _git clone https://github.com/oya10/nothing_ (if this doesn't work, browse to the same URL, download the damn thing, and put it in the same directory)
4. Copy out the contents: _cp nothing/* ._ (including the full-stop!) (also, if you downloaded nothing manually, the thing would be called _nothing-master_ , so adapt, beeeeatch).
5. Run the main script, caller.py: _python caller.py_
6. The script should now ask you to enter the filenames of the lists. Just enter, can separate by comma/space, e.g. *list1, list2*
7. If you want to delay the scan, enter no. of minutes you want to script to wait. If scan now, just skip
8. **If you want to scan just the top 1000 ports, enter “yes”.** If All Port scan (which you should do by default), just skip
9. Choose between UDP, TCP, both, honey, tea, or me. no just choose first 3 (instructions will be shown anyway). if scan both, just skip
10. Then hit another enter, and wait for the results – results will be stored in folders named in this way: _list1_results_udp_ , _list2_results_tcp_ , etc …

**Have fun**
