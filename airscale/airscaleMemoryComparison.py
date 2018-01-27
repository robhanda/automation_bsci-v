import sys,os,time,paramiko,ConfigParser


def formattingfiles(logFolderPath,bsctype,logServerIp):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(logServerIp, port=22, username='root', password='password')

                # this function reads pq_mem_pre1 files generted by script and removes all the garbage from it to make it readable by program
         
       #pre1- gena=N,pre2-gena=y,post1-gena=y,post2-gena=n ,pre1 and post-2 and pre2 and post1 has to be compared
	
	

	
	
	
	
	cmd1="sed '/CHUNK/d' "+logFolderPath+'/'+'pq_mem_pre1.txt > '+logFolderPath+'/pre1A.txt'
	cmd2="sed '/CHUNK/d' "+logFolderPath+'/'+'pq_mem_pre2.txt > '+logFolderPath+'/pre2A.txt'
	cmd3="sed '/CHUNK/d' "+logFolderPath+'/'+'pq_mem_post1.txt > '+logFolderPath+'/post1A.txt'
	cmd4="sed '/CHUNK/d' "+logFolderPath+'/'+'pq_mem_post2.txt > '+logFolderPath+'/post2A.txt'
#        print cmd1
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd4)


		
	cmd1="awk '/ssv/ {c=15} c && c-- {next}1'"+ ' '+logFolderPath+'/'+'pre1A.txt > '+logFolderPath+'/pre1B.txt'
	cmd2="awk '/ssv/ {c=15} c && c-- {next}1'"+ ' '+logFolderPath+'/'+'pre2A.txt > '+logFolderPath+'/pre2B.txt'
	cmd3="awk '/ssv/ {c=15} c && c-- {next}1'"+ ' '+logFolderPath+'/'+'post1A.txt > '+logFolderPath+'/post1B.txt'
	cmd4="awk '/ssv/ {c=15} c && c-- {next}1'"+ ' '+logFolderPath+'/'+'post2A.txt > '+logFolderPath+'/post2B.txt'
#	print cmd1
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd4)

	cmd1= "sed -e 's/--//g' -e's/,//g' -e 's/INTERNAL POOLS//g' -e 's/POOL TYPE DPM_MEMPOOL//g' -e 's/%//g' "+' '+logFolderPath+'/'+'pre1B.txt > '+logFolderPath+'/pre1C.txt'
       	cmd2= "sed -e 's/--//g' -e's/,//g' -e 's/INTERNAL POOLS//g' -e 's/POOL TYPE DPM_MEMPOOL//g' -e 's/%//g'  "+' '+logFolderPath+'/'+'pre2B.txt > '+logFolderPath+'/pre2C.txt'
	cmd3= "sed -e 's/--//g' -e's/,//g' -e 's/INTERNAL POOLS//g' -e 's/POOL TYPE DPM_MEMPOOL//g' -e 's/%//g'  "+' '+logFolderPath+'/'+'post1B.txt > '+logFolderPath+'/post1C.txt'
	cmd4= "sed -e 's/--//g' -e's/,//g' -e 's/INTERNAL POOLS//g' -e 's/POOL TYPE DPM_MEMPOOL//g' -e 's/%//g'  "+' '+logFolderPath+'/'+'post2B.txt > '+logFolderPath+'/post2C.txt' 

#	print cmd1
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd4)
        time.sleep(5)

	cmd1='grep "buffers" -A 24'+ ' '+logFolderPath+'/'+'pre1C.txt > '+logFolderPath+'/pre1.txt'
        cmd2='grep "buffers" -A 24'+ ' '+logFolderPath+'/'+'pre2C.txt > '+logFolderPath+'/pre2.txt'
        cmd3='grep "buffers" -A 24'+ ' '+logFolderPath+'/'+'post1C.txt > '+logFolderPath+'/post1.txt'
        cmd4='grep "buffers" -A 24'+ ' '+logFolderPath+'/'+'post2C.txt > '+logFolderPath+'/post2.txt'
 #       print cmd1
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd4)
        time.sleep(5)
	'''
        cmd5='cd'+' '+logFolderPath+";"+'rm -rf post1A.txt post1B.txt pre1C.txt pre2C.txt post1C.txt post2C.txt  post2A.txt post2B.txt pre1A.txt pre1B.txt pre2A.txt pre2B.txt'
        print cmd5
        stdin, stdout, stderr = ssh.exec_command(cmd5)
	'''
        ssh.close()

