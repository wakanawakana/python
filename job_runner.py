import subprocess
import sys, os, select, time

   
def monitor_job(jobfile):
    while 1:
        try:
            if os.path.exists('./job.lock'): os.remove('./job.lock')
            os.rename(jobfile, 'job.lock')
            f = open('job.lock', 'r')
            lines = []
            for line in f:
                if line != "\n" and line[0] != '#':
                    line = line.rstrip('\n')
                    lines.append(line)
        
            f.close()
            f = open(jobfile, 'w')
            for n in range(1, len(lines)):
                f.write(lines[n]+'\n')
            f.close()
            if len(lines) > 0:
                try:
                    print 'execute comand: {}'.format(lines[0])
                    proc = subprocess.Popen(lines[0], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    while True:
                        line = proc.stdout.readline()
                        sys.stdout.write(line)
                        if proc.poll() is not None:
                            print 'End Process command (waiting next)'
                            break
                    
                except KeyboardInterrupt:
                    print "aborted"
                    proc.kill()
                except:
                    print "Process error"

            time.sleep(2)

        except KeyboardInterrupt:
            print "aborted"
            break
        except:
            print "job file error"
            break

    return

if __name__ == '__main__':
    jobfile = 'job.txt'
    print 'Start Easy Job Runner'
    monitor_job(jobfile)
    print 'BeyBey\n'
    
