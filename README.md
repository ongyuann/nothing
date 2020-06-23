## Pre-reqs:
This script assumes you have testssl located at `~/Desktop/tools/testssl.sh/testssl.sh`

## Implementation:
1. Make a new folder for your scans – recommended to mkdir by date for organization, e.g. *mkdir 8_Jan_2019*
2. Then prepare a list/many lists of IP addresses you want to scan.
  * a. Can prepare multiple lists: the script allows you to specify multiple lists, will scan each IP address in sequence one by one
  * b.	Keep calm and discover that you can also open a new tab and run another instance of the script: this allows you to run multiple scans simultaneously
  * c.	Just FYI: how to create list: *vi targets_list_1* , then just copy and paste the IP addresses in, separated by newline
  * d.	You can also prepare lists from windows, just make sure the IP addresses are separated by newline
3. Type: _git clone https://github.com/oya10/nothing_ (if this doesn't work, browse to the same URL, download the damn thing, and put it in the same directory)
4. Copy out the contents: _cp nothing/* ._ (including the full-stop!) (if you downloaded nothing manually, the thing would be called _nothing-master_).

## Usage:
1. Run the main script, caller.py: _python3 caller.py_
2. The script should be asking you to enter the filenames of the lists. Just enter, can separate by comma/space, e.g. *list1, list2*
3. Enter no. of minutes you want to script to wait. If scan now, just skip
4. **If you want to scan just the top 1000 ports, enter “yes”.** If All Port scan (which you should do by default), just skip
5. Choose between UDP, TCP, both, honey, tea, or me. no just choose first 3 (instructions will be shown anyway). if scan both, just skip
6. Hit another enter, and wait for the results – results will be stored in folders named in this way: _list1_results_udp_ , _list2_results_tcp_ , etc …

## Disclaimer:
This script takes no responsibilities for whatever happens when you use it.

## Targeted features
- ~~timer for delayed scan~~
- improved progress tracking mechanism
- rdp encryption check
- http methods check
- snmp check
- secure renegotiation check
