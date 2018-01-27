import ConfigParser
import re
import sys
class initAutomation(object):

    def __init__(self,trafficProfile):
        #pass
        self.trafficProfile=trafficProfile
        print trafficProfile
    def updateConfigFile(self,trafficProfile,gemuConfigfile):
        gemuConfigfile.set('Test_Case_Details','traffic_profile',trafficProfile[1])
	gemuConfigfile.set('Test_Environment_GEMU','logFolder',trafficProfile[2])
        with open('/home/Automation/scripts/testConfiguration.ini', 'w') as configFile:
            gemuConfigfile.write(configFile)
if __name__ == "__main__":
    gemuConfigfile = ConfigParser.ConfigParser()
    gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
    trafficProfile=sys.argv
    testCase=initAutomation(trafficProfile)
    testCase.updateConfigFile(trafficProfile,gemuConfigfile)	
