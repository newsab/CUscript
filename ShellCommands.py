import paramiko


class ShellCommands:

    def __init__(self, ip):
        """
        Class with the purpose of communication with the PMU, PBU and PTU through shell commands.
        Takes an ip address as parameter.
        """
        self.hostname = ip
        self.username = "pi"
        self.password = "pamp"
        self.client = paramiko.SSHClient()

    def connect(self):
        """
        Connect to the given ip address
        """
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.hostname,
                                username=self.username, password=self.password)
            print("Connected")
        except:
            return "[!] Cannot connect to the SSH Server"
            exit()

    def executeCmd(self, cmd):
        """
        Takes a command as a parameter.
        Then executes the command.
        Return a decoded string with information from the command.
        """
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
        """
        Tells executeCmd() to execute a command which will return information about if PMUscript is running.
        """
        command = "sudo systemctl status pmuscript | grep Active"
        return self.executeCmd(command)

    def rebootRaspi(self):
        """
        Tells executeCmd() to execute a command which will reboot the Raspberry Pi and return information about it.
        """
        command = "sudo reboot"
        return self.executeCmd(command)

    def coldRestart(self):
        """
        Tells executeCmd() to execute a command which will make a cold restart of the RasPiGNSS chip and return information about it.
        """
        command = "sudo ubxcmd -v cfg-rst 0xffffC"
        return self.executeCmd(command)

    def setFrequency(self, freq):
        """
        Takes a frequency as a parameter.
        Tells executeCmd() to execute a command which will set the frequency.
        """
        frequency = (float(freq)*1000000.0)
        command = "hackrf_transfer -f" + str(frequency) + " -a1 -x47 -c127"
        return self.executeCmd(command)
