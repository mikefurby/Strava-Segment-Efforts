import subprocess, signal
from subprocess import Popen
import os

def check_for_kill():
    processes = subprocess.call(["ps", "-u", "ubuntu"])
    processes = Popen(["ps", "-u", "ubuntu"], stdout=subprocess.PIPE)
    out, err = processes.communicate()
    for line in out.splitlines():
        elements=line.split()
        PID=(elements[0])
        TTY=(elements[1])
        TIME=(elements[2])
        CMD=(elements[3])
        print (PID,TTY,TIME,CMD)
        if (str(TIME)) != ("TIME"):
            h, m, s = TIME.split(':')
            process_time = (int(h) * 3600 + int(m) * 60 + int(s))
            print (process_time)
            if process_time > 100:
                print (PID,process_time) 
                print (int(PID))
                os.kill(int(PID),signal.SIGKILL)


def main():
   check_for_kill()

if __name__ == '__main__':
    main()
