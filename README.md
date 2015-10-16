# Python_Admin
Administrative tasks.

The python programs in this branch are just for proving my programming skills in python.
You can modify it at will and redistribute it.

check_passwd.py:

You will need permission to run the "passwd -S $username" command if you are not root. This code retrieves user names
from the "/etc/passwd" file, runs the "passwd -S $username" on each user, and then, analyses the output returned for each
user and displays information about users that are locked and users that can login without authentication.
Note: This code does not check the strength of passwords.


check_procs.py:

This program will first open the “/proc/meminfo” file to retrieve the amount of available RAM on the system and then runs
the “ps -eo user,ppid,pid,stat,pcpu,pmem,command” command, retrieves the percentage of memory used by each process and
performs a mathematical calculation to convert them into an approximate value in megabyte and lists processes in two 
groups: Active process(es) and Inactive process(es). Active processes are processes that are constantly accessing 
the CPU and Inactive processes are the ones that are idle or seem to be idle.

http_server.sock.py:

Socket HTTP server.

track_Zombies.py:

This program runs the “ps -eo user,ppid,pid,stat,pcpu,pmem,command” command, sorts out zombie processes and output them to
the terminal.
