##############################################################################################################################
# file name   : post_memory_check.py
# date        : 20-08-2017
# author      : Pavan Kumar
# version     : 0.1
## description : To check memory check of PQ and DSP after the test case (i.e. Post memory readings)
                #a> reading the memory run just after the test case, it means stop the elg macro and take the reading while GENA is Y
                #b> Second reading Disbale the GENA and take the meamory readings.
#################################################################################################################################
#!/usr/bin/env python
import os,sys,telnetlib,getpass,paramiko,time
import subprocess
import re
sys.path.insert(0,'/home/Automation/parameters/')
import input_file
#sys.path.append("/home/Automation/parameters/input_file")
#import /home/Automation/parameters/input_file
def telnetFunction():
	global telnetBsc
	global expectedBscLine
	expectedBscLine = "BASE TRANSCEIVER STATION HANDLING IN BSC COMMAND <EQ_>" 
        telnetBsc = telnetlib.Telnet(input_file.bsc_ip)
	telnetBsc.read_until(b'ENTER USERNAME <',5)
	username="SYSTEM"
	telnetBsc.write(username+"\r")
	telnetBsc.read_until(b'ENTER PASSWORD <',5)
	password="SYSTEM"
	telnetBsc.write(password+"\r")
	telnetBsc.read_until(b'MAIN LEVEL COMMAND <___>',5)
	telnetBsc.read_until(b'<',5)
def genaDisable():
	for bcf in range(1,input_file.no_of_bcf):
		for bts in range (1,input_file.bts_per_bcf):
			btsGenaState=("ZEQO:BTS=%d%d:GPRS;"%(bcf,bts))
			telnetBsc.write(btsGenaState+'\n\r')
			telnetBsc.read_until(b'expectedBscLine',5)
			btsLock=("ZEQS:BTS=%d%d:L;"%(bcf,bts))
			telnetBsc.write(btsLock+'\n\r')
			time.sleep(10)
			telnetBsc.read_until(b'expectedBscLine',5)
                	btsGenaDisable=("ZEQV:BTS=%d%d:GENA=N;"%(bcf,bts))
                	telnetBsc.write(btsGenaDisable+'\n\r')
                	time.sleep(15)
			telnetBsc.read_until(b'expectedBscLine',5)
                	btsUnlock=("ZEQS:BTS=%d%d:U;"%(bcf,bts))
               		telnetBsc.write(btsUnlock+'\n\r')
                	time.sleep(10)
			telnetBsc.read_until(b'expectedBscLine',5)

def memleakCommandafterGenaDisable():
	if input_file.bsc_type == "Flexi":
		telnetBsc.read_until(b'expectedBscLine',10)
		cmd=("ZDDS:BCSU,%s,,PCU2,%s:;"%(input_file.bcsu_id,input_file.pcu_id))
		telnetBsc.write(cmd+'\n\r')
		telnetBsc.read_until(b'OSE>',10)
		output_file1 = open('/home/Automation/memoryleak/pq_mem_post2.txt','w+')
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
		telnetBsc.read_until(b'REMOTE DEBUGGER SESSION COMMAND <DD_>',5)
		output_file1.close()
	else:
		telnetBsc.read_until(b'expectedBscLine',5)
	        pcumLogin=("ZDDS:PCUM,%s:;"%input_file.pcum_id)
	        global var
		var=input_file.pidm_ip
        	telnetBsc.write(cmd+'\n\r')
        	telnetBsc.read_until(b'var>',10)
        	output_file1 = open('/home/Automation/memoryleak/pq_mem_post2.txt','w+')
        	pcumVersion = "ssv"
        	telnetBsc.write(pcumVersion+'\r')
        	outputpcumVersion=telnetBsc.read_until(b'var>',10)
        	print outputpcumVersion
        	output_file1.write(outputpcumVersion)
        	pcumPqMem="dbu pq2"
        	telnetBsc.write(pcumPqMem+'\r')
        	outputpcumPqMem=telnetBsc.read_until(b'var>',5)
		print outputpcumPqMem
        	output_file1.write(outputpcumPqMem)
        	pcumDspMem="dbu dsp:all"
        	print pcumDspMem
        	telnetBsc.write(pcumDspMem+'\r')
        	outputpcumDspMem=telnetBsc.read_until(b'var>',5)
        	print outputpcumDspMem
        	output_file1.write(outputpcumDspMem)
        	cmdx="exit"
		print cmdx
        	telnetBsc.write(cmdx+'\r')
        	telnetBsc.read_until(b'REMOTE DEBUGGER SESSION COMMAND <DD_>',5)
		telnetBsc.close
		output_file1.close()

		print "Please waite for 5 min"
		time.sleep(300)
	

