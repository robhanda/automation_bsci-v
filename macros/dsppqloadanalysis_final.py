# eneter the stat manager ip and numberof dsp&pq in file input_file.py

import sys,os
sys.path.insert(0,'/home/Automation/parameters/')
import input_file
#import /home/Automation/parameters/input_file


def filecopying():	

	ip=input_file.stat_ip
	path=input_file.destination_path
	bsctype=input_file.bsc_type
	pcuid=input_file.pcu_id
	pcumid=input_file.pcum_id


	if(bsctype=="mcbsc"):


		scpcommand="scp" + " " + "root"+"@"+ip+ ":/home/bscmeas/PCUM_Status_na"+pcumid+".log"+" " + path
		print scpcommand
		os.system("scp" + " " + "root"+"@"+ip+ ":/home/bscmeas/PCUM_Status_na"+pcumid+".log"+" " + path)

	else:
		scpcommand="scp" + " " + "root"+"@"+ip+ ":/home/bscmeas/PCU_Status_"+pcuid+".log"+" " + path
                print scpcommand
                os.system("scp" + " " + "root"+"@"+ip+ ":/home/bscmeas/PCU_Status_"+pcuid+".log"+" " + path)




def dataprocessing():
	bsctype=input_file.bsc_type
	dsppq=input_file.number_of_pqdsp
	no_of_pqdsp=int(dsppq)+1
	if(bsctype=="mcbsc"):
		file=open('/root/PCUM_Status_na00.log','r+')

	else:
		file=open('/root/PCU_Status_0004.log','r+')
# reading lines

	lines=file.readlines()
	j=0;

	colpq=[]
	threshold = []
	pqordsp=[]
	bsctype=input_file.bsc_type
	print bsctype
# creating list of lists which has 100 blank lists
	for i in range(0,100):
		colpq.append([])


	for line in lines:
		temp=[]
		splitted_line=line.split()
		i = 0
	# this will remove blank lines and blank spaces
		if len(splitted_line)>0:
			for element in splitted_line:
				if len(element)>0:
					colpq[i].append(element)
					i = i + 1  # each element of row/line will be appended to different list, once the elements in splitted line will be over value of i will be refreshed
	
		threshold.append("Not Crossed")
		pqordsp.append(" ")
# each element of row/line will be appended to different list, once the elements in splitted line will be over value of i will be refreshed, so elements of next splitted line will be appended below same lists
# in this way we will get different columns in different lists
# threshold is one more blank list in which " not crossed " is appended in each line


		
	k=0
# reading columns which have pq and dsp data
	for i in colpq[3:no_of_pqdsp]:
		k=k+1				# k increments with outer loop and j increments with inner loop. Inner loop - each element in that loop
		j = 0
		for x in i: # reading data/elements inside each columns i represents columns and x represents elements inside those columns
			if float(x) >= 85.0:
				print x + str(j)
				threshold[j] = "Threshold Crossed"
				if(bsctype=="mcbsc"):
					if(1<=k<10):
						pqordsp[j]= "pq"+str(k)
					else:
						pqordsp[j]= "dsp"+str(k)


				else:
					if(j==1):
						pqordsp[j]= "pq"+str(k)
					else:
				
						pqordsp[j]= "dsp"+str(k)
			j = j + 1

# for every next element of column, j increments, so wherever thresold 	is crossed, in that particular place of threshold column "threshold crossed" is appended
	print "----"



#  range is calculated wrt column length, so for loop is run wrt column length. colpq[0]- time colpq[1]= seconds , when i iterates each element of column is printed
	for i in range(0, len(colpq[0])):
		print colpq[0][i], "\t", colpq[1][i], "\t",
		print pqordsp[i] , "\t","\t", threshold[i]


if __name__ == "__main__":
	print("copying file from stat manager to local machine where script is kept")
	filecopying()
	print(" checking that any of the dsp or pq value has crossed the threshold or not")
	dataprocessing()

