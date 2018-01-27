import sys,os,ConfigParser,telnetlib,paramiko,getpass,time

def telnetFunction(bscIp):
        global telnetBsc
        global expectedBscLine
	print bscIp
        expectedBscLine = "BASE TRANSCEIVER STATION HANDLING IN BSC COMMAND <EQ_>"
        telnetBsc = telnetlib.Telnet(bscIp)
        status=telnetBsc.read_until(b'ENTER USERNAME <',5)
	print status
        username="SYSTEM"
        status=telnetBsc.write(username+"\r")
	print status
        status=telnetBsc.read_until(b'ENTER PASSWORD <',5)
	print status
        password="SYSTEM"
        telnetBsc.write(password+"\r")
        telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
        status=telnetBsc.read_until(b'<',5)
	print status



def genaTogling(genaState,totalNumOfBcf,numberOfBtsPerBCF):
	global telnetBsc
	global btsLock,btsGenaDisable,btsUnlock,btsGenaState,username,password
	if(genaState=='Y'):	
		for bcf in range(1,totalNumOfBcf):
                	for bts in range (1,numberOfBtsPerBCF):
			
				telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
				telnetBsc.read_until(b'<',5)
                        	cmd=btsGenaState=("ZEQO:BTS=%d%d:GPRS;"%(bcf,bts))
				print cmd
                        	telnetBsc.write(btsGenaState+'\r\n')
                        	telnetBsc.read_until(b'expectedBscLine',5)
                        	btsLock=("ZEQS:BTS=%d%d:L;"%(bcf,bts))
				print btsLock
                        	read=telnetBsc.write(btsLock+'\r\n')
				print read
                        	time.sleep(10)
                        	telnetBsc.read_until(b'expectedBscLine',5)
                        	btsGenaDisable=("ZEQV:BTS=%d%d:GENA=%s;"%(bcf,bts,genaState))
				print btsGenaDisable
                        	telnetBsc.write(btsGenaDisable+'\r\n')
                        	time.sleep(15)
                        	read=telnetBsc.read_until(b'expectedBscLine',5)
				print read
                        	btsUnlock=("ZEQS:BTS=%d%d:U;"%(bcf,bts))
                        	telnetBsc.write(btsUnlock+'\r\n')
                        	time.sleep(10)
                        	read=telnetBsc.read_until(b'expectedBscLine',5)
				print read
#	telnetBsc.close()

	else:
		for bcf in range(1,totalNumOfBcf):
                        for bts in range (1,numberOfBtsPerBCF):
                        
                                telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
                                telnetBsc.read_until(b'<',5)
                                cmd=btsGenaState=("ZEQO:BTS=%d%d:GPRS;"%(bcf,bts))
                                print cmd
                                telnetBsc.write(btsGenaState+'\r\n')
                                telnetBsc.read_until(b'expectedBscLine',5)
                                btsGenaDisable=("ZEQV:BTS=%d%d:GENA=%s;"%(bcf,bts,genaState))
                                print btsGenaDisable
                                telnetBsc.write(btsGenaDisable+'\r\n')
                                read=telnetBsc.read_until(b'expectedBscLine',5)
                                print read

def bufferReading(fileName,bcsu_id,pcu_id,logFolderPath):
	print bcsu_id,pcu_id,logFolderPath
#	global telnetBsc
	print bsc_type,fileName
#	telnetBsc = telnetlib.Telnet(bscIp)
	telnetBsc.read_until(b'expectedBscLine',10)
       	pcumLogin=("ZDDS:PCUM,%s:;"%pcu_id)
       	telnetBsc.read_until(b'var>',10)
       	telnetBsc.write(pcumLogin+'\n\r')
     
  	telnetBsc.read_until(b'var>',10)
	outputfile=logFolderPath+'/'+fileName
	print ("o/p file is %s",outputfile)
	output_file1 = open(outputfile,'w+')
       	pcumVersion="ssv"
       	telnetBsc.write(pcumVersion+'\r')
       	outputpcumVersion=telnetBsc.read_until(b'var>',10)
       	print outputpcumVersion
       	output_file1.write(outputpcumVersion)
       	pcumPqMem="dbu fp"
       	telnetBsc.write(pcumPqMem+'\r')
       	outputpcumPqMem=telnetBsc.read_until(b'var>',10)
	print outputpcumPqMem
       	output_file1.write(outputpcumPqMem)
       	pcumDspMem="dbu sp"
       	print pcumDspMem
       	telnetBsc.write(pcumDspMem+'\r')
       	outputpcumDspMem=telnetBsc.read_until(b'var>',10)
       	print outputpcumDspMem
       	output_file1.write(outputpcumDspMem)
	cmdx="exit"
	print cmdx
       	telnetBsc.write(cmdx+'\r')
       	telnetBsc.read_until(b'REMOTE DEBUGGER SESSION COMMAND <DD_>',10)
	telnetBsc.close
	output_file1.close()

	telnetBsc.close()
