# 查找有没有这个账号如果有不创建作为提示
# 用户名和密码不能有空格 去掉空格

from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815.CreateAccountRequest import CreateAccountRequest

import csv

accessKeyId = ""
accessSecret = ""
regionId = ""
DBInstanceId = ""
accountType = "Normal"
filePath = "./data.csv"


def get_data():
    csvData = []

    with open(filePath, "r") as csvFile:
        try:
            data = csv.reader(csvFile)
            for row in data:
                csvData.append(row)
        except Exception as error:
            print(error)
        return csvData


def send_request(csvData):
    for row in csvData:
        accountName = row[0]
        accountPassword = row[1]
        accountDescription = row[2]
        client = AcsClient(accessKeyId, accessSecret, regionId)
        request = CreateAccountRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(DBInstanceId)
        request.set_AccountName(accountName)
        request.set_AccountPassword(accountPassword)
        request.set_AccountDescription(accountDescription)
        request.set_AccountType(accountType)
        try:
            client.do_action_with_exception(request)
        except Exception as error:
            if 'InvalidAccountName.Duplicate Invalid "AccountName" specified, duplicated.' in str(error):
                print(accountName + ": 用户名重复创建失败")
            elif 'InvalidAccountName.Malformed The specified parameter "AccountName" is not valid.' in str(error):
                print(accountName + ": 用户名无效不能使用")
            elif 'InvalidAccountPassword.Malformed The specified parameter "AccountPassword" is not valid.' in str(error):
                print(accountName + ": 用户密码无效不能使用")
            else:
                print("我也不知道是什么错误:" + error)


if __name__ == '__main__':
    csvData = get_data()
    send_request(csvData)
    print("所有账户创建成功")