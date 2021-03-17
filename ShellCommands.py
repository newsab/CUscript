import paramiko


hostname = "172.16.06"
username = "pi"
password = "pamp"

commands = [
    "pwd",
    "id",
    "uname -a",
    "df -h",
    "sudo stty -aF /dev/ttyAMA0",
    "sudo /./rtkscript/./str2str.sh"
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

    # execute the commands
for command in commands:
    print("="*50, command, "="*50)
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)
