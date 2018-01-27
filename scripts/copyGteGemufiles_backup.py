import os
import ConfigParser
def copyGteFiles(sourcePath,targetPath,ipAddressList,numberOfMachines):
    for index,ipAddress in enumerate(ipAddressList):
        if numberOfBcfPerMachine == 2:
            if index == 0 or index % 2 == 0:
                os.system("scp "+sourcePath+" root@"+ipAddress+":"+targetPath)
                print ipAddress
def copyElgMacro(sourceElgMacroPath,targetElgMacroPathbcf1,targetElgMacroPathbcf2,ipAddressList,numberOfMachines) :
    for index,ipAddress in enumerate(ipAddressList):
        if numberOfBcfPerMachine == 2 :
            if index==0 or index%2 ==0 :
                os.system("scp " + sourceElgMacroPath + " root@" + ipAddress + ":" + targetElgMacroPathbcf1)
                os.system("scp " + sourceElgMacroPath + " root@" + ipAddress + ":" + targetElgMacroPathbcf2)
if __name__ == "__main__":
    gemuConfigfile=ConfigParser.ConfigParser()
    gemuConfigfile.read('testConfiguration.ini')
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
        targetPath=gemuConfigfile.get('Test_Environment_GEMU','gtepath')
        sourceElgMacroPath=gemuConfigfile.get('Test_Environment_GEMU','filepathelgmsmacro')
        targetElgMacroPathbcf1=gemuConfigfile.get('Test_Environment_GEMU','gemumacrospathbcf1')
        targetElgMacroPathbcf2=gemuConfigfile.get('Test_Environment_GEMU', 'gemumacrospathbcf2')
        copyGteFiles(sourcePath,targetPath,ipAddressList,numberOfMachines)
        copyElgMacro(sourceElgMacroPath,targetElgMacroPathbcf1,targetElgMacroPathbcf2,ipAddressList,numberOfMachines)
    elif trafficProfileType=="EGPRS":
        print "i am in EGPS"