def genaEnable():
	for bcf in range(1,input_file.no_of_bcf):
        	for bts in range (1,input_file.bts_per_bcf):
                	btsGenaState=("ZEQO:BTS=%d%d:GPRS;"%(bcf,bts))
                	telnetBsc.write(btsGenaState+'\n\r')
			telnetBsc.read_until(b'expectedBscLine',5)
			btsLock=("ZEQS:BTS=%d%d:L;"%(bcf,bts))
			telnetBsc.write(btsLock+'\n\r')
                	time.sleep(10)
			telnetBsc.read_until(b'expectedBscLine',5)
			btsGenaEnable=("ZEQV:BTS=%d%d:GENA=Y;"%(bcf,bts))
			telnetBsc.write(btsGenaEnable+'\n\r')
               		time.sleep(15)
			telnetBsc.read_until(b'expectedBscLine',5)
                	btsUnlock=("ZEQS:BTS=%d%d:U;"%(bcf,bts))
			telnetBsc.write(btsUnlock+'\n\r')
			time.sleep(10)
                	telnetBsc.read_until(b'expectedBscLine',5)
                	time.sleep(5)

def memleakCommandwhenGenaEnable():
	if input_file.bsc_type == "Flexi":
		telnetBsc.read_until(b'expectedBscLine',10)
		cmd=("ZDDS:BCSU,%s,,PCU2,%s:;"%(input_file.bcsu_id,input_file.pcu_id))
		telnetBsc.write(cmd+'\n\r')
		telnetBsc.read_until(b'OSE>',10)
		output_file1 = open('/home/Automation/memoryleak/pq_mem_post1.txt','w+')
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
		telnetBsc.read_until(b'expectedBscLine',10)
        	pcumLogin=("ZDDS:PCUM,%s:;"%input_file.pcum_id)
        	telnetBsc.read_until(b'var>',10)
        	telnetBsc.write(pcumLogin+'\n\r')
        	telnetBsc.read_until(b'var>',10)
        	output_file1 = open('/home/Automation/memoryleak/pq_mem_post1.txt','w+')
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
		time.sleep(300)


def findalivemachines():
        #ip = raw_input("enter the ip of machine:")
        #print ip
        text_file = open("/home/Automation/parameters/variables.txt","r+")
        ip_line=text_file.readline()
        ip=ip_line.split("=")[1].strip()
        print ip_line
        #print ip
        machine_line=text_file.readline()
        machine=machine_line.split("=")[1].strip()
        machines=int(machine)
        text_file.close()
        machines=machines+1
        ip_parts = ip.split(".")
        ip_parts = [int(part) for part in ip_parts]
        first, second, third, fourth = ip_parts

        #print first, second, third, fourth
        hostname=[]
#last_ip = ip + 3

        for i in range(1,machines):

                result = os.system("ping -c 2 " +str(first)+"."+str(second)+"."+str(third)+"."+str(fourth))

                #fourth= fourth +4

                if result == 0:
                        #print("ip %s is pinging" %i)
                        comp_ip=str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)
                        #print comp_ip
                        hostname.append(comp_ip)


                else:
                        print("ip %s is not pinging" %i)

                fourth=fourth+4
        return hostname


def dis_creatingcommands():
                # code to read .txt file having user inputs

        #print "reading a file"

        text_file = open("/home/Automation/parameters/variables.txt","r+")
        dummy=text_file.readline()
