import socket, sys, requests

raw = "https://raw.githubusercontent.com/redscientific/Companion/master/Version.txt?token=AH5QIBO7ADV5FWFR2AXOYSK5AAF3C"
r = requests.get(raw)
# print(r.status_code)
# print(r.headers['content-type'])
if "Companion App Version:" in r.text:
    print(r.text[r.text.index(":") + 1:])

'''
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error", err)
    # default port for socket
port = 80

try:
    host_ip = socket.gethostbyname('www.github.com')
except socket.gaierror:
    # this means could not resolve the host
    print("there was an error resolving the host")
    sys.exit()

    # connecting to the server
s.connect((host_ip, port))

print("the socket has successfully connected to www.github.com on port ==", host_ip)
'''