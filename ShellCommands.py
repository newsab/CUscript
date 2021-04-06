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
            print("Connection closed")
            return(command + " succesfully executed")

        except:
            err = stderr.read().decode()
            self.client.close()
            print("Connection closed")
            return(err)

    def executeCmd2(self, cmd):

        self.connect()
        command = cmd
        try:
            self.client.exec_command(command)
            self.client.close()
            print("Connection closed")
            return(command + " succesfully executed")

        except:
            self.client.close()
            print("Connection closed")
            return("Could not connect to Str2STr Server")

    def setBaudrate(self):
        command = "sudo stty -F /dev/ttyAMA0 115200 raw; stty -F /dev/ttyAMA0"
        print(command)
        return self.executeCmd(command)

    def startPMUapp(self):
        command = "sh /home/pi/Shellscripts/PMU.sh"
        print(command)
        return self.executeCmd2(command)

    def startStr2StrServer(self):
        command = "sudo /./rtkscript/./str2str.sh"
        print(command)
        return self.executeCmd2(command)

    def startStr2StrClient(self):
        command = "sudo kill -9 $(sudo lsof -t -i:2101); str2str -in tcpcli://:@172.16.0.6:2101 -out serial://ttyAMA0:115200:8:n:1:off"
        print(command)
        return self.executeCmd2(command)

    def startPyro(self):
        #command = "pyro4-ns -n 172.16.0.3 -p 43329"
        command = "/usr/bin/pyro.sh"
        print(command)
        return self.executeCmd2(command)

    def coldRestart(self):
        command = "sudo ubxcmd -v cfg-rst 0xffffC"
        print(command)
        return self.executeCmd(command)

    def setFrequency(self, freq):
        frequency = (float(freq)*1000000.0)
        command = "hackrf_transfer -f" + str(frequency) + " -a1 -x47 -c127"
        print(command)
        return self.executeCmd(command)
