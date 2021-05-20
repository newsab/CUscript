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

    def executeCmdNoReturn(self, cmd):
        """
        Takes a command as a parameter.
        Then executes the command.
        Does not return a decoded string with information from the command instead it rerurn a fixed string.
        """
        self.connect()
        command = cmd
        try:
            stdin, stderr = self.client.exec_command(command)
            self.client.close()
            return('PTU:s frekvens är nu satt till ')

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

        command = "sudo hackrf_transfer -f" + \
            str(frequency) + " -a1 -x47 -c127"
        return self.executeCmdNoReturn(command)

    def stopTransmitting(self):
        """
        Tells executeCmd() to execute a command which will tell the HackRF to stop transmitting.
        """
        command = "sudo killall -9 hackrf_transfer"
        msg = self.executeCmd(command)

        return "PTU har slutat sända"

    def resetHackRF(self):
        """
        Tells executeCmd() to execute a command which will tell the HackRF to reset.
        """
        command = "sudo hackrf_info"
        msg2 = self.executeCmd(command)
