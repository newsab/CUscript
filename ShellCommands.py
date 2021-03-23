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
            print("connected")
            return

        except:
            return "[!] Cannot connect to the SSH Server"
            exit()

    def executeCmd(self, cmd):
        self.client.close()
        self.connect()
        command = cmd
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            print(stdout.read().decode())
            return

        except:
            print("someting wnt wrong!!!")

    def PMUbaud(self):
        command = "sudo stty -F /dev/ttyAMA0 115200 raw; stty -aF /dev/ttyAMA0"
        print(command)
        self.executeCmd(command)

    def startPMUapp(self):
        command = "sudo /home/pi/pmuScript/PMUapp.py"
        print(command)
        self.executeCmd(command)

    def startStr2StrClient(self):
        command = "sudo kill -9 $(sudo lsof -t -i:2101); sudo /./rtkscript/./str2str.sh"
        print(command)
        self.executeCmd(command)

    def startPyro(self):
        command = "sudo pyro4-ns -n 172.16.0.3 -p 43329"
        print(command)
        self.executeCmd(command)

    def coldRestart(self):
        command = "sudo ubxcmd -v cfg-rst 0xffffC"
        print(command)
        self.executeCmd(command)

    def StartPMU(self):
        """[Set PMU ready]
        Sets baudrate to 115200, cold restart of the RaspiGNNS, start rtk client str2str, start Pyro4 and last starts the PMUapp.py
        """
        self.connect()
        try:
            command = "sudo stty -F /dev/ttyAMA0 115200 raw; stty -aF /dev/ttyAMA0"
            stdin, stdout, stderr = self.client.exec_command(command)

            return(stdout.read().decode())
            self.client.close()
        except:
            err = stderr.read().decode()
            return(err)

    def StartPMUapp2(self):
        """[Set PMU ready]
        Sets baudrate to 115200, cold restart of the RaspiGNNS, start rtk client str2str, start Pyro4 and last starts the PMUapp.py
        """
        self.connect()
        try:
            command = "sudo /home/pi/pmuScript/PMUapp.py"
            stdin, stdout, stderr = self.client.exec_command(command)
            self.client.close()
            print(stdout.read().decode())
            return

        except:
            err = stderr.read().decode()
            return(err)

    def StartRBU(self):
        """[Set RBU ready]
        Sets baudrate to 115200, cold restart of the RaspiGNNS,   
        """
        self.connect()
        try:
            command = "sudo stty -F /dev/ttyAMA0 115200raw;"
            stdin, stdout, stderr = self.client.exec_command(command)
            self.client.close()
            return(stdout.read().decode())
        except:
            err = stderr.read().decode()
            return(err)

    def startStr2StrServer(self):
        self.connect()
        command = "sudo kill -9 $(sudo lsof -t -i:2101); sudo /./rtkscript/./str2str.sh"
        stdin, stdout, stderr = self.client.exec_command(command)
        self.client.close()
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def startStr2StrClient2(self):
        self.connect()
        command = "sudo kill -9 $(sudo lsof -t -i:2101); str2str -in tcpcli://:@172.16.0.6:2101 -out serial://ttyAMA0:115200:8:n:1:off"
        stdin, stdout, stderr = self.client.exec_command(command)
        self.client.close()
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def startPyro2(self):
        self.connect()
        command = "sudo pyro4-ns -n 172.16.0.3 -p 43329"
        stdin, stdout, stderr = self.client.exec_command(command)
        self.client.close()
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

    def coldRestart2(self):
        self.connect()
        command = "sudo ubxcmd -v cfg-rst 0xffffC"
        stdin, stdout, stderr = self.client.exec_command(command)
        self.client.close()
        return(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            return(err)

        """
        sudo kill -9 $(sudo lsof -t -i:2101)  == kill process on port 2101
        sudo lsof -i:2101                     == check process on port 2101

        """
