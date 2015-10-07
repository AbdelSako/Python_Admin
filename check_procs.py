cmd = 'ps -eo user,ppid,pid,stat,pcpu,pmem,command'
db = {'user':None,'ppid':None, 'pid':None, 'stat':None,\
       'pcpu':None,'pmem':None, 'cmd':None}

def ret_cmd(cmd): #Command function
   import subprocess
   exe = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
   return exe.communicate() #returns a tuple of stdout and stderr

mem_info = '/proc/meminfo'
def get_avail_ram(mem_info):
   f = open(mem_info,'r')
   avail_ram = f.readline(); f.close()
   avail_ram = (float(avail_ram.split()[1]))/1024
   return avail_ram

def int_main():
   avail_ram = get_avail_ram(mem_info)
   stdout, stderr = ret_cmd(cmd)
   if stdout:
      inactive_procs = ''; active_procs = ''
      cpu_load = 0.0; inact_mem_load = 0.0;
      act_mem_load = 0.0; total_mem_used = 0.0

      n = 0
      for lines in stdout.split('\n'):
         if n == 0: n += 1; continue # Skip first line
         if lines:
            for key in db.keys():
               if key == 'user': db[key] = str(lines.split()[0])
               elif key == 'ppid': db[key] = int(lines.split()[1])
               elif key == 'pid': db[key] = int(lines.split()[2])
               elif key == 'stat': db[key] = str(lines.split()[3])
               elif key == 'pcpu': db[key] = float(lines.split()[4])
               elif key == 'pmem':
                  db[key] = float(lines.split()[5])*avail_ram/100
                  total_mem_used += db['pmem']
               elif key == 'cmd': db[key] = lines.split()[6]

            output = "[+] %s \t%d \t%d \t%s \t%.2f \t%.2f\tmb \t%s\n"\
               %(db['user'], db['ppid'], db['pid'], db['stat'], db['pcpu'], db['pmem'], db['cmd'])
            if db['pcpu'] > 0:
               cpu_load += db['pcpu']
               act_mem_load += db['pmem']
               active_procs += output
            elif db['pcpu'] == 0:
               inact_mem_load += db['pmem']
               inactive_procs += output

      header =  "[+] user \tppid \tpid \tstat \tcpu% \tmem in use \tcommand"
      if active_procs:
         print "[+] ACTIVE PROCESSES:"
         print "[+] Approximate memory: %.2f MB\n[+] Approximate CPU load: %.2f%%\n"%(act_mem_load, cpu_load)
         print header
         print active_procs

      if inactive_procs:
         print "[+] INACTIVE PROCESSES:"
         print "[+] Approximate memory: %.2f MB\n"%inact_mem_load
         print header
         print inactive_procs

      if not active_procs and not inactive_procs:
         print "[*] No process found...\n"
         # The program won't run into this clause
         # I am sure at 99.9%

      if active_procs or inactive_procs:
         print "[+] Overall CPU load: %.2f%%"%cpu_load
         print "[+] Total memory in use: %.2fMB"%total_mem_used
         print '[+] Free memory: %.2fMB'%(avail_ram-total_mem_used)

if __name__ == '__main__':
   int_main()
