import paramiko


hostname = "172.16.03"
username = "pi"
password = "pamp"

commands = [
    "pwd",
    "id",
    "sudo reboot"
]


# initialize the SSH client
client = paramiko.SSHClient()
# add to known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=hostname, username=username, password=password)
except:
    print("[!] Cannot connect to the SSH Server")
    exit()
