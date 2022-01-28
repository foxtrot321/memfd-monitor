import sys
import time
import os
from bcc.utils import printb
from bcc import BPF

bppf = r"""
BPF_RINGBUF_OUTPUT(buffer,1 << 4);

struct event {
    char uname[16];
    u64 pid;
   
};
TRACEPOINT_PROBE(syscalls, sys_enter_memfd_create) {

    struct event event = {};
     
    bpf_probe_read_user_str(event.uname, sizeof(event.uname), args->uname);
    
    event.pid=bpf_get_current_pid_tgid();
    
    event.pid=event.pid >> 32;
    
    buffer.ringbuf_output(&event, sizeof(event),0);
    return 0;
    
}
"""

b = BPF(text=bppf)

#name of the process calling memfd_create
def get_pid_name(pid):
    with open("/proc/%d/cmdline" % pid) as status:
        for line in status:
            return line

#print file descriptors of the process
def get_fd_name(pid):
    os.system('ls -al /proc/%d/fd' %pid)

def callback(ctx, data, size):
    event = b['buffer'].event(data)
    
    printb("%-8s %-8d %-8s" % (event.uname,event.pid,get_pid_name(event.pid))) #printing name,pid and pid's proc name
    print("Printing file descriptors of the PID %d\n"%(event.pid))
    get_fd_name(event.pid) #print file descriptors of the process
b['buffer'].open_ring_buffer(callback)
 
print("Printing memfd_create caller's pid and name, ctrl-c to exit.")
print("\nName\tPID\tProcess Name\n")
try:
    while 1:
        b.ring_buffer_poll()

except KeyboardInterrupt:
    sys.exit()
