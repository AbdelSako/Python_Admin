""" This http server handles only the get request  """

import sys, socket

def get_HostPort(request):
   port = 80
   headers = request.split('\r\n')
   if len(headers) <= 1:
      return '0.0.0.0',0
   host_port = headers[1][6:]

   host  = host_port.split(':')[0]
   if len(host_port.split(':')) > 1:
      port = host_port.split(':')[1]
   return str(host),int(port)

def recv_request(connection):
   buffer = ""
   connection.settimeout(2)
   try:
      while True:
         data = connection.recv(4096)
         if not data:
            break
         buffer += data
   except:
      pass
   return buffer


def server_loop(local_host,local_port):
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      server.bind((local_host,local_port))
   except:
      print "[!!] Failed to listen on %s:%d" % (local_host,local_port)
      print "[!!] Check for other listening sockets or correct permissions."
      sys.exit(0)

   print "[*] Listening on %s:%d" % (local_host,local_port)
   server.listen(5)

   while True:
      try:
         print "[+] Waiting for incomming connecction... "
         client_sock, addr = server.accept()
         print "[+] Received incoming connection from %s:%d\n" %(addr[0],addr[1])
         request = recv_request(client_sock)
         print "[+] request from the client: ",request
         remote_host, remote_port = get_HostPort(request)

         if remote_host == sys.argv[1] or remote_host == 'localhost':
            header = "HTTP/1.1 200 OK\r\nServer: Minimal Python Server\r\n\r\n"
            body = "<html><body><p align='center'> Hello World!!!</p</body></html>\r\n"
            client_sock.sendall(header+body)
            client_sock.close
            del client_sock
            print "[+] Home page function executed successfully..\n"
      except KeyboardInterrupt:
         print "\n"; break

def main():
   if len(sys.argv) != 3:
      print "[+] Usage: ./prog_name [local host] [local port]"
      return 0

   server_loop(sys.argv[1], int(sys.argv[2]))

if __name__ == '__main__':
   main()
