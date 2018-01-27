import sys,os,time,paramiko,ConfigParser


def formattingfiles(logFolderPath,bsctype,logServerIp):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(logServerIp, port=22, username='root', password='password')

        if(bsctype=="mcbsc"):
                # this function reads pq_mem_pre1 files generted by script and removes all the garbage from it to make it readable by program
                #pre1- gena=N,pre2-gena=y,post1-gena=y,post2-gena=n ,pre1 and post-2 and pre2 and post1 has to be compared
                cmd1='sed "s/\<INTERNAL POOLS\>//g"'+ ' '+logFolderPath+'/'+'pq_mem_pre1.txt > '+logFolderPath+'/pre1A.txt'
                cmd2='sed "s/\<INTERNAL POOLS\>//g"'+ ' '+logFolderPath+'/'+'pq_mem_pre2.txt > '+logFolderPath+'/pre2A.txt'
                cmd3='sed "s/\<INTERNAL POOLS\>//g"'+ ' '+logFolderPath+'/'+'pq_mem_post1.txt > '+logFolderPath+'/post1A.txt'
                cmd4='sed "s/\<INTERNAL POOLS\>//g"'+ ' '+logFolderPath+'/'+'pq_mem_post2.txt > '+logFolderPath+'/post2A.txt'
		print cmd1

                stdin, stdout, stderr = ssh.exec_command(cmd1)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd2)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd3)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd4)


                cmd1='sed "/Total/d"'+ ' '+logFolderPath+'/'+'pre1A.txt > '+logFolderPath+'/pre1B.txt'
                cmd2='sed "/Total/d"'+ ' '+logFolderPath+'/'+'pre2A.txt > '+logFolderPath+'/pre2B.txt'
                cmd3='sed "/Total/d"'+ ' '+logFolderPath+'/'+'post1A.txt > '+logFolderPath+'/post1B.txt'
                cmd4='sed "/Total/d"'+ ' '+logFolderPath+'/'+'post2A.txt > '+logFolderPath+'/post2B.txt'

                stdin, stdout, stderr = ssh.exec_command(cmd1)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd2)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd3)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd4)


                cmd1='grep "buffers" -A 23'+ ' '+logFolderPath+'/'+'pre1B.txt > '+logFolderPath+'/pre1.txt'
                cmd2='grep "buffers" -A 23'+ ' '+logFolderPath+'/'+'pre2B.txt > '+logFolderPath+'/pre2.txt'
                cmd3='grep "buffers" -A 23'+ ' '+logFolderPath+'/'+'post1B.txt > '+logFolderPath+'/post1.txt'
                cmd4='grep "buffers" -A 23'+ ' '+logFolderPath+'/'+'post2B.txt > '+logFolderPath+'/post2.txt'
                print cmd1
                stdin, stdout, stderr = ssh.exec_command(cmd1)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd2)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd3)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd4)
                time.sleep(5)
                cmd5='cd'+' '+logFolderPath+";"+'rm -rf post1A.txt post1B.txt  post2A.txt post2B.txt pre1A.txt pre1B.txt pre2A.txt pre2B.txt'
                print cmd5
                stdin, stdout, stderr = ssh.exec_command(cmd5)
                ssh.close()
        else:

                cmd1='grep "Current" -A 30'+ ' '+logFolderPath+'/'+'pq_mem_pre1.txt > '+logFolderPath+'/pre1.txt'
                cmd2='grep "Current" -A 30'+ ' '+logFolderPath+'/'+'pq_mem_pre2.txt > '+logFolderPath+'/pre2.txt'
                cmd3='grep "Current" -A 30'+ ' '+logFolderPath+'/'+'pq_mem_post1.txt > '+logFolderPath+'/post1.txt'
                cmd4='grep "Current" -A 30'+ ' '+logFolderPath+'/'+'pq_mem_post2.txt > '+logFolderPath+'/post2.txt'
                print cmd1
                stdin, stdout, stderr = ssh.exec_command(cmd1)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd2)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd3)
                time.sleep(5)
                stdin, stdout, stderr = ssh.exec_command(cmd4)
                time.sleep(5)

                os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_pre1.txt>/home/Automation/memoryleak/pre1.txt')
                os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_post2.txt>/home/Automation/memoryleak/post2.txt')
                os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_pre2.txt>/home/Automation/memoryleak/pre2.txt')
                os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_post1.txt>/home/Automation/memoryleak/post1.txt')
                ssh.close()