def fpFileformatting(logFolderPath,logServerIp,poolid,numberofBuffersinPool):
	ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(logServerIp, port=22, username='root', password='password')

	cmd1='grep -w '+'"'+ 'POOL ID '+poolid+'"'+ ' -A '+ numberofBuffersinPool+ ' '+logFolderPath+'/'+'pre1C.txt > '+logFolderPath+'/pre1fp.txt'
	cmd2='grep -w '+'"'+ 'POOL ID '+poolid+'"'+ ' -A '+ numberofBuffersinPool+ ' '+logFolderPath+'/'+'pre2C.txt > '+logFolderPath+'/pre2fp.txt'
	cmd3='grep -w '+'"'+ 'POOL ID '+poolid+'"'+ ' -A '+ numberofBuffersinPool+ ' '+logFolderPath+'/'+'post1C.txt > '+logFolderPath+'/post1fp.txt'
	cmd4='grep -w '+'"'+ 'POOL ID '+poolid+'"'+ ' -A '+ numberofBuffersinPool+ ' '+logFolderPath+'/'+'post2C.txt > '+logFolderPath+'/post2fp.txt'
#	print cmd1
#	print ("this is command 4 print")

#	print cmd4
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd3)
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command(cmd4)
        time.sleep(5)

	ssh.close()


def readingcolumns(file):
#	print file
	busy_buffer=[]
	free_buffer=[]
	buffer_index=[]
	utilization=[]
	lines=file.readlines()
	#First program is reading all the lines,each line is seperated by , 
	for line in lines[1:]:
	#	print line
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
				buffer_index.append(temp[0])
		    		busy_buffer.append(temp[2])	
		    		free_buffer.append(temp[3])
				utilization.append(temp[5])
					
	return(busy_buffer,free_buffer,buffer_index,utilization)
#	file.close()


def comparison_of_buffers(file,initial_buffer,final_buffer,buffer_index):
#	print("initial buffer is %s"%initial_buffer)
#	print("final buffer is %s"%final_buffer)
	template=[]
	template=["index","\t\t\t","initial","\t\t\t","final","\t\t","difference","\t","result"]
	counter=0
	for material in template:
        	file.write(material)
	file.write("\n")
	for i,j,k in zip(initial_buffer,final_buffer,buffer_index):
        	if i!=j:
                	print("\n following buffers are not matching \n")
                	print i
              	  	print j
			diff=float(i)-float(j)
			print("difference between the initial and final busy buffer is%d"% diff)
			if(abs(diff)>1):
				res="memory leak"
			else:
				res="stable"
			file.write( k+ '\t')
                	file.write('\t\t'+ i+ '\t\t')
                	file.write(j+'\t\t')
			diff=str(diff)
			file.write(diff + '\t\t\t')
			file.write(res + '\n')
                	counter=counter+1
	print("in both the files total %d lines were not matching"%counter)
	
def searchElementinFile(filepath):
#	print("in search element function")
        file=open(filepath,'r')
#	print file
        for line in file:
		print line
                if "memory leak" in line:
			print("<---------->")
			file.close()
			return True
#	file.close()
	return False




def verdictFunction(file5Path,file6Path,file7Path,file8Path,mergedfp):
	print file5Path

        found=searchElementinFile(file5Path)
#	print found
        if(found==False):
                print("second file")
                found=searchElementinFile(file6Path)
#		print found
        if(found==False):
                print("3rd file")
                found=searchElementinFile(file7Path)
#		print found
        if(found==False):
                print("4th file")
                found=searchElementinFile(file8Path)
#		print found
	if(found==False):
                print("5th file")
                found=searchElementinFile(mergedfp)
#        	print found

        if(found==True):
                print("memory leak found")
        else:
                print("no memory leak found")
#        print found





if __name__ == "__main__":

	gemuConfigfile = ConfigParser.ConfigParser()
        gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
        logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
        logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
        logServerIp=gemuConfigfile.get("Test_Environment_GEMU","logserver_ip")
        bsctype=gemuConfigfile.get("Test_Environment_BSC","bsc_type")
        logFolderPath=logPath+logfolder
        print logFolderPath

	formattingfiles(logFolderPath,bsctype,logServerIp)
	file1Path=logFolderPath+'/'+'pre1.txt'
	file2Path=logFolderPath+'/'+'post2.txt'
	file3Path=logFolderPath+'/'+'pre2.txt'
	file4Path=logFolderPath+'/'+'post1.txt'
#	print file1Path
	file1=open(file1Path,'r+')
	file2=open(file2Path,'r+')
	file3=open(file3Path,'r+')
	file4=open(file4Path,'r+')

	file5Path=logFolderPath+'/'+'busybuffers_comparison_gena-disable.txt'
        file6Path=logFolderPath+'/'+'freebuffers_comparison_gena-disable.txt'
        file7Path=logFolderPath+'/'+'busybuffers_comparison_gena-enable.txt'
        file8Path=logFolderPath+'/'+'freebuffers_comparison_gena-enable.txt'
	file5=open(file5Path,'w')
        file6=open(file6Path,'w')
        file7=open(file7Path,'w')
        file8=open(file8Path,'w')


