########################################################################################################
# file name   : loggingLibrary.py                                                                      #
# date        : 23-11-2017                                                                             #
# author      : Arun Vignesh N.S. arun.ns@nokia.com                                                    #
# version     : 0.1                                                                                    #
# description : Library function for logging                                                           #
#                                                                                                      #
########################################################################################################
import logging
import time
import ConfigParser
gemuConfigfile=ConfigParser.ConfigParser()
gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
logPath=gemuConfigfile.get('Test_Environment_GEMU','logpath')
logFolder=gemuConfigfile.get('Test_Environment_GEMU','logfolder')
logFileName = logPath+logFolder+"/"+'logfileKPI_'
logDateTime = time.strftime("%m%d%Y_%I%M%S")
logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter=logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler=logging.FileHandler(logFileName + logDateTime + '.log')
#file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
class logPrint:
    def writeInfoLogs(self,logDescription):
        file_handler.setLevel(logging.INFO)
        logger.info(logDescription)
    def writeDebugLogs(self,logDescription):
        file_handler.setLevel(logging.DEBUG)
        logger.debug(logDescription)
    def writeErrorLogs(self,logDescription):
        file_handler.setLevel(logging.ERROR)
        logger.error(logDescription)
    def writeWarningLogs(self, logDescription):
        file_handler.setLevel(logging.WARNING)
        logger.warning(logDescription)
if __name__=="__main__":
    logDateTime=''
    logFileName=''
    #logObject = logPrint()



