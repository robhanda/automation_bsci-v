import ConfigParser

def searchElementinFile(filepath):
	file=open(filepath,'r+')
        for line in file:
                print line
                if "memory leak" in line:
                        found=True
                        file.close()
                        break





def verdictFunction(file5Path,file6Path,file7Path,file8Path):
	
	global found
	found=False

	searchElementinFile(file5Path)

	if(found==False):
		print("second file")	
		searchElementinFile(file6Path)
	if(found==False):
		print("3rd file") 
                searchElementinFile(file7Path)
	if(found==False):
		print("4th file")
                searchElementinFile(file8Path)

	if(found==True):
		print("memory leak found")
	else:
		print("no memory leak found")
	print found	








if __name__ == "__main__":
	print("inside main")
	gemuConfigfile = ConfigParser.ConfigParser()
        gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
        logPath=gemuConfigfile.get("Test_Environment_GEMU","logPath")
        logfolder=gemuConfigfile.get("Test_Environment_GEMU","logfolder")

	logFolderPath=logPath+logfolder
	file5Path=logFolderPath+'/'+'busybuffers_comparison_gena-NO.txt'
        file6Path=logFolderPath+'/'+'freebuffers_comparison_gena-NO.txt'
        file7Path=logFolderPath+'/'+'busybuffers_comparison_gena-yes.txt'
        file8Path=logFolderPath+'/'+'freebuffers_comparison_gena-yes.txt'
	
	verdictFunction(file5Path,file6Path,file7Path,file8Path)