def elgStateChange(state,num_of_VM,gemu_StartIp,num_of_Ips_PerVM):
	print ("inside gena toggling function")
	cmd='LT_'+state+' '+'ELG ALL'
        for gemuMachine in range(1,num_of_VM):
                #hostname_list = ["180.144.75.73"]
                print gemu_StartIp
                
                port = 7031
               # print port
               # print num_of_Ips_PerVM
                t = telnetlib.Telnet(gemu_StartIp,port)
                read=t.read_until(b'GEMU>', 10)
		print read
		print cmd
                t.write(cmd+"\r")
		read=t.read_until(b'GEMU>', 10)
		print read
                ipOctectList = gemu_StartIp.split(".")
                lastIpOctet=int((gemu_StartIp.split("."))[3])
                ipAddressList=[]
                ipAddressGenerate=ipOctectList[0]+"."+ipOctectList[1]+"."+ipOctectList[2]+"."+str(lastIpOctet+num_of_Ips_PerVM)
                ipAddressList.append(ipAddressGenerate)
               # print ipAddressList
                gemu_StartIp=ipAddressGenerate
               # print t
    
if __name__=="__main__":
	memoryLeakState=sys.argv
	gemuConfigfile = ConfigParser.ConfigParser()
	gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
	bsc_type=gemuConfigfile.get("Test_Environment_BSC","bsc_type")
	totalNumOfBcf=int(gemuConfigfile.get("Test_Environment_BSC","number_of_bcf_in_bsc"))
	numberOfBtsPerBCF=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_bts_per_bcf"))
	bscIp=gemuConfigfile.get("Test_Environment_BSC","bsc_omu_ip")
	bcsu_id=gemuConfigfile.get("Test_Environment_BSC","bcsu_id")
	pcu_id=gemuConfigfile.get("Test_Environment_BSC","pcu_id")
	pcum_id=gemuConfigfile.get("Test_Environment_BSC","pcum_id")
	pidm_ip=gemuConfigfile.get("Test_Environment_BSC","pidm_ip")
	logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
        logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
        logFolderPath=logPath+logfolder
	num_of_VM=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_gemu_machines"))
        gemu_StartIp=gemuConfigfile.get("Test_Environment_GEMU","gemu_machine_start_ip")
        num_of_Ips_PerVM=int(gemuConfigfile.get("Test_Environment_GEMU","number_of_bcf_per_machine"))
        #num_of_Ips_PerVM=gemuConfigfile.get("Test_Environment_GEMU","number_of_bcf_per_machine")
        print totalNumOfBcf,numberOfBtsPerBCF,num_of_VM
        print bsc_type,gemu_StartIp
	num_of_VM=num_of_VM+1
	totalNumOfBcf=totalNumOfBcf+1
	numberOfBtsPerBCF=numberOfBtsPerBCF+1	
	print totalNumOfBcf,numberOfBtsPerBCF
	print bsc_type
   	bscType=""
	state='DISABLE'
	print memoryLeakState
    	if memoryLeakState[1] =="PRE":
		print("inside pre")
		telnetFunction(bscIp)
		genaTogling('N',totalNumOfBcf,numberOfBtsPerBCF)
		time.sleep(20)
		elgStateChange('DISABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
		time.sleep(120)

		bufferReading('pq_mem_pre1.txt',bcsu_id,pcum_id,logFolderPath)
		telnetFunction(bscIp)
		genaTogling('Y',totalNumOfBcf,numberOfBtsPerBCF)
		time.sleep(120)
                bufferReading('pq_mem_pre2.txt',bcsu_id,pcum_id,logFolderPath)

		elgStateChange('ENABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
		time.sleep(20)

						        	
    	if memoryLeakState[1]=="POST":
        	print("inside post")
                elgStateChange('DISABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
                time.sleep(120)
		telnetFunction(bscIp)
                bufferReading('pq_mem_post1.txt',bcsu_id,pcum_id,logFolderPath)

		telnetFunction(bscIp)
                genaTogling('N',totalNumOfBcf,numberOfBtsPerBCF)
                time.sleep(120)

                bufferReading('pq_mem_post2.txt',bcsu_id,pcum_id,logFolderPath)
		
		telnetFunction(bscIp)
		genaTogling('Y',totalNumOfBcf,numberOfBtsPerBCF)
		time.sleep(20)

                elgStateChange('ENABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
                time.sleep(20)

