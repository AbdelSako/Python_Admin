cmd = 'ps -eo user,ppid,pid,stat,pcpu,pmem,command'
db = {'user':None,'ppid':None, 'pid':None, 'stat':None,\
       'pcpu':None,'pmem':None, 'cmd':None}

def ret_cmd(cmd): #Command function
   import subprocess
   exe = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
   return exe.communicate() #returns a tuple of stdout and stderr

def int_main():
   stdout, stderr = ret_cmd(cmd)
   if stdout:
      zombie_procs = ''
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
               elif key == 'pmem': db[key] = float(lines.split()[5])
               elif key == 'cmd': db[key] = lines.split()[6]

            output = "[+] %s \t%d \t%d \t%s \t%.2f \t%.2f \t%s\n"\
               %(db['user'], db['ppid'], db['pid'], db['stat'], db['pcpu'], db['pmem'], db['cmd'])

            if 'Z' in db['stat']: zombie_procs += output

      header =  "[+] user \tppid \tpid \tstat \tcpu% \tmem% \tcommand\n"
      
      if zombie_procs:
         print header+zombie_procs
      else: print "\n[+] Zombie process(es) not found."

if __name__ == '__main__':
   int_main()
