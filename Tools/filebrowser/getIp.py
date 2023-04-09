import socket
import os
import platform
import subprocess
import fcntl
import struct

ip = ""

# ref https://stackoverflow.com/questions/45892239/what-is-the-use-of-0x8915
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

def checkError(errorCode, deed):
    if(errorCode != 0):
        print('failed at ' + deed + "!")
        os._exit(1)

if (platform.architecture()[1] == "WindowsPE"):
    print("run in windows")
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    ret = subprocess.run(["where", "filebrowser"])
    if (ret.returncode == 1):
        print("Cannot find filebrowser, please install first! Doc is https://filebrowser.org/installation")
        os._exit(1)
    else:
        os.system("filebrowser -a " + ip + " -p 7658")
elif(platform.system() == "Darwin"):
    print("run in mac")
    hostname = socket.getfqdn(socket.gethostname())
    for i in range(0,8):
        print(i)
        ip = os.popen("ipconfig getifaddr en%d" % (i)).read().strip('\n')
        if len(ip) > 0:
            break
    if len(ip) < 1:
        raise "ipconfig no use"
    os.system("filebrowser -a " + ip + " -p 7658")
elif(platform.system() == "Linux"):
    try :
        ip = get_ip_address('wlan0')
    except:
        pass
    if (ip == ""):
        try:
            ip = get_ip_address('eth0')
        except:
            pass
    if(ip == ""):
        print('not support wlan0 or eth0')
    else:
        print("ip is ", ip)
        os.system("filebrowser -a " + ip + " -p 7658")
else:
    print('unsupport system: ', platform.system())
    os._exit(1)