################################################################################
# file name   : copy.py
# date        : 09-08-2017
# author      : Pavan Kumar
# version     : 0.1
# description : To copy all the macros from controller to all machine.
################################################################################
#!/usr/bin/env python
import os,sys
sys.path.insert(0,'/home/Automation/parameters/')
import input_file

#import /home/Automation/parameters/input_file
variable_file = open("/home/Automation/parameters/variables.txt","r+")
ip_line=variable_file.readline()
ip=ip_line.split("=")[1].strip()
machine_line=variable_file.readline()
machine=machine_line.split("=")[1].strip()
machine = int(machine)
machine=machine+1
hostname=[]
ip_parts = ip.split(".")
ip_parts = [int(part) for part in ip_parts]
first, second, third, fourth = ip_parts
for bcf in xrange (machine):
	complete_ip=str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)
	hostname.append(complete_ip)
	os.system("scp "+input_file.filePathegprs+" root@"+hostname[bcf]+":"+input_file.serverPathconf)
	os.system("scp "+input_file.filePathgprs+" root@"+hostname[bcf]+":"+input_file.serverPathconf)
	os.system("scp "+input_file.filePathegprstest+" root@"+hostname[bcf]+":"+input_file.serverPathconf)
	os.system("scp "+input_file.filePathgprstest+" root@"+hostname[bcf]+":"+input_file.serverPathconf)
	fourth=fourth+4	
	#print bcf
	#print hostname
no_of_bcf=machine*2
for bcf in xrange (no_of_bcf):
        ip_parts = ip.split(".")
        ip_parts = [int(part) for part in ip_parts]
        first, second, third, fourth = ip_parts
        fourth=fourth+bcf
        complete_ip=str(first)+"."+str(second)+"."+str(third)+"."+str(fourth)
        hostname.append(complete_ip)
        print hostname
        os.system("scp "+input_file.filePathelgmsmacro+" root@"+hostname[bcf]+":"+input_file.serverPath)
        os.system("scp "+input_file.filePathelgmsmacro+" root@"+hostname[bcf]+":"+input_file.serverPath1)
      #  os.system("scp "+input_file.filePathelgmsmacro+" root@"+hostname[bcf]+":"+input_file.serverPath2)
      #  os.system("scp "+input_file.filePathelgmsmacro+" root@"+hostname[bcf]+":"+input_file.serverPath3)
        #print bcf
	#print hostname




