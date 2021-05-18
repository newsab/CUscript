import paramiko


class ShellCommands:

    def __init__(self, ip):
        self.hostname = ip
        self.username = "pi"
        self.password = "pamp"
        self.client = paramiko.SSHClient()

    def connect(self):

        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.hostname,
                                username=self.username, password=self.password)
            print("Connected")
        except:
            return "[!] Cannot connect to the SSH Server"
            exit()

    def executeCmd(self, cmd):
        self.connect()
        command = cmd
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            returnString = stdout.read().decode()
            self.client.close()
            return(returnString)

        except:
            err = stderr.read().decode()
            self.client.close()
            return(err)

    def getPmuscriptStatus(self):
        command = "sudo systemctl status pmuscript | grep Active"
        return self.executeCmd(command)

    def rebootRaspi(self):
        command = "sudo reboot"
        return self.executeCmd(command)

    def coldRestart(self):
        command = "sudo ubxcmd -v cfg-rst 0xffffC"
        return self.executeCmd(command)

    def setFrequency(self, freq):
        frequency = (float(freq)*1000000.0)
        command = "hackrf_transfer -f" + str(frequency) + " -a1 -x47 -c127"
        return self.executeCmd(command)
