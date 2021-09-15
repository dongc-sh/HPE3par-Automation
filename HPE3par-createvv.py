import urllib3
from hpe3parclient import client
import pandas as pd


def Get3parInfo(workbook, sheetname):
    dev_read = pd.read_excel(io=workbook, sheet_name=sheetname, header=None, names=None, usecols='K')
    dev_info = dev_read.values.tolist()
    global hpe3parip,username,password,hostname
    hpe3parip = dev_info[1][0]
    username = dev_info[2][0]
    password = dev_info[3][0]
    hostname = dev_info[0][0]

def GetVolumeInfo(workbook, sheetname):
    dev_read = pd.read_excel(io=workbook, sheet_name=sheetname, header=0, names=None, usecols='B:F')
    dev_info = dev_read.values.tolist()
    global VolumeName,VolumeSize,UsrCPG,SnapCPG,TPVV
    VolumeName,VolumeSize,UsrCPG,SnapCPG,TPVV = [[] for x in range(5)]
    for member in dev_info:
        VolumeName.append(member[0])
        VolumeSize.append(member[1]*1024)
        UsrCPG.append(member[2])
        if member[3] == "None" or member[3] == "none" or member[3] == "NONE":
            SnapCPG.append(None)                                                      #如果volume不需要配置snapCPG，则返回None
        else:
            SnapCPG.append(member[3])
        TPVV.append(member[4])


def CreateVolume(conn, *volumeinfo):
    if VolumeName[i] in vol_tuple:
        print("volume exists! %s not created" % VolumeName[i])                         #如果volume已存在，则不进行创建操作
    else:
        conn.createVolume(name=VolumeName[i], cpgName=UsrCPG[i], sizeMiB=VolumeSize[i],optional={'snapCPG':SnapCPG[i], 'tpvv':TPVV[i]})
        vol_info = conn.getVolume(VolumeName[i])
        print("VV:%s  Size:%dGB  usrCPG:%s  CreateTime:%s" %(vol_info['name'],vol_info['sizeMiB']/1024,vol_info['userCPG'],vol_info['creationTime8601']))

def Connect3par(hpe3parip, username, password):
    cl = client.HPE3ParClient('https://%s:8080/api/v1' % hpe3parip)
    cl.setSSHOptions(ip=hpe3parip, login=username, password=password)
    cl.login(username, password)
    print("Success login %s, Prepare the creation..." %hpe3parip)
    return cl

if __name__ == '__main__':
    WorkBook = 'D:\\Python\Prohpe3par\HPE3parAutomation.xlsx'
    SheetName = 'createvv'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    Get3parInfo(WorkBook,SheetName)                                    #读取excel表中3par存储的登录账户
    conn = Connect3par(hpe3parip, username, password)                  #登录3par存储
    GetVolumeInfo(WorkBook, SheetName)                                 #读取excel表需要创建的volume的信息

    output = conn.getVolumes()                                          #获取当前存储volume列表，用户创建时判断volume是否已存在
    vol_list = []
    for i in output['members']:
        vol_list.append(i['name'])
    vol_tuple = tuple(vol_list)

    for i in range(len(VolumeName)):
        CreateVolume(conn,VolumeName[i],UsrCPG[i],VolumeSize[i],SnapCPG[i],TPVV[i],vol_tuple)               #按照excel表，创建volume

    conn.logout()


