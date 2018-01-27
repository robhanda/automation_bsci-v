import  os,sys,telnetlib,getpass,paramiko,time

def findalivemachines():
	#ip = raw_input("enter the ip of machine:")
	#print ip
	text_file = open("/root/variables.txt","r+")
        ip_line=text_file.readline()
	ip=ip_line.split("=")[1].strip()
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
def creatingcommands():
		# code to read .txt file having user inputs

	#print "reading a file"

	text_file = open("/root/variables.txt","r+")
	dummy=text_file.readline()
	dummy2=text_file.readline()
	interface_line=text_file.readline()
	interface=interface_line.split("=")[1].strip()
	gemu_path_line= text_file.readline()
	gemu_path=gemu_path_line.split("=")[1].strip()
	bts_type_line= text_file.readline()
	bts_type=bts_type_line.split("=")[1].strip()
	numberofbcf_line=text_file.readline()
	numberofbcf=numberofbcf_line.split("=")[1].strip()
	bcf=int(numberofbcf)
	text_file.close()

	#print interface,gemu_path,bts_type,numberofbcf



	#print interface,gemu_path,bts_type,bcf
	first_command = "LT_SET CONF\rEOF\r\n"
	cmd = []
	# Now program for for creating commands and saving those in list
	cmd.append(first_command)
	#print cmd
	#print interface



	for i in range(0,bcf):

    		if(i==0):
        	# GTE commnad for BCF-1
        		cmd1= "LT_SET BIN "+str(interface)+" "+"0"+" " +str(gemu_path)+"/bcf struct_2g.db 0 "+str(bts_type)+" NULL"
        		#print cmd1
       			cmd2=cmd1.replace("\n","")
			cmd3=cmd2.replace("\r","")
			cmd3=cmd3.replace("\r\n","")
     			#print"inside if loop"
        		#print cmd3
       			cmd.append(cmd3)
			cmd3= "LT_SET BIN ELG"+" " + str(i)+" "+ str(gemu_path)+"/bcf"+ " /root/gte/profile/egprs.conf /root/gte/profile/egprs_test.tcl"+" " +str(i)+" " +  "NULL NULL"
		        cmd3=cmd3.replace("\r\n","")

        		#cmd4= "LT_SET BIN ELG 1 /home/gprs3gemulator-5.5.10-corr1/bcf /root/gte/profile/ps.conf /root/gte/profile/dt_test.tcl 0 NULL NULL"
        		i=i+1
       			cmd.append(cmd3)
     			#cmd.append(cmd4)


    		else:

        	# GTE commnad for BCF-2,3,4
        		cmd1= "LT_SET BIN "+str(interface)+" "+ str(i) +" " +str(gemu_path)+"/bcf_"+str(i)+" struct_2g.db 0 "+str(bts_type)+" NULL"
        		#print cmd1
      		 	#print i
        		cmd2=cmd1.replace("\n","")
			cmd2=cmd2.replace("\r","")
			cmd2=cmd2.replace("\r\n","")
        		#print"inside else loop"
        		#print cmd2
      		  	cmd.append(cmd2)
        		cmd3= "LT_SET BIN ELG"+" " + str(i)+" "+ str(gemu_path)+"/bcf_"+str(i)+ " /root/gte/profile/egprs.conf /root/gte/profile/egprs_test.tcl"+" " +str(i)+" " +  "NULL NULL"
        		#cmd4= "LT_SET BIN ELG" + str(i)+ str(gemu_path)+"/bcf_"+str(i)+"/MS6 /root/gte/profile/ps.conf /root/gte/profile/dt_test.tcl"+"" +str(i)+""+  "NULL NULL"
        		#print cmd3
			cmd3=cmd3.replace("\r\n","")
        		cmd.append(cmd3)
    	    		#print cmd4
       		 	#cmd.append(cmd4)
			#cmd=cmd.replace("\r\n","")


	cmd5= "LT_START"
	cmd.append(cmd5)

        for j in range(0,4):
   		#print"in 2nd for loop"
    		cmd6= "LT_ENABLE ELG"+" "+str(j)
   		cmd.append(cmd6)


	return  cmd
	
if __name__ == "__main__":
	hostname=[]
	hostname=findalivemachines()
	print hostname
	bcfcommands=[]
	bcfcommands=creatingcommands()
	#a=["LT_STATUS","LT_STATUS"]
	print bcfcommands
	port = 7031
	for j in hostname:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(j, port=22, username='root', password='password')
              	while True:
		       try:	
		
		  		stdin, stdout, stderr = ssh.exec_command('cd /root/gte; killall process_manager.tcl;./recover.tcl;echo $?;')
				time.sleep(35)
				t = telnetlib.Telnet(j,port)
				d = t.read_until(b'GEMU>',10)
				for cmd in bcfcommands:
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

















