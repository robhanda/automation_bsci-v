########################################################################################################
# file name   : kpiAnalysis.py                                                                         #
# date        : 23-11-2017                                                                             #
# author      : Arun Vignesh N.S. arun.ns@nokia.com                                                    #
# version     : 0.1                                                                                    #
# description : Read TP_SUMMARY.log and PA_SUMMARY.log file and check the Packet Abis and Gb throughput#
#               are within the threshold.                                                              #
########################################################################################################
import sys
import time
import loggingLibrary
import ConfigParser
class kpiAnalysis:
    def __init__(self,ulGbIp,dlGbIp,ulPAbis,dlPAbis,measureFileName,resultKey):
        self.ulGbIp=ulGbIp
        self.dlGbIp=dlGbIp
        self.ulPAbis=ulPAbis
        self.dlPAbis=dlPAbis
        self.measureFileName=measureFileName
        self.resultKey=resultKey

    def collectStats(self,summaryFilePath):
        '''This function reads the Throughput summary files and store the values in lists'''
        try:
            fileOpenTpSummary=open(summaryFilePath+"/TP_SUMMARY.log",'r')
            readLineTpSummary=fileOpenTpSummary.readlines()
            if len(readLineTpSummary)>0:
                for line in readLineTpSummary:
                    gbThroughputDataLine = (line.strip()).split(' ')
                    gbThroughputDataList=' '.join(gbThroughputDataLine).split()
                    measureFileName.append(gbThroughputDataList[3])
                    if gbThroughputDataList[4].isalpha():
                        pass
                    else:
                        ulGbIp.append(float(gbThroughputDataList[4]))
                        dlGbIp.append(float(gbThroughputDataList[5]))
                fileOpenTpSummary.close()
                logObject.writeInfoLogs("TP_SUMMARY.log file read successful")
            else:
                logObject.writeErrorLogs("TP_SUMMARY.log file is empty")
        except IOError:
            logObject.writeErrorLogs("TP_SUMMARY.log File not found")
        try:
            fileOpenPaSummary=open(summaryFilePath+"/PA_SUMMARY.log",'r')
            readLinePaSummary=fileOpenPaSummary.readlines()
            if len(readLinePaSummary)>0:
                for line in readLinePaSummary:
                    paThroughputDataLine = (line.strip()).split(' ')
                    paThroughputDataList = ' '.join(paThroughputDataLine).split()
                    if paThroughputDataList[6].isalpha():
                        pass
                    else:
                        ulPAbis.append(float(paThroughputDataList[6]))
                        dlPAbis.append(float(paThroughputDataList[7]))
                fileOpenPaSummary.close()
                logObject.writeInfoLogs("PA_SUMMARY.log file read successful")
            else:
                logObject.writeErrorLogs("PA_SUMMARY.log file is empty")
        except IOError:
            logObject.writeErrorLogs("PA_SUMMARY.log File not found")
    def gbThroughputAnalysis(self,resultKey):
        '''This Function does the GB throughput analysis.80% of the max GB throughput is taken as the threshold value'''
        try:
            max_ulGbIp=max(ulGbIp)
            avg_ulGbIp=sum(ulGbIp)/len(ulGbIp)
            max_dlGbIp=max(dlGbIp)
            avg_dlGbIp=sum(dlGbIp)/len(dlGbIp)
            thresholdulGbIp=.80* max_ulGbIp
            thresholddlGbIp=.80* max_dlGbIp
            #print avg_ulGbIp
            logObject.writeInfoLogs("The avg_ulGbIP is "+str(avg_ulGbIp)+" and the expected Threshold is "+str(thresholdulGbIp))
            logObject.writeInfoLogs("The avg_dlGbIP is " + str(avg_dlGbIp) + " and the expected Threshold is " + str(thresholddlGbIp))
            if ((avg_ulGbIp >= thresholdulGbIp) & (avg_dlGbIp >= thresholddlGbIp)):
                self.resultKey="True"
            else:
                self.resultKey="False"
        except:
            logObject.writeErrorLogs("List ulGbIp/dlGbIp is empty")

    def paThroughputAnalysis(self,resultKey):
        '''This Function does the PA throughput analysis.80% of the max PA throughput is taken as the threshold value'''
        try:
            max_ulPAbis = max(ulPAbis)
            avg_ulPAbis = sum(ulPAbis) / len(ulPAbis)
            max_dlPAbis = max(dlPAbis)
            avg_dlPAbis = sum(dlPAbis) / len(dlPAbis)
            thresholdulPAbis=.80 * max_ulPAbis
            thresholddlPAbis=.80 * max_dlPAbis
            logObject.writeInfoLogs("The avg_ulPAbis is " + str(avg_ulPAbis) + " and the expected Threshold is " + str(thresholdulPAbis))
            logObject.writeInfoLogs("The avg_dlPAbis is " + str(avg_dlPAbis) + " and the expected Threshold is " + str(thresholddlPAbis))
            if self.resultKey == "True" :
                if ((avg_ulPAbis >= thresholdulPAbis) & (avg_dlPAbis >= thresholddlPAbis)):
                    self.resultKey = "True"
                else:
                    self.resultKey="False"
        except:
            logObject.writeErrorLogs("List ulPAbis/dlPAbis is empty")
    def verdictFunction(self,resultKey):
        '''This Function Analyse the resultKey and provides the verdict'''
        if self.resultKey=="True":
            print ("KPI Analysis Passed ")
        else:
            print ("KPI Analysis Failed")
    def findSummaryFilesPath(self):
        ''' This Function finds the path of the Summary Files transfered from the GEMU Stat Manager '''
        gemuConfigfile=ConfigParser.ConfigParser()
        gemuConfigfile.read('/home/Automation/scripts/testConfiguration.ini')
        logPathSummaryFile=gemuConfigfile.get('Test_Environment_GEMU','logpath')
        logFolderSummaryFile=gemuConfigfile.get('Test_Environment_GEMU','logfolder')
        absoluteLogPath=logPathSummaryFile+logFolderSummaryFile
        return absoluteLogPath
if __name__ == "__main__":
    ulGbIp = []
    dlGbIp = []
    measureFileName = []
    ulPAbis=[]
    dlPAbis=[]
    resultKey=""
    logObject = loggingLibrary.logPrint()
    gbThroughput=kpiAnalysis(ulGbIp,dlGbIp,ulPAbis,dlPAbis,measureFileName,resultKey)
    summaryFilePath=gbThroughput.findSummaryFilesPath()
    #print summaryFilePath
    gbThroughput.collectStats(summaryFilePath)
    gbThroughput.gbThroughputAnalysis(resultKey)
    gbThroughput.paThroughputAnalysis(resultKey)
    gbThroughput.verdictFunction(resultKey)
    #print gbThroughput.resultKey