def readingcolumns(file):
#	print file
	busy_buffer=[]
	free_buffer=[]
	buffer_size=[]
	lines=file.readlines()
	#First program is reading all the lines,each line is seperated by , 
	for line in lines:
		splited_line=line.split()
		# each element of each line is splitted
        	temp = []
		# if statement removes free spaces
		if(len(splited_line) > 0):
	        	for char in splited_line:
			# second if statement removes free spaces inside line
				if len(char)>0:
					temp.append(char)
		# this if statement removes dotted line
			if len(temp)>1:
				buffer_size.append(temp[1])
		    		busy_buffer.append(temp[1])	
		    		free_buffer.append(temp[2])	
	return(busy_buffer,free_buffer,buffer_size)
	file.close()


def comparison_of_buffers(file,initial_buffer,final_buffer,buffer_size):
#	print("initial buffer is %s"%initial_buffer)
#	print("final buffer is %s"%final_buffer)
	template=[]
	template=["buffer_size","\t","buffer_initial","\t\t","buffer_final","\t","difference","\t","result"]
	counter=0
	for material in template:
        	file.write(material)
	file.write("\n")
	for i,j,k in zip(initial_buffer,final_buffer,buffer_size):
        	if i!=j:
                	print("\n following buffers are not matching \n")
                	print i
              	  	print j
			diff=int(i)-int(j)
			print("difference between the initial and final busy buffer is%d"% diff)
			if(abs(diff)>2):
				res="memory leak"
			else:
				res="stable"
			file.write( k+ '\t')
                	file.write('\t\t'+ i+ '\t\t')
                	file.write(j+'\t\t')
			diff=str(diff)
			file.write(diff + '\t\t')
			file.write(res + '\n')
                	counter=counter+1
	print("in both the files total %d lines were not matching"%counter)
	

if __name__ == "__main__":

	gemuConfigfile = ConfigParser.ConfigParser()
        gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
        logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
        logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
        logServerIp=gemuConfigfile.get("Test_Environment_GEMU","logserver_ip")
        bsctype=gemuConfigfile.get("Test_Environment_BSC","bsc_type")
        logFolderPath=logPath+logfolder
        print logFolderPath,bsctype
	formattingfiles(logFolderPath,bsctype,logServerIp)
	file1Path=logFolderPath+'/'+'pre1.txt'
	file2Path=logFolderPath+'/'+'post2.txt'
	file3Path=logFolderPath+'/'+'pre2.txt'
	file4Path=logFolderPath+'/'+'post1.txt'
	print file1Path
	file1=open(file1Path,'r+')
	file2=open(file2Path,'r+')
	file3=open(file3Path,'r+')
	file4=open(file4Path,'r+')

	file5Path=logFolderPath+'/'+'busybuffers_comparison_gena-NO.txt'
        file6Path=logFolderPath+'/'+'freebuffers_comparison_gena-NO.txt'
        file7Path=logFolderPath+'/'+'busybuffers_comparison_gena-yes.txt'
        file8Path=logFolderPath+'/'+'freebuffers_comparison_gena-yes.txt'
	file5=open(file5Path,'w')
        file6=open(file6Path,'w')
        file7=open(file7Path,'w')
        file8=open(file8Path,'w')


#	formattingfiles(logFolderPath,bsctype,logServerIp)
	busy_buffer_initial=[]
	free_buffer_initial=[]
	busy_buffer_final=[]
	free_buffer_final=[]
	buffer_size=[]
	print(" \n\n comparison of pre and post files when GENA=N")
	print("calling function 1-reading busy buffers of both the files")
	# In pre1 file busy buffer and free buffer columns will be read and stored in list
	busy_buffer_initial,free_buffer_initial,buffer_size=readingcolumns(file1)
#	print busy_buffer_initial
#	print free_buffer_initial

	print("calling function 2-reading free buffers of both the files")

	busy_buffer_final,free_buffer_final,buffer_size=readingcolumns(file2)
	# this function compares the buffers and write those buffers as well as their difference in file
#	print busy_buffer_final
#	print free_buffer_final

	comparison_of_buffers(file5,busy_buffer_initial,busy_buffer_final,buffer_size)
	comparison_of_buffers(file6,free_buffer_initial,free_buffer_final,buffer_size)
		




	print("\n\n comparison of pre and post files when GENA=Y")

        print("calling function -reading busy buffers of both the files")

        busy_buffer_initial,free_buffer_initial,buffer_size=readingcolumns(file3)
        print("calling function 2-reading free buffers of both the files")

        busy_buffer_final,free_buffer_final,buffer_size=readingcolumns(file4)
        comparison_of_buffers(file7,busy_buffer_initial,busy_buffer_final,buffer_size)
        comparison_of_buffers(file8,free_buffer_initial,free_buffer_final,buffer_size)


	file5.close
	file6.close
	file7.close
        file8.close







