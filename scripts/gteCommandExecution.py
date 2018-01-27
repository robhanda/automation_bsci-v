
import ConfigParser,sys,os,time,paramiko,telnetlib,getpass




def findalivemachines(ip,num_of_VM,noOfBcfPerMachine):
        global hostname
        hostname=[]
        num_of_VM=num_of_VM+1
        ip_parts = ip.split(".")
        ip_parts = [int(part) for part in ip_parts]
        first, second, third, fourth = ip_parts

        #print first, second, third, fourth


        for i in range(1,num_of_VM):

                result = os.system("ping -c 2 " +str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)+" > /dev/null 2>&1")

                #fourth= fourth +4

                if result == 0:
                        #print("ip %s is pinging" %i)
                        comp_ip=str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)
                        #print comp_ip
                        hostname.append(comp_ip)


                else:
                        print("ip %s is not pinging" %i)

                fourth=fourth+noOfBcfPerMachine
        return hostname







def makeLogfolder(logPath,logfolder,logServerIp):
	logFolderPath=logPath+logfolder
	cmd1='cd'+' '+logPath
        cmd2='rm -rf'+' '+logfolder
	cmd= cmd1+";"+cmd2+';'
        cmd3='mkdir'+' '+logFolderPath
        print cmd3
	ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(logServerIp, port=22, username='root', password='password')
	stdin, stdout, stderr = ssh.exec_command(cmd)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        ssh.close()




def createInitGteCmd():

    global initGteCmd
		
    initGteCmd = ["LT_SET CONF","EOF"]
    print initGteCmd
def createBcfGteCmd(noOfBcfPerMachine,gemuPathBcf,btsType,abisType):
    for bcf in xrange(noOfBcfPerMachine):
        if bcf==0:
            gteCmd="LT_SET BIN" + " "+abisType + " "+str(bcf) + " " + gemuPathBcf + " " + "struct_2g.db" + " 0 " + btsType + " " + "NULL"
            bcfGteCmd.append(gteCmd)
        else :
            gteCmd = "LT_SET BIN" + " " + abisType + " " + str(bcf) + " " + gemuPathBcf +"_"+str(bcf)+ " " + "struct_2g.db" + " 0 " + btsType + " " + "NULL"
            bcfGteCmd.append(gteCmd)
#    print bcfGteCmd


def createGprsGteCmd(noOfBcfPerMachine,gemuPathBcf,gtePath,filePathgprs,elgStateMachinePath,filePathgprstest):
    gprsConfFile = filePathgprs.split("/")
    gprsConfFile = gprsConfFile[(gprsConfFile.__len__()) - 1]
    gprsTestFile = filePathgprstest.split("/")
    gprsTestFile = gprsTestFile[(gprsTestFile.__len__()) - 1]

    for bcf in xrange(noOfBcfPerMachine):
        if bcf==0:
            gprsCmd ="LT_SET BIN ELG" + " " + str(bcf) + " " + gemuPathBcf + " " + gtePath+"/" + str(gprsConfFile) + " " + elgStateMachinePath  + str(gprsTestFile)+" " +str(bcf)+" " +  "NULL NULL"
            gprsGteCmd.append(gprsCmd)
        else :
            gprsCmd ="LT_SET BIN ELG" + " " + str(bcf) + " " + gemuPathBcf +"_" + str(bcf) + " " + gtePath +"/"+ str(gprsConfFile) + " " + elgStateMachinePath  + str(gprsTestFile)+" " +str(bcf)+" " +  "NULL NULL"
            gprsGteCmd.append(gprsCmd)
 
#   print gprsGteCmd


def createEgprsGteCmd(noOfBcfPerMachine,gemuPathBcf,gtePath,filePathegprs,elgStateMachinePath,filePathegprstest):
    egprsConfFile = filePathegprs.split("/")
    egprsConfFile = egprsConfFile[(egprsConfFile.__len__()) - 1]
    egprsTestFile = filePathegprstest.split("/")
    egprsTestFile = egprsTestFile[(egprsTestFile.__len__()) - 1]

    for bcf in xrange(noOfBcfPerMachine):
        if bcf == 0:
            egprsCmd = "LT_SET BIN ELG" + " " + str(bcf) + " " + gemuPathBcf + " " + gtePath +"/"+ str(egprsConfFile) + " " + elgStateMachinePath  + str(egprsTestFile)+" " +str(bcf)+" " +  "NULL NULL"
            egprsGteCmd.append(egprsCmd)
        else:
            egprsCmd = "LT_SET BIN ELG" + " " + str(bcf) + " " + gemuPathBcf + "_" + str(bcf) + " " + gtePath +"/"+ str(egprsConfFile) + " " + elgStateMachinePath  + str(egprsTestFile)+" " +str(bcf)+" " +  "NULL NULL"
            egprsGteCmd.append(egprsCmd)
    print egprsGteCmd

