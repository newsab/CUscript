import paramiko

class ShellCommands:

    def __init__(self, ip):
        self.hostname = ip
        self.username = "pi"
        self.password = "pamp"
        self.client = paramiko.SSHClient()
        self.connect()

    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try: 
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        except:
            return "[!] Cannot connect to the SSH Server"
            exit()

    def setBaudrate(self):
        """
        If I really hate pressing `enter` and
        typing all those hash marks, I could
        just do this instead
        """
        command = "sudo stty -F /dev/ttyAMA0 115200 raw; stty -aF /dev/ttyAMA0"     
        #for command in commands:
            #print("="*50, command, "="*50)
        stdin, stdout, stderr = self.client.exec_command(command)
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def coldRestart(self):
        return "Restart done"

    def startStr2StrServer(self):
        return "Server startar"

    def startStr2StrClient(self):
        return "Server startar"