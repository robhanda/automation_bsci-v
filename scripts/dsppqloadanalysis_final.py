# eneter the stat manager ip and numberof dsp&pq in file input_file.py

import sys,os,ConfigParser


def filecopying(bsctype,statManagerip,logFolderPath):	

	os.system("scp" + " " + "root"+"@"+statManagerip+ ":/home/bscmeas/*.log"+" " + logFolderPath)
	

	'''
	if(bsctype=="mcbsc"):


		scpcommand="scp" + " " + "root"+"@"+statManagerip+ ":/home/bscmeas/PCUM_Status_na"+pcumid+".log"+" " + logFolderPath
		print scpcommand
		os.system("scp" + " " + "root"+"@"+statManagerip+ ":/home/bscmeas/PCUM_Status_na"+pcumid+".log"+" " + logFolderPath)

	elif(bsctype=="Flexi"):

		scpcommand="scp" + " " + "root"+"@"+statManagerip+ ":/home/bscmeas/PCU_Status_"+pcuid+".log"+" " + logFolderPath
                print scpcommand
                os.system("scp" + " " + "root"+"@"+statManagerip+ ":/home/bscmeas/PCU_Status_"+pcuid+".log"+" " + logFolderPath)


	'''

def dataprocessing(bsctype,pcuOrpcumid,logFolderPath,dsppqCount):
	no_of_pqdsp=dsppqCount+1
	if(bsctype=="mcbsc"):
		fileName1=logFolderPath+'/'+"PCUM_Status_na"+pcuOrpcumid+".log"
		print fileName1
		cmd="grep -v \"Time\" "+fileName1+" > "+ logFolderPath+ '/' + 'dsppq.log'
		print cmd
		os.system(cmd)
		fileName=logFolderPath+ '/' + 'dsppq.log'
		print fileName
		file=open(fileName,'r+')

	else:
		print("inside else for flexi bsc")
		fileName1=logFolderPath+'/'+"PCU_Status_"+pcuOrpcumid+".log"
		print fileName1
		cmd="grep -v \"Time\" "+fileName1 +" > "+ logFolderPath+ '/' + 'dsppq.log'
                print cmd
                os.system(cmd)
		fileName=logFolderPath+ '/' + 'dsppq.log'
                print fileName


		file=open(fileName,'r+')
	# reading lines

	lines=file.readlines()
	j=0;

	colpq=[]
	threshold = []
	pqordsp=[]
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
					if(k==10):
						pqordsp[j]= "pq"
					else:
						pqordsp[j]= "dsp"+str(k-2)


				else:
					if(k==1):
						pqordsp[j]= "pq"
					else:
				
						pqordsp[j]= "dsp"+str(k-2)
			j = j + 1

# for every next element of column, j increments, so wherever thresold 	is crossed, in that particular place of threshold column "threshold crossed" is appended
	print "----"



#  range is calculated wrt column length, so for loop is run wrt column length. colpq[0]- time colpq[1]= seconds , when i iterates each element of column is printed
	global resultFillename
	resultFillename=logFolderPath+'/dsppqloadanalysis_result.txt'
	print resultFillename
	resultFile=open(resultFillename,'w+')
	
	for i in range(0, len(colpq[0])):
		print>>resultFile, colpq[0][i], "\t", colpq[1][i], "\t",
		print>>resultFile, pqordsp[i] , "\t","\t", threshold[i]

	resultFile.close()

def verdictFunction():

        global found
        found=False
	file=open(resultFillename,'r+')
        for line in file:
                print line
                if "Threshold Crossed" in line:
                        found=True
                        file.close()
                        break


	if(found==True):
                print("pqordsp buffer threshold exceeded")
        else:
                print("buffer threshold not exceeded")
        print found






if __name__ == "__main__":
	gemuConfigfile = ConfigParser.ConfigParser()
	gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
	statManagerip=gemuConfigfile.get("Test_Environment_BSC","statmanager_ip")
        bsctype=gemuConfigfile.get("Test_Environment_BSC","bsc_type")
        pcuid=gemuConfigfile.get("Test_Environment_BSC","pcu_id")
        pcumid=gemuConfigfile.get("Test_Environment_BSC","pcum_id")
	dsppqCount=int(gemuConfigfile.get("Test_Environment_BSC","number_of_pqdsp"))
	logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
        logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")
        logFolderPath=logPath+logfolder
	print("copying file from stat manager to local machine where script is kept")
	filecopying(bsctype,statManagerip,logFolderPath)
	print(" checking that any of the dsp or pq value has crossed the threshold or not")
	if(bsctype=="mcbsc"):
		dataprocessing(bsctype,pcumid,logFolderPath,dsppqCount)
	elif(bsctype=="Flexi"):
		dataprocessing(bsctype,pcuid,logFolderPath,dsppqCount)


	verdictFunction()
