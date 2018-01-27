import ConfigParser,sys,paramiko,os,telnetlib,time

if __name__=="__main__":
	gemuConfigfile = ConfigParser.ConfigParser()
	gemuConfigfile.read('testConfiguration.ini')
	logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
	logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
	logServerIp=gemuConfigfile.get("Test_Environment_GEMU","logserver_ip")
	logFolderPath=logPath+logfolder
	print logServerIp
	cmd1='cd'+' '+logPath
	cmd2='rm -rf'+' '+logfolder
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(logServerIp, port=22, username='root', password='password')
	cmd= cmd1+";"+cmd2+';'
	cmd3='mkdir'+' '+logFolderPath
        print cmd3
	stdin, stdout, stderr = ssh.exec_command(cmd)
	time.sleep(5)
	stdin, stdout, stderr = ssh.exec_command(cmd3)
	ssh.close()
	

