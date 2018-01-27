import sys,os,ConfigParser,telnetlib,paramiko,getpass,time

def telnetFunction(bscIp):
        global telnetBsc
        global expectedBscLine
	print bscIp
        expectedBscLine = "BASE TRANSCEIVER STATION HANDLING IN BSC COMMAND <EQ_>"
        telnetBsc = telnetlib.Telnet(bscIp)
        telnetBsc.read_until(b'ENTER USERNAME <',5)
        username="SYSTEM"
        telnetBsc.write(username+"\r")
        telnetBsc.read_until(b'ENTER PASSWORD <',5)
        password="SYSTEM"
        telnetBsc.write(password+"\r")
        telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
        telnetBsc.read_until(b'<',5)



def genaTogling(genaState,totalNumOfBcf,numberOfBtsPerBCF):
	global telnetBsc
	global btsLock,btsGenaDisable,btsUnlock,btsGenaState,username,password
	
	for bcf in range(1,totalNumOfBcf):
                for bts in range (1,numberOfBtsPerBCF):
			
			telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
			telnetBsc.read_until(b'<',5)
                        btsGenaState=("ZEQO:BTS=%d%d:GPRS;"%(bcf,bts))
                        telnetBsc.write(btsGenaState+'\r\n')
                        telnetBsc.read_until(b'expectedBscLine',5)
                        btsLock=("ZEQS:BTS=%d%d:L;"%(bcf,bts))
			print btsLock
                        telnetBsc.write(btsLock+'\r\n')
                        time.sleep(10)
                        telnetBsc.read_until(b'expectedBscLine',5)
                        btsGenaDisable=("ZEQV:BTS=%d%d:GENA=%s;"%(bcf,bts,genaState))
                        telnetBsc.write(btsGenaDisable+'\r\n')
                        time.sleep(15)
                        telnetBsc.read_until(b'expectedBscLine',5)
                        btsUnlock=("ZEQS:BTS=%d%d:U;"%(bcf,bts))
                        telnetBsc.write(btsUnlock+'\r\n')
                        time.sleep(10)
                        telnetBsc.read_until(b'expectedBscLine',5)
#	telnetBsc.close()


def bufferReading(bsc_type,fileName,bcsu_id,pcu_id,logFolderPath):
	print bcsu_id,pcu_id,logFolderPath
#	global telnetBsc
	print bsc_type,fileName
#	telnetBsc = telnetlib.Telnet(bscIp)
	if bsc_type=="Flexi":
		print("inside if")
		telnetBsc.read_until(b'expectedBscLine',10)
		cmd=("ZDDS:BCSU,%s,,PCU2,%s:;"%(bcsu_id,pcu_id))
		telnetBsc.write(cmd+'\n\r')
		telnetBsc.read_until(b'OSE>',10)
		outputfile=logFolderPath+'/'+fileName
		print ("o/p file is %s",outputfile)
		output_file1 = open(outputfile,'w+')
		pcuVersion="ssv"
		telnetBsc.write(pcuVersion+'\r')
		outputpcuVersion=telnetBsc.read_until(b'OSE>',10)
		print outputpcuVersion
		output_file1.write(outputpcuVersion)
		pqMem="dbu pq2"
		telnetBsc.write(pqMem+'\r')
		outputpqMem=telnetBsc.read_until(b'OSE>',10)
		print outputpqMem
		output_file1.write(outputpqMem)
		for i in range (0,6):
        		dspMem=("dbu dsp:%d"%i)
        		print dspMem
        		telnetBsc.write(dspMem+'\r')
        		outputdspMem=telnetBsc.read_until(b'OSE>',10)
        		print outputdspMem
        		output_file1.write(outputdspMem)
		cmdx="exit"
		telnetBsc.write(cmdx+'\r')
		telnetBsc.read_until(b'REMOTE DEBUGGER SESSION COMMAND <DD_>',10)
		output_file1.close()
	else:
		print("inside else")
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
        	pcumPqMem="dbu pq2"
        	telnetBsc.write(pcumPqMem+'\r')
        	outputpcumPqMem=telnetBsc.read_until(b'var>',10)
		print outputpcumPqMem
        	output_file1.write(outputpcumPqMem)
        	pcumDspMem="dbu dsp:all"
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
	cmd='LT_'+state+' '+'ELG ALL'
        for gemuMachine in range(1,num_of_VM):
                #hostname_list = ["180.144.75.73"]
                print gemu_StartIp
                
                port = 7031
               # print port
               # print num_of_Ips_PerVM
                t = telnetlib.Telnet(gemu_StartIp,port)
                t.read_until(b'GEMU>', 10)
                t.write(cmd+"\r")
		t.read_until(b'GEMU>', 10)
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
		time.sleep(120)
		elgStateChange('DISABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
		time.sleep(120)
		if bsc_type=="Flexi":

			bufferReading(bsc_type,'pq_mem_pre1.txt',bcsu_id,pcu_id,logFolderPath)
		else:
			bufferReading(bsc_type,'pq_mem_pre1.txt',bcsu_id,pcum_id,logFolderPath)
	
		telnetFunction(bscIp)
		genaTogling('Y',totalNumOfBcf,numberOfBtsPerBCF)
		time.sleep(120)
		if bsc_type=="Flexi":
			print("inside flexi-pre2 block")
                        bufferReading(bsc_type,'pq_mem_pre2.txt',bcsu_id,pcu_id,logFolderPath)
                else:
                        bufferReading(bsc_type,'pq_mem_pre2.txt',bcsu_id,pcum_id,logFolderPath)

		elgStateChange('ENABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
		time.sleep(120)


						        	
    	if memoryLeakState[1]=="POST":
        	print("inside post")
                elgStateChange('DISABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
                time.sleep(120)
		telnetFunction(bscIp)
                if bsc_type=="Flexi":

                        bufferReading(bsc_type,'pq_mem_post1.txt',bcsu_id,pcu_id,logFolderPath)
                else:
                        bufferReading(bsc_type,'pq_mem_post1.txt',bcsu_id,pcum_id,logFolderPath)

		telnetFunction(bscIp)
                genaTogling('N',totalNumOfBcf,numberOfBtsPerBCF)
                time.sleep(120)
                if bsc_type=="Flexi":

                        bufferReading(bsc_type,'pq_mem_post2.txt',bcsu_id,pcu_id,logFolderPath)
                else:
                        bufferReading(bsc_type,'pq_mem_post2.txt',bcsu_id,pcum_id,logFolderPath)
		
		telnetFunction(bscIp)
		genaTogling('Y',totalNumOfBcf,numberOfBtsPerBCF)
		time.sleep(120)

                elgStateChange('ENABLE',num_of_VM,gemu_StartIp,num_of_Ips_PerVM)
                time.sleep(120)


