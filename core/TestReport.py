import os
import json
import shutil
import time

result = {
    "testPass": 1,
    "testResult": [
        {
            "serviceName": "com.test.testcase.TestDemo1",
            "serviceUrl": "http://test",
            "methodName": "post",
            "description": "测试DEMO",
            "spendTime": "11ms",
            "status": "成功",
            "log": [
                "this is demo!"
            ]
        },
        {
            "serviceName": "com.test.testcase.TestDemo1",
            "serviceUrl": "http://test",
            "methodName": "post",
            "description": "测试DEMO",
            "spendTime": "11ms",
            "status": "失败",
            "log": [
                "this is demo!"
            ]
        }
    ],
    "testName": "20171109132744898",
    "testAll": 1,
    "testFail": 0,
    "beginTime": "2017-11-09 13:27:44.917",
    "totalTime": "11ms",
    "testSkip": 0
}


class Report:

    testResultList = []
    testResultDict = {}

    def buildReportResult(self, serviceName, serviceUrl, methodName, description, spendTime, status, logMessage):
        log = []
        log.append(logMessage)
        self.testResultDict["log"] = log
        self.testResultDict["serviceName"] = serviceName
        self.testResultDict["serviceUrl"] = serviceUrl
        self.testResultDict["methodName"] = methodName
        self.testResultDict["description"] = description
        self.testResultDict["spendTime"] = spendTime
        self.testResultDict["status"] = status
        self.testResultList.append(self.testResultDict)
        return self.testResultList


    def buildTestReport(self, testResult, testName, testPass, testFail, testSkip, totalTime):

        reportResut = {}

        reportResut["testPass"] = testPass
        reportResut["testResult"] = testResult
        reportResut["testName"] = testName
        reportResut["testAll"] = len(testResult)
        reportResut["testFail"] = testFail
        reportResut["beginTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        reportResut["totalTime"] = totalTime
        reportResut["testSkip"] = testSkip

        # 写入测试报告
        self.writeReport(reportResut, testName)

    def writeReport(self, reportResut, testName):
        reportHtmlFileName = testName + "_report.html"

        reportDirPath = os.path.dirname(os.path.dirname(os.path.realpath("report"))) + "\\report\\"

        template = open("template", "r", encoding='UTF-8')
        reportHtml = open(reportHtmlFileName, "w", encoding='UTF-8')
        for s in template:
            reportHtml.write(s.replace("${resultData}", json.dumps(reportResut)))

        reportHtml.close()
        template.close()

        # 剪切文件到指定文件夹中 report
        if os.path.exists(reportDirPath):
            self.moveRepor(reportHtmlFileName,reportDirPath)

        else:
            os.makedirs(reportDirPath)
            self.moveRepor(reportHtmlFileName,reportDirPath)

    def moveRepor(self, fileName, dirPath):
        oldFilePath = os.path.realpath(fileName)
        newFilePath = dirPath + fileName
        shutil.move(oldFilePath, newFilePath)


report1 = Report()
report_result = report1.buildReportResult("userService", "http://user", "post", "用户信息接口",
                                                     "10ms", "成功", "测试数据")
report1.buildTestReport(report_result,"测试1", result["testPass"], result["testFail"], result["testSkip"],
                        result["totalTime"])
