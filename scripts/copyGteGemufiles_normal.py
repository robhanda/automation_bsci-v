import os
import ConfigParser
def copyGteFiles(sourcePath,targetPath,sourcePathStateMachine,ipAddressList,numberOfMachines,numberOfBcfPerMachine):
    for index,ipAddress in enumerate(ipAddressList):
        if index == 0 or index % numberOfBcfPerMachine == 0:
            os.system("scp "+sourcePath+" root@"+ipAddress+":"+targetPath)
            os.system("scp " + sourcePathStateMachine + " root@" + ipAddress + ":" + targetPath)
def copyElgMacro(sourceElgMacroPath,targetElgMacroPathbcf,ipAddressList,numberOfMachines,numberOfBcfPerMachine) :
    for index,ipAddress in enumerate(ipAddressList):
        if index==0 or index%numberOfBcfPerMachine ==0 :
            for bcf in xrange(numberOfBcfPerMachine):
                if bcf==0 :
                   print ipAddress,sourceElgMacroPath,targetElgMacroPathbcf
                   os.system("scp " + sourceElgMacroPath + " root@" + ipAddress + ":" + targetElgMacroPathbcf)
                else:
                    
                    tempPath=targetElgMacroPathbcf.replace("bcf","bcf_"+str(bcf))
                    print ipAddress,sourceElgMacroPath,tempPath
                    os.system("scp " + sourceElgMacroPath + " root@" + ipAddress + ":" + tempPath)
if __name__ == "__main__":
    gemuConfigfile=ConfigParser.ConfigParser()
    gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
    gemuStartIp=gemuConfigfile.get('Test_Environment_GEMU','gemu_machine_start_ip')
    trafficProfileType=gemuConfigfile.get("Test_Case_Details","traffic_profile")
    ipAddress=gemuConfigfile.get('Test_Environment_GEMU','gemu_machine_start_ip')
    ipOctectList = ipAddress.split(".")
    lastIpOctet=int((ipAddress.split("."))[3])
    ipAddressList=[]
    numberOfMachines=int(gemuConfigfile.get('Test_Environment_GEMU','number_of_gemu_machines'))
    numberOfBcfPerMachine=int(gemuConfigfile.get('Test_Environment_GEMU','number_of_bcf_per_machine'))
    totalNumberOfBcf=numberOfMachines*numberOfBcfPerMachine
    print totalNumberOfBcf
    for bcf in xrange(totalNumberOfBcf):
        ipAddressGenerate=ipOctectList[0]+"."+ipOctectList[1]+"."+ipOctectList[2]+"."+str(lastIpOctet+bcf)
        ipAddressList.append(ipAddressGenerate)
    if trafficProfileType=="GPRS":
        print trafficProfileType
        sourcePath=gemuConfigfile.get('Test_Environment_GEMU','filepathgprs')
        sourcePathStateMachine=gemuConfigfile.get('Test_Environment_GEMU','filepathgprstest')
        targetPath=gemuConfigfile.get('Test_Environment_GEMU','gtepath')
        sourceElgMacroPath=gemuConfigfile.get('Test_Environment_GEMU','filepathelgmsmacro')
        targetElgMacroPathbcf=gemuConfigfile.get('Test_Environment_GEMU','gemumacrospathbcf1')
        copyGteFiles(sourcePath,targetPath,sourcePathStateMachine,ipAddressList,numberOfMachines,numberOfBcfPerMachine)
        copyElgMacro(sourceElgMacroPath,targetElgMacroPathbcf,ipAddressList,numberOfMachines,numberOfBcfPerMachine)
    elif trafficProfileType=="EGPRS":
        print "i am in EGPS"
        sourcePath=gemuConfigfile.get('Test_Environment_GEMU','filepathegprs')
        sourcePathStateMachine=gemuConfigfile.get('Test_Environment_GEMU','filepathegprstest')
        targetPath=gemuConfigfile.get('Test_Environment_GEMU','gtepath')
        sourceElgMacroPath=gemuConfigfile.get('Test_Environment_GEMU','filepathelgmsmacro_egprs')
        targetElgMacroPathbcf=gemuConfigfile.get('Test_Environment_GEMU','gemumacrospathbcf1')
        copyGteFiles(sourcePath,targetPath,sourcePathStateMachine,ipAddressList,numberOfMachines,numberOfBcfPerMachine)
        copyElgMacro(sourceElgMacroPath,targetElgMacroPathbcf,ipAddressList,numberOfMachines,numberOfBcfPerMachine)