def createElgCmd():
	global elgCmd
	elgCmd=["LT_START","LT_ENABLE ALL"]

def createEcgsmGteCmd():
    pass

'''
def gettingAliveMachinesIp():
	global aliveIpList
	aliveIpList=[]

	with open("/home/Automation/parameters/aliveMachines.txt") as file:

		for line in file:
			if len(line)>0:

         	   		print line
            			line=line.strip()
            			aliveIpList.append(line)

	return aliveIpList
#	print aliveIpList


'''





def telnetFunction(aliveIpList,completeGteCmd):
#	hostname=["10.253.192.54"]
#	hostname=findalivemachines()
	port = 7031
	for j in aliveIpList:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(j, port=22, username='root', password='password')
              	while True:
		       try:	
		  		stdin, stdout, stderr = ssh.exec_command('cd /root/gte; killall process_manager.tcl;./recover.tcl;echo $?;')
				time.sleep(35)
				t = telnetlib.Telnet(j,port)
				d = t.read_until(b'GEMU>',10)
				for cmd in completeGteCmd:
						print cmd
        					s = t.write(cmd+"\r")
						print s
        					time.sleep(10)
        					d = t.read_until(b'GEMU>', 10)
        					print d
						t.close
			  	break
		       except KeyboardInterrupt:
						break
		       except:
		       		pass	


if __name__ == "__main__":
    bcfGteCmd=[]
    gprsGteCmd=[]
    egprsGteCmd=[]
    ecgsmGteCmd=[]
    completeGteCmd=[]
    gemuConfigfile = ConfigParser.ConfigParser()
    gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
    trafficProfile=gemuConfigfile.get("Test_Case_Details","traffic_profile")
    print trafficProfile	
    noOfBcfPerMachine=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_bcf_per_machine"))
    gemuPathBcf=gemuConfigfile.get("Test_Environment_GEMU","gemuPathBcf")
    btsType=gemuConfigfile.get("Test_Environment_GEMU","bts_type")
    abisType=gemuConfigfile.get("Test_Environment_GEMU","abis_type")
    gtePath=gemuConfigfile.get("Test_Environment_GEMU","gtePath")
    filePathgprs=gemuConfigfile.get("Test_Environment_GEMU","filePathgprs")
    elgStateMachinePath=gemuConfigfile.get("Test_Environment_GEMU","elgStateMachinePath")
    filePathgprstest=gemuConfigfile.get("Test_Environment_GEMU","filePathgprstest")
    filePathegprstest=gemuConfigfile.get("Test_Environment_GEMU", "filePathegprstest")
    filePathegprs=gemuConfigfile.get("Test_Environment_GEMU", "filePathegprs")
    logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
    logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
    logServerIp=gemuConfigfile.get("Test_Environment_GEMU","logserver_ip")
    num_of_VM=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_gemu_machines"))
    gemu_StartIp=gemuConfigfile.get("Test_Environment_GEMU","gemu_machine_start_ip")
    print("test case assed")

    
    aliveIpList=findalivemachines(gemu_StartIp,num_of_VM,noOfBcfPerMachine)
    print("test case failed")		
    #aliveIpList=gettingAliveMachinesIp()
    num_of_VM=num_of_VM+1
    print num_of_VM
    makeLogfolder(logPath,logfolder,logServerIp)		
    if trafficProfile=="GPRS":
	
        createInitGteCmd()
        createBcfGteCmd(noOfBcfPerMachine,gemuPathBcf,btsType,abisType)
        createGprsGteCmd(noOfBcfPerMachine,gemuPathBcf,gtePath,filePathgprs,elgStateMachinePath,filePathgprstest)
	createElgCmd()
	completeGteCmd = initGteCmd+bcfGteCmd+gprsGteCmd+elgCmd
	print completeGteCmd
	telnetFunction(aliveIpList,completeGteCmd)
    if trafficProfile=="EGPRS":
        createInitGteCmd()
        createBcfGteCmd(noOfBcfPerMachine,gemuPathBcf,btsType,abisType)
        createEgprsGteCmd(noOfBcfPerMachine,gemuPathBcf,gtePath,filePathegprs,elgStateMachinePath,filePathegprstest)
	createElgCmd()
	completeGteCmd=initGteCmd+bcfGteCmd+egprsGteCmd+elgCmd
	print completeGteCmd
	telnetFunction(aliveIpList,completeGteCmd)
    elif trafficProfile=="ECGSM":
        pass
    elif trafficProfile=="GPRS+EGPRS":
        createBcfGteCmd()
        createGprsGteCmd()
        createEgprsGteCmd()
      


