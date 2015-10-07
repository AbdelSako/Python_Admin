def ret_cmd(cmd): #Command function
   from subprocess import Popen, PIPE
   exe = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
   return exe.communicate() #returns a tuple of stdout and stderr

def int_main():
   passwd_file = '/etc/passwd'
   nopasswd_users = ''
   locked_users = ''

   f = open(passwd_file, 'r')
   pwd_db = f.readlines()
   f.close()

   user_list = []
   for line in pwd_db:
      u = line.split(':')
      user_list.append(u[0])

   for user in user_list:
      stdout, stderr = ret_cmd('passwd -S %s'%user)
      if stdout:
         user = stdout.split()[0]
         status = stdout.split()[1]
         if status == 'NP':
            nopasswd_users += '[>] %s\n'%user
         if status == 'L':
            locked_users += '[>] %s\n'%user
      elif stderr:
         print '[error] %s'%stderr

   if locked_users:
      print '\n[*] LOCKED USER(S):\n'
      print locked_users
   if nopasswd_users:
      print '\n[*] WARNING: Password(s) not set.'
      print '[*] The follwing user(s) can log in without authentication,'
      print '[*] which can be a security threat.\n'
      print nopasswd_users
   if not locked_users and not nopasswd_users: print '[*] Quedal'
if __name__ == '__main__':
   int_main()
