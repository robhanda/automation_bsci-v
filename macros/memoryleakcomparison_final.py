import sys,os


def formattingfiles():
	if(bsctype=="mcbsc"):
		# this function reads pq_mem_pre1 files generted by script and removes all the garbage from it to make it readable by program
		#pre1- gena=N,pre2-gena=y,post1-gena=y,post2-gena=n ,pre1 and post-2 and pre2 and post1 has to be compared
							
		print("this function foemats o/p file in  format that can be used by program")
		os.system('sed "s/\<INTERNAL POOLS\>//g" /home/Automation/memoryleak/pq_mem_pre1.txt > /home/Automation/memoryleak/pre1A.txt')
		os.system('sed "s/\<INTERNAL POOLS\>//g"/home/Automation/memoryleak/ pq_mem_pre2.txt >/home/Automation/memoryleak/ pre2A.txt')
		os.system('sed "s/\<INTERNAL POOLS\>//g"/home/Automation/memoryleak/ pq_mem_post1.txt >/home/Automation/memoryleak/ post1A.txt')
		os.system('sed "s/\<INTERNAL POOLS\>//g"/home/Automation/memoryleak/ pq_mem_post1.txt >/home/Automation/memoryleak/ post2A.txt')


		os.system('sed "/Total/d" </home/Automation/memoryleak/pre1A.txt >/home/Automation/memoryleak/ pre1B.txt')
		os.system('sed "/Total/d" </home/Automation/memoryleak/pre2A.txt >/home/Automation/memoryleak/ pre2B.txt')
		os.system('sed "/Total/d" </home/Automation/memoryleak/post1A.txt >/home/Automation/memoryleak/ post1B.txt')
		os.system('sed "/Total/d" </home/Automation/memoryleak/post2A.txt >/home/Automation/memoryleak/ post2B.txt')

		os.system('grep "buffers" -A 23 /home/Automation/memoryleak/pre1B.txt>/home/Automation/memoryleak/pre1.txt')
		os.system('grep "buffers" -A 23 /home/Automation/memoryleak/pre2B.txt>/home/Automation/memoryleak/pre2.txt')
		os.system('grep "buffers" -A 23 /home/Automation/memoryleak/post1B.txt>/home/Automation/memoryleak/post1.txt')
		os.system('grep "buffers" -A 23 /home/Automation/memoryleak/post2B.txt>/home/Automation/memoryleak/post2.txt')

	else:
		os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_pre1.txt>/home/Automation/memoryleak/pre1.txt')
	        os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_post2.txt>/home/Automation/memoryleak/post2.txt')
        	os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_pre2.txt>/home/Automation/memoryleak/pre2.txt')
        	os.system('grep "Current" -A 28 /home/Automation/memoryleak/pq_mem_post1.txt>/home/Automation/memoryleak/post1.txt')






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
	template=["buffer_size","    ","buffer_initial","    ","buffer_final","    ","difference","        ","result"]
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
			file.write(' ' + k+ '             ')
                	file.write('   '+ i+ '                      ')
                	file.write(j+'          ')
			diff=str(diff)
			file.write(diff + '     ')
			file.write(res + '\n')
                	counter=counter+1
	print("in both the files total %d lines were not matching"%counter)
	

if __name__ == "__main__":
	sys.path.insert(0,'/home/Automation/parameters/')

	import input_file
	bsctype=input_file.bsc_type
	print bsctype
	formattingfiles()
	file1=open('/home/Automation/memoryleak/pre1.txt','r+')
	file2=open('/home/Automation/memoryleak/post2.txt','r+')
	file3=open('/home/Automation/memoryleak/pre2.txt','r+')
        file4=open('/home/Automation/memoryleak/post1.txt','r+')
	# compared values will be saved in 4 different files
	file5=open('/home/Automation/memoryleak/busybuffers_comparison_gena-NO.txt','w')
	file6=open('/home/Automation/memoryleak/freebuffers_comparison_gena-NO.txt','w')
	file7=open('/home/Automation/memoryleak/busybuffers_comparison_gena-yes.txt','w')
        file8=open('/home/Automation/memoryleak/freebuffers_comparison_gena-yes.txt','w')

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







