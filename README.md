# memfd-monitor
The program monitors and logs the process calling memfd_create. Along with process name and PID, it also logs file descriptors associated with the memfd_create caller process. 
The program also logs daemonized(fileless) process calling memfd_create via direct syscall.