#	formattingfiles(logFolderPath,bsctype,logServerIp)
	busy_buffer_initial=[]
	free_buffer_initial=[]
	busy_buffer_final=[]
	free_buffer_final=[]
	buffer_index=[]
	utilization_initial=[]
	utilization_final=[]
	print(" \n\n comparison of pre and post files when GENA=N")
	print("calling function 1-reading busy buffers of both the files")
	# In pre1 file busy buffer and free buffer columns will be read and stored in list
	busy_buffer_initial,free_buffer_initial,buffer_index,utilization=readingcolumns(file1)
#	print buffer_index
#	print "busy_buffer_initial is ", busy_buffer_initial
#	print free_buffer_initial

	print("calling function 2-reading free buffers of both the files")

	busy_buffer_final,free_buffer_final,buffer_index,utilization=readingcolumns(file2)
	# this function compares the buffers and write those buffers as well as their difference in file
#	print busy_buffer_final
#	print free_buffer_final

	comparison_of_buffers(file5,busy_buffer_initial,busy_buffer_final,buffer_index)
	comparison_of_buffers(file6,free_buffer_initial,free_buffer_final,buffer_index)
		




	print("\n\n comparison of pre and post files when GENA=Y")

        print("calling function -reading busy buffers of both the files")

        busy_buffer_initial,free_buffer_initial,buffer_index,utilization=readingcolumns(file3)
        print("calling function 2-reading free buffers of both the files")

        busy_buffer_final,free_buffer_final,buffer_index,utilization=readingcolumns(file4)
        comparison_of_buffers(file7,busy_buffer_initial,busy_buffer_final,buffer_index)
        comparison_of_buffers(file8,free_buffer_initial,free_buffer_final,buffer_index)


	file5.close()
	file6.close()
	file7.close()
        file8.close()
	# comparison of fp internal pool utilization

	fpFileformatting(logFolderPath,logServerIp,'0','11')
	
	global file9,file10,file11,file12
	file9Path=logFolderPath+'/'+'pre1fp.txt'
        file10Path=logFolderPath+'/'+'post2fp.txt'
        file11Path=logFolderPath+'/'+'pre2fp.txt'
        file12Path=logFolderPath+'/'+'post1fp.txt'
 #       print file9Path
        file9=open(file9Path,'r+')
        file10=open(file10Path,'r+')
        file11=open(file11Path,'r+')
        file12=open(file12Path,'r+')


	file13Path=logFolderPath+'/'+'fpUtilization_pool0_gena-disable.txt'
        file14Path=logFolderPath+'/'+'fpUtilization_pool0_gena-enable.txt'
        file13=open(file13Path,'w')
        file14=open(file14Path,'w')
	file15Path=logFolderPath+'/'+'fpUtilization_pool1_gena-disable.txt'
        file16Path=logFolderPath+'/'+'fpUtilization_pool1_gena-enable.txt'
        file15=open(file15Path,'w')
        file16=open(file16Path,'w')
	file17Path=logFolderPath+'/'+'fpUtilization_pool2_gena-disable.txt'
        file18Path=logFolderPath+'/'+'fpUtilization_pool2_gena-enable.txt'
        file17=open(file17Path,'w')
        file18=open(file18Path,'w')
	file19Path=logFolderPath+'/'+'fpUtilization_pool3_gena-disable.txt'
        file20Path=logFolderPath+'/'+'fpUtilization_pool3_gena-enable.txt'
        file19=open(file19Path,'w')
        file20=open(file20Path,'w')
	file21Path=logFolderPath+'/'+'fpUtilization_pool4_gena-disable.txt'
        file22Path=logFolderPath+'/'+'fpUtilization_pool4_gena-enable.txt'
        file21=open(file21Path,'w')
        file22=open(file22Path,'w')
	file23Path=logFolderPath+'/'+'fpUtilization_pool25_gena-disable.txt'
        file24Path=logFolderPath+'/'+'fpUtilization_pool25_gena-enable.txt'
        file23=open(file23Path,'w')
        file24=open(file24Path,'w')






	# processing for pool id-0
#	fpFileformatting(logFolderPath,logServerIp,'0','11')	 
	# fp utilization readings when Gena is disabled
