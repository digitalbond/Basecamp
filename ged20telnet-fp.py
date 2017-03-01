import socket
import time
import sys

def hexstr(instr):
  out = ""
  for b in instr:
    out = out + str('%02x' % ord(b))
  return out

if len(sys.argv) < 4:
  sys.stderr.write("Usage: " + sys.argv[0] + " <ip> <port> <timeout>\n")
  sys.exit(1)
host = sys.argv[1]
port = int(sys.argv[2])
timeout = float(sys.argv[3])
bsize = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.5)
s.connect((host,port))
commands = range(0,50)
commands.append(138)
commands.append(139)
commands.append(140)
time.sleep(1)
response = s.recv(bsize)
s.settimeout(timeout)
print "," + hexstr(response)
for i in range(251, 255):
	for j in commands:
		directive = chr(0xff) + chr(i) + chr(j)
		s.send(directive)
		try:
			response = s.recv(bsize)
		except:
			response = ""
		print hexstr(directive) + "," + hexstr(response)
print "done"
