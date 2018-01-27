##############################################################################################################################
# file name   : Pcums_process_running_check.py
# date        : 12-08-2017
# author      : Pavan Kumar
# version     : 0.1
# description : To check PCUMS process running or not in all machine.
		#Three Functions are used 
		#a>main fun() ****this will log the output of LT_STATUS****
		#b>pcums_check() ****this function will open the log file and check the PCUMS process is running or not
		#c>recovery_process() ****it will fire the recovery command if PCUMS process is not working
#################################################################################################################################
#!/usr/bin/env python
import os,sys,telnetlib,getpass,paramiko,time
import subprocess
variable_file = open("/home/Automation/parameters/variables.txt","r+")
ip_line=variable_file.readline()
ip=ip_line.split("=")[1].strip()
machine_line=variable_file.readline()
machine=machine_line.split("=")[1].strip()
machine = int(machine)
hostname=[]
ip_parts = ip.split(".")
ip_parts = [int(part) for part in ip_parts]

def main_fun():           #/////***this function will login into the machine and capture the output of LT_STATUS****//////
	first, second, third,fourth = ip_parts
	global text_file_update
	global text_file
	global bcf
	global lt_Status
	global lt_status_file
	global text_file_line
	global port
	for bcf in xrange (machine):
        	complete_ip=str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)
        	hostname.append(complete_ip)
		port = 7031
		t = telnetlib.Telnet(hostname[bcf],port)
		t.read_until(b'GEMU>',10)
		cmd="LT_STATUS"
		s = t.write(cmd+"\r")
		time.sleep(10)
		lt_Status=t.read_until(b'GEMU>',10)
		lt_status_file = open('/home/Automation/logs/LT_STATUS_OUTPUT.txt', 'w')
		lt_status_file.write(lt_Status)
		lt_status_file.close()
		pcums_check()	
		fourth=fourth+4
		print hostname
		t.close
def pcums_check():                             # ///***This function will login into the machine and will start the receovery process if PCUMs is not working***/////
	text_file = open("/home/Automation/logs/LT_STATUS_OUTPUT.txt","r+")
        text_file_line = text_file.read()
        text_file_update = text_file_line.strip()

	for i in range(0,4):
        	if ("PCUMS%d running"%i) in text_file_update:
                	print ("PCUMS%d running"%i)
			
		else:
			print ("PCUMS%d not running"%i)
			time.sleep(15)
			print("recovery commands starting")
			recovery_process()
			t = telnetlib.Telnet(hostname[bcf],port)
			t.read_until(b'GEMU>',10)
	                cmd="LT_STATUS"
        	        s = t.write(cmd+"\r")
                	time.sleep(10)
			lt_Status=t.read_until(b'GEMU>',10)
                	lt_status_file = open('/home/Automation/logs/LT_STATUS_OUTPUT.txt', 'w')
                	lt_status_file.write(lt_Status)
                	lt_status_file.close()
                	text_file = open("/home/Automation/logs//LT_STATUS_OUTPUT.txt","r+")
                	text_file_line = text_file.read()
                	text_file_update = text_file_line.strip()
			time.sleep(20)			
			if ("PCUMS%d not running"%i) in text_file_update:
				recovery_process()
			elif ("PCUMS%d running"%i) in text_file_update:
				print ("PCUMS%d are running"%i)
				#	print ("PCUMS%d running"%i)
			else:
				print ("recovery done for two times, error in PCUMS%d check manually"%i)
 		
def recovery_process():	
	ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname[bcf], port=22, username='root', password='password')
        stdin, stdout, stderr = ssh.exec_command('cd /root/gte; killall process_manager.tcl;./recover.tcl;echo $?;')
        time.sleep(50)
        print("recovery commands fired")
	
main_fun()

