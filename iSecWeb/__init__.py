from datetime import datetime
import time
import os
from flask import json
from flask_restful import abort, request, Resource, Api
from random import randint

ipConnADDR = []
iSecWebConfig = {
    'restrictionFN': 'restNF.json',
    'filename': 'iplogs.json',
    'connTime': 1.15,
    'tolaration': 16
}

key = ''
url = ''
def ip(request):
    return {'origin': request.headers.get('X-Forwarded-For', request.remote_addr)}


bannedADDR = []
_req__address_key_ = []

def timeout():
    time.sleep(100000)

message = {}

def generateKey(ip):
    key = randint(100000, 999999)
    found = False
    for ip_ in _req__address_key_:
        if ip_['ip'] == ip:
            ip_['key'] = key
            found = True
    
    if found == False:
        _req__address_key_.append(key)



def iSecWebLoadLogs():
    global ipConnADDR
    global bannedADDR
    global iSecWebConfig
    arr = []
    if os.path.isfile(iSecWebConfig['filename']) == False:
        file = open(iSecWebConfig['filename'], 'w')
        file.write(str(arr))
        file.close()
        file2 = open(iSecWebConfig['restrictionFN'], 'w')
        file2.write(str(arr))
        file2.close()

    newitem = open(iSecWebConfig['filename'], 'r')
    itemdata = newitem.read()
    itemdata = eval(itemdata)
    ipConnADDR = itemdata
    newitem.close()
    newitem2 = open(iSecWebConfig['restrictionFN'], 'r')
    itemdata2 = newitem2.read()
    newitem2.close()
    itemdata2 = eval(itemdata2)
    bannedADDR = itemdata2

print(bannedADDR)

def UploadData():
    global iSecWebConfig
    global ipConnADDR
    file = open(iSecWebConfig['filename'], 'w')
    file2 = open(iSecWebConfig['restrictionFN'], 'w')
    value = ipConnADDR
    value = str(value)
    value2 = bannedADDR
    value2 = str(value2)
    file2.write(value2)
    file.write(value)
    file.close()
    file2.close()

def banUserns(user):
    pass

def iSecWeb(ipADDRjson, url2):
        ipADDR = ipADDRjson['origin']
        timestamp = datetime.now()
        global url
        global message
        global ipConnADDR
        global iSecWebConfig
        global UploadData
        found = False
        url = url2
        item = {}
        for connecton in ipConnADDR:
            if connecton['ip'] == ipADDR:
                found = True
                item = connecton

        if found == True:
            lastConn = item['CTIT']
            item['CTIT'] = str(timestamp)
            lastConn = datetime.fromisoformat(lastConn)
            curr_time = timestamp - lastConn
            warrentTime = int(iSecWebConfig['connTime'])
            if curr_time.seconds < warrentTime:
                wp = item['WP']
                wp = wp + 1
                message = {'message': '[*] WARNING ip: '+str(item['ip'])+' is a threat, adding WP to this address.'}
                item['WP'] = wp
                UploadData()
            if int(item['WP'])<int(iSecWebConfig['tolaration']):
                return {'status': 'negative'}
            else:
                foundItem = False
                for ip in bannedADDR:
                    if ip['ip'] == item['ip']:
                        foundItem = True
                    
                if foundItem == True:
                    pass
                else:
                    bannedADDR.append(item)
                UploadData()
                if item['notified'] == False:
                    item['notified'] = True
                    message = {'message': '[*] INFO Ip: '+str(item['ip'])+' was banned from accessing the site.'}
                    print(message)
                return {'status': 'positive'}

            
        else:
            timestamp = str(timestamp)
            new = {
                'ip': ipADDR,
                'CTIT': timestamp,
                'notified': False,
                'WP': 0,
                'connections': 1
            }
            ipConnADDR.append(new)
            new = {}
            UploadData()
            return {'status': 'negative'}


def iSecWebApi(appname,route ,secretKey):
    api = Api(appname)
    global iSecWeb
    global UploadData
    class GetNF(Resource):
        def post(self):
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            status = iSecWeb(ip(request), url)
            if status['status'] == 'negative':
                if secretKey['key'] == child['key']:
                    return {'data': bannedADDR}
                else:
                    return {'status': 'unauthorized'}
            if status['status'] == 'positive':
                timeout()
                return {'message': 'banned'}

    api.add_resource(GetNF, route)

def debugMode(appname, keyname):
    api = Api(appname)
    global iSecWeb
    global UploadData
    global key
    key = keyname
    class GetLogs22(Resource):
        def post(self):
            child = request.get_data(False)
            child = child.decode()
            if 'key='+key == child:
                global message
                message2 = message
                print(message2)
                message = {}
                return message2
            else:
                return {'message': 'unauthotized'}
    class UploadLogs(Resource):
        def post(self):
            child = request.get_data(False)
            child = child.decode()
            global message
            if 'key='+key == child:
                message = {'message': child['message']}
                return {'status': 'updated'}
    api.add_resource(GetLogs22, '/isecweb/logs')
    api.add_resource(UploadLogs, '/isecweb/info')

def Check(app):
    @app.before_request
    def check():
        ipadr = ip(request=request)
        status = iSecWeb(ipadr, '')
        if status['status'] == 'positive':
            timeout()

