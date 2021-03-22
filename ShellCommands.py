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

    def setBaudrate(self, baudrate):
        """
        If I really hate pressing `enter` and
        typing all those hash marks, I could
        just do this instead
        """
        command = "sudo stty -F /dev/ttyAMA0 " + baudrate + " raw; stty -aF /dev/ttyAMA0"     
        stdin, stdout, stderr = self.client.exec_command(command)
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)
    

    def startStr2StrServer(self):
        command = ""   
        stdin, stdout, stderr = self.client.exec_command(command)
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def startStr2StrClient(self):
        command = ""     
        stdin, stdout, stderr = self.client.exec_command(command)
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def startPyro(self):
        command = ""     
        stdin, stdout, stderr = self.client.exec_command(command)
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def coldRestart(self):
        command = ""     
        stdin, stdout, stderr = self.client.exec_command(command)
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)