#       dummy2=text_file.readline()
        interface_line=text_file.readline()
        interface=interface_line.split("=")[1].strip()
        gemu_path_line= text_file.readline()
        gemu_path=gemu_path_line.split("=")[1].strip()
        bts_type_line= text_file.readline()
        bts_type=bts_type_line.split("=")[1].strip()
        numberofbcf_line=text_file.readline()
        numberofbcf=numberofbcf_line.split("=")[1].strip()
        bcf=int(numberofbcf)
        numberofbcf_line=text_file.readline()
        numberofbcf=numberofbcf_line.split("=")[1].strip()
        print numberofbcf
        elgprocess_line=text_file.readline()
        print elgprocess_line
        process=elgprocess_line.split("=")[1].strip()
        print process
        text_file.close()



        #first_command = "LT_SET CONF\rEOF\r\n"
        cmd = []
       # cmd.append(first_command)



        if(process=="mixed"):
                for j in range(0,8):
                        #print"in 2nd for loop"
                        cmd6= "LT_DISABLE ELG"+" "+str(j)
                        cmd.append(cmd6)

	else:
                for j in range(0,2):
                        #print"in 2nd for loop"
                        cmd6= "LT_DISABLE ELG"+" "+str(j)
                        cmd.append(cmd6)
        return  cmd



def dis_commandfiring():
        hostname=[]
        hostname=findalivemachines()
        print hostname

        bcfcommands=[]
        bcfcommands=dis_creatingcommands()
        #a=["LT_STATUS","LT_STATUS"]
        print bcfcommands
        port = 7031
        for j in hostname:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(j, port=22, username='root', password='password')
                while True:
                       try:

                                t = telnetlib.Telnet(j,port)
                                d = t.read_until(b'GEMU>',10)
                                for cmd in bcfcommands:
                                                print cmd
                                                s = t.write(cmd+"\r")
                                                print s
                                                time.sleep(5)
                                                d = t.read_until(b'GEMU>', 10)
                                                print d
                                                t.close
                                break
                       except KeyboardInterrupt:
                                                break
                       except:
                                pass

def enable_creatingcommands():
                # code to read .txt file having user inputs

        #print "reading a file"

        text_file = open("/home/Automation/parameters/variables.txt","r+")
        dummy=text_file.readline()
#       dummy2=text_file.readline()
        interface_line=text_file.readline()
        interface=interface_line.split("=")[1].strip()
        gemu_path_line= text_file.readline()
        gemu_path=gemu_path_line.split("=")[1].strip()
        bts_type_line= text_file.readline()
        bts_type=bts_type_line.split("=")[1].strip()
        numberofbcf_line=text_file.readline()
        numberofbcf=numberofbcf_line.split("=")[1].strip()
        bcf=int(numberofbcf)
        numberofbcf_line=text_file.readline()
        numberofbcf=numberofbcf_line.split("=")[1].strip()
        print numberofbcf
        elgprocess_line=text_file.readline()
        print elgprocess_line
        process=elgprocess_line.split("=")[1].strip()
        print process
        text_file.close()



      #  first_command = "LT_SET CONF\rEOF\r\n"
        cmd = []
      #  cmd.append(first_command)



        if(process=="mixed"):
                for j in range(0,8):
                        #print"in 2nd for loop"
                        cmd6= "LT_ENABLE ELG"+" "+str(j)
                        cmd.append(cmd6)

        else:
                for j in range(0,2):
                        #print"in 2nd for loop"
                        cmd6= "LT_ENABLE ELG"+" "+str(j)
			cmd.append(cmd6)
        return  cmd

		

def enable_commandfiring():
        hostname=[]
        hostname=findalivemachines()
        print hostname

        bcfcommands=[]
        bcfcommands=enable_creatingcommands()
        #a=["LT_STATUS","LT_STATUS"]
        print bcfcommands
        port = 7031
        for j in hostname:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(j, port=22, username='root', password='password')
                while True:
                       try:

                                t = telnetlib.Telnet(j,port)
                                d = t.read_until(b'GEMU>',10)
                                for cmd in bcfcommands:
                                                print cmd
                                                s = t.write(cmd+"\r")
                                                print s
                                                time.sleep(5)
                                                d = t.read_until(b'GEMU>', 10)
                                                print d
                                                t.close
                                break
                       except KeyboardInterrupt:
                                                break
                       except:
                                pass
			


if __name__ == "__main__":
	print("executing post memory leak script")
	dis_commandfiring()
	time.sleep(120)
	telnetFunction()
	memleakCommandwhenGenaEnable()
	telnetFunction()
	genaDisable()
	time.sleep(60)
	memleakCommandafterGenaDisable()
	genaEnable()
	enable_commandfiring()
	time.sleep(120)







