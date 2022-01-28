# memfd-monitor
The program monitors and logs the process calling memfd_create. Along with process name and PID, it also logs file descriptors associated with the memfd_create caller process. 
The program:

>> logs process calling memfd_create along with its file descriptors.
>> logs process calling memfd_create via direct syscall.
>> logs daemonized(fileless) process calling memfd_create via direct syscall.