#	print file9
	print(" processing for pool id 0")
	busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file9)
	busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file10)
	comparison_of_buffers(file13,utilization_initial,utilization_final,buffer_index)
	file13.close()	
	# fp utilization readings when Gena is enabled


	busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file11)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file12)
        comparison_of_buffers(file14,utilization_initial,utilization_final,buffer_index)
	file14.close()
	file9.close(),file10.close(),file11.close(),file12.close()
#	verdictFunction(file5Path,file6Path,file7Path,file8Path,file13Path,file14Path)
	# processing for pool id-1
	
	print(" processing for pool id 1")
	file9=open(file9Path,'r+')
        file10=open(file10Path,'r+')
	file11=open(file11Path,'r+')
        file12=open(file12Path,'r+')
	fpFileformatting(logFolderPath,logServerIp,'1','3')

	busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file9)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file10)
        comparison_of_buffers(file15,utilization_initial,utilization_final,buffer_index)
        file15.close()
	busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file11)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file12)
        comparison_of_buffers(file16,utilization_initial,utilization_final,buffer_index)
        file16.close()
	file9.close(),file10.close(),file11.close(),file12.close()

	# processing for pool id-2
	print(" processing for pool id 2")
	file9=open(file9Path,'r+')
	file10=open(file10Path,'r+')
	file11=open(file11Path,'r+')
	file12=open(file12Path,'r+')
       	fpFileformatting(logFolderPath,logServerIp,'2','4')



        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file9)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file10)
        comparison_of_buffers(file17,utilization_initial,utilization_final,buffer_index)
        file17.close()


        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file11)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file12)
        comparison_of_buffers(file18,utilization_initial,utilization_final,buffer_index)
        file18.close()

	file9.close(),file10.close(),file11.close(),file12.close()
	# processing for pool id-3
	print(" processing for pool id 3")
	file9=open(file9Path,'r+')
        file10=open(file10Path,'r+')
        file11=open(file11Path,'r+')
        file12=open(file12Path,'r+')

        fpFileformatting(logFolderPath,logServerIp,'3','3')



        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file9)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file10)
        comparison_of_buffers(file19,utilization_initial,utilization_final,buffer_index)
        file19.close()


        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file11)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file12)
        comparison_of_buffers(file20,utilization_initial,utilization_final,buffer_index)
        file20.close()
	
	file9.close(),file10.close(),file11.close(),file12.close()


	# processing for pool id-4
	
	print(" processing for pool id 4")
	file9=open(file9Path,'r+')
        file10=open(file10Path,'r+')
        file11=open(file11Path,'r+')
        file12=open(file12Path,'r+')

        fpFileformatting(logFolderPath,logServerIp,'4','3')



        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file9)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file10)
        comparison_of_buffers(file21,utilization_initial,utilization_final,buffer_index)
        file21.close()


        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file11)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file12)
        comparison_of_buffers(file22,utilization_initial,utilization_final,buffer_index)
        file22.close()

	file9.close(),file10.close(),file11.close(),file12.close()



	 # processing for pool id-25

	print(" processing for pool id 25")
	file9=open(file9Path,'r+')
        file10=open(file10Path,'r+')
        file11=open(file11Path,'r+')
        file12=open(file12Path,'r+')
        fpFileformatting(logFolderPath,logServerIp,'25','3')



        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file9)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file10)
        comparison_of_buffers(file23,utilization_initial,utilization_final,buffer_index)
        file23.close()


        busy_buffer_initial,free_buffer_initial,buffer_index,utilization_initial=readingcolumns(file11)
        busy_buffer_final,free_buffer_final,buffer_index,utilization_final=readingcolumns(file12)
        comparison_of_buffers(file24,utilization_initial,utilization_final,buffer_index)
        file24.close()

	file9.close(),file10.close(),file11.close(),file12.close()

	# Removing all the unnsecessary files from log folder
	ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(logServerIp, port=22, username='root', password='password')
	cmd5='cd'+' '+logFolderPath+";"+'cat fp* > mergedfp.txt'
	stdin, stdout, stderr = ssh.exec_command(cmd5)
#	print cmd5							
	cmd6='cd'+' '+logFolderPath+";"+'rm -rf fp* pre1.txt pre2.txt post1.txt post2.txt post1fp.txt post2fp.txt pre1fp.txt pre2fp.txt  post1A.txt post1B.txt pre1C.txt pre2C.txt post1C.txt post2C.txt  post2A.txt post2B.txt pre1A.txt pre1B.txt pre2A.txt pre2B.txt'
 #       print cmd6
        stdin, stdout, stderr = ssh.exec_command(cmd6)
	mergedfpPath=logFolderPath+'/'+'mergedfp.txt'
#	m=open(mergedfpPath,'r+')


	verdictFunction(file5Path,file6Path,file7Path,file8Path,mergedfpPath)
