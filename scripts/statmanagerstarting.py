

import os,sys,paramiko,telnetlib,time,ConfigParser

def statcommands(bscip,pcuip,pcunumOrbcsunum,instance):
	cmd=[]
	cmreadingPrompt="LT_SET CONF"
	cmd2="EOF"
	cmd3="LT_SET BIN BSCMEAS 0"+" "+bscip+" " +"SYSTEM SYSTEM /home/bscmeas/"
	cmd3a="LT_SET BIN BSCTSL 0"+" "+bscip+" " +"SYSTEM SYSTEM 10 NULL /home/bscmeas/"
	cmd3b="LT_SET BIN PCU2 0"+" "+pcuip+" " +"SYSTEM SYSTEM "+pcunumOrbcsunum+" null null E /home/bscmeas/"
	cmd4="LT_SET BIN GNUPLOT 0 /home/bscmeas/ DSP:1200x250+0+580,PQ:1200x250+0+580,RTSL:1200x250+0+580,TPGEN:1200x250+0+870,TPPA:1200x250+0+1160,MS:540x200+540+0,TBF:1200x250+0+290"
#	cmd4="LT_SET BIN GNUPLOT 0 /home/bscmeas/ TPGEN:540x200+540+480,TPARTP:540x200+0+720,TPPA:540x200+540+720"
	cmd5="LT_START"
	cmd6="LT_GLOBAL BSCMEAS display=:"+str(instance)
	cmd7="LT_GLOBAL GNUPLOT display=:"+str(instance)
	cmd8="LT_GLOBAL BSCMEAS meficodigits=4"
	cmd9="LT_GLOBAL GNUPLOT pngsize=1000x300"
	cmd.extend([cmreadingPrompt,cmd2,cmd3,cmd3a,cmd3b,cmd4,cmd5,cmd6,cmd7,cmd8,cmd9])
	return cmd

if __name__ == "__main__":
	gemuConfigfile = ConfigParser.ConfigParser()
    	gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
	bscip=gemuConfigfile.get("Test_Environment_BSC","bsc_omu_ip")
	pcuip=gemuConfigfile.get("Test_Environment_BSC","pcu_ip")
	pcunum=gemuConfigfile.get("Test_Environment_BSC","pcu_id")
	pcumnum=gemuConfigfile.get("Test_Environment_BSC","pcum_id")
	bcsunum=gemuConfigfile.get("Test_Environment_BSC","bcsu_id")
	vncinstance=gemuConfigfile.get("Test_Environment_BSC","vnc_instance")
	bsc_type=gemuConfigfile.get("Test_Environment_BSC","bsc_type")

	ip=gemuConfigfile.get("Test_Environment_BSC","statmanager_ip")


	first_cmd="LT_ENABLE stat_manager"	
	hostname=[]
        statManagercommands=[]
	if(bsc_type=="Flexi"):
        	statManagercommands=statcommands(bscip,pcuip,pcunum,vncinstance)
	else:
		statManagercommands=statcommands(bscip,pcuip,pcumnum,vncinstance)
        print statManagercommands
	first_port=7002
        port = 7001
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='root', password='password')
	stdin, stdout, stderr = ssh.exec_command('cd /home/bscmeas;rm -rf *  $?;')	
	i=0
	while True:
		try:
			print("inside first while loop")
			time.sleep(40)
			i=i+1
			if(i>7):
				print("telnet tried for 7 times")
				break
			telnetInstance = telnetlib.Telnet(ip,first_port)
			readingPrompt = telnetInstance.read_until(b'PROCESS>',10)
			firingTelnetcommand = telnetInstance.write("LT_DIE"+"\r")
			time.sleep(40)

			telnetInstance = telnetlib.Telnet(ip,first_port)
                        readingPrompt = telnetInstance.read_until(b'PROCESS>',10)

			print first_cmd
        		firingTelnetcommand = telnetInstance.write(first_cmd+"\r")
        		print firingTelnetcommand
        		time.sleep(10)
        		readingPrompt = telnetInstance.read_until(b'PROCESS>', 10)
        		print readingPrompt
        		telnetInstance.close
			break	
		
		except:
			pass

	time.sleep(20)
	while True:
		try:	
			print("inside second for loop")
			time.sleep(40)
			if(i>7):
                                print("telnet tried for 7 times")
                                break

			ssh = paramiko.SSHClient()
        		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        		ssh.connect(ip, port=22, username='root', password='password')
			telnetInstance = telnetlib.Telnet(ip,port)		 
			readingPrompt = telnetInstance.read_until(b'STAT>',10)
			firingTelnetcommand = telnetInstance.write("LT_DIE"+"\r")
			time.sleep(40)
			telnetInstance = telnetlib.Telnet(ip,port)
                        readingPrompt = telnetInstance.read_until(b'STAT>',10)
			
        		for cmd in statManagercommands:
                      		print cmd
                      		firingTelnetcommand = telnetInstance.write(cmd+"\r")
                      		print firingTelnetcommand
                      		time.sleep(10)
                      		readingPrompt = telnetInstance.read_until(b'STAT>', 10)
                      		print readingPrompt
                      		telnetInstance.close
		
			break
		except:
			pass




	










