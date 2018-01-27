
import ConfigParser,paramiko,time,sys,os,telnetlib

def telnetFunction(bscIp):
        global telnetBsc
        global expectedBscLine
     #   print bscIp
        expectedBscLine = "BASE TRANSCEIVER STATION HANDLING IN BSC COMMAND <EQ_>"
        telnetBsc = telnetlib.Telnet(bscIp)
        status=telnetBsc.read_until(b'ENTER USERNAME <',5)
    #    print status
        username="SYSTEM"
        status=telnetBsc.write(username+"\r")
   #     print status
        status=telnetBsc.read_until(b'ENTER PASSWORD <',5)
  #      print status
        password="SYSTEM"
        telnetBsc.write(password+"\r")
        telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
        status=telnetBsc.read_until(b'<',5)
 #       print status


def setOflLoglevel(pcum_id,fp_loglevel,sp_loglevel):
	telnetBsc.read_until(b'expectedBscLine',10)
        pcumLogin=("ZDDS:PCUM,%s:;"%pcum_id)
        status=telnetBsc.read_until(b'$',10)
#	print status
        status=telnetBsc.write(pcumLogin+'\n\r')
#	print status

        telnetBsc.read_until(b'$',10)

	fpLoglevel="sll fp "+fp_loglevel
        telnetBsc.write(fpLoglevel+'\r')
        status=telnetBsc.read_until(b'$',10)
  #      print status

	spLoglevel="sll sp "+sp_loglevel
        telnetBsc.write(spLoglevel+'\r')
        status=telnetBsc.read_until(b'-$',10)
 #       print status

	telnetBsc.write("exit"+'\r')
	status=telnetBsc.read_until(b'-$',10)
#	print status

	telnetBsc.close()

def fTransferFiles(remote_path, local_path,bscIp, mode=0):
    ftp_ssh = paramiko.SSHClient()
    ftp_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ftp_ssh.connect(hostname=bscIp, username="SYSTEM", password="SYSTEM")
    ftp_client = ftp_ssh.open_sftp()
    try:
#	print("under try")
        if (mode == 0):
	#    print("under if statement")
            ftp_client.get(remote_path, local_path)
        else:
            ftp_client.put(local_path, remote_path)
        return 1

    except:
        return 0

if __name__ == "__main__":

        gemuConfigfile = ConfigParser.ConfigParser()
        gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
        logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
        logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
        logServerIp=gemuConfigfile.get("Test_Environment_GEMU","logserver_ip")
	pcum_id=gemuConfigfile.get("Test_Environment_BSC","pcum_id")
	fp_loglevel=gemuConfigfile.get("Ofl_Logs_Details","fp_loglevel")        
	sp_loglevel=gemuConfigfile.get("Ofl_Logs_Details","sp_loglevel")
	omuWorkingDir=gemuConfigfile.get("Ofl_Logs_Details","working_directory")
	logTimeinhr=gemuConfigfile.get("Ofl_Logs_Details","log_collection_time_hr")
	bscIp=gemuConfigfile.get("Test_Environment_BSC","bsc_omu_ip")
        logFolderPath=logPath+logfolder
#	print logFolderPath
	logTimeinSeconds=int(logTimeinhr)*3600
	print logTimeinSeconds	
	remote_path=omuWorkingDir+'-/SG092500/ASWDIR/LGFILE00.IMG'
	remote_path1=omuWorkingDir+'-/SG092500/ASWDIR/LGFILE01.IMG'
	local_path=logFolderPath+"/"+'LGFILE00.IMG'
	local_path1=logFolderPath+"/"+'LGFILE01.IMG'

	# calling function to telnet bsc and set log level
	telnetFunction(bscIp)
	setOflLoglevel(pcum_id,fp_loglevel,sp_loglevel)
	#calling function to wait as per user input
	print("now waiting for"+str(logTimeinSeconds)+" seconds")
	time.sleep(logTimeinSeconds)

	# calling function to transfer log files from OMU to logfolder
	fTransferFiles(remote_path, local_path,bscIp, mode=0)
	fTransferFiles(remote_path1, local_path1,bscIp, mode=0)



