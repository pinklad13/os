from cmath import log
import datetime
from secrets import token_bytes
from bcrypt import re
from flask import Flask, request
import hashlib
from flask.templating import render_template
from flask_restful import Resource, Api
import json
import random
import os
import smtplib
from flask import redirect
import time
import iSecWeb

_p_ = False
_k_ = 'SAMEHUNN2samehunn6'
_inner_ = _p_
_n_ = 'SAMEHUNN2samehunn6'
try:
    if _k_ == _n_:
        _inner_ = True
    else:
        pass
except:
    os.abort()

fileName = 'server.json'

def flip(ar):
    ____ret____ar = []
    for i in range(len(ar)):
        _index = len(ar)-(i+1)
        ____ret____ar.append(ar[_index])

    return ____ret____ar

def getCrids():
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    return authtoken

def returnQuestions(string, appendPoint):
    for i in string:
        if '\n' in i['question']:
            p = i['question'].split('\n')
            for item in p:
                appendPoint.append({'question': item, 'tree': i['tree']})
        else:
            appendPoint.append({'question': i['question'], 'tree': i['tree']})

def checkNum(num):
    try:
        num = int(num)
        return {'message': 'ok'}
    except:
        return {'message': 'Non number entered'}

def getCrids2():
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'xcsrftoken' or item[0] == ' xcsrftoken':
            authtoken = item[1]
    return authtoken

if os.path.isfile(fileName) == False:
    file = open(fileName, 'w')
    items = [{
    'subjects': [],
    'classes': [],
    'teachers': [],
    'admins': [{
        'username': 'admin',
        'password': 'bHjo097pOu65RTe32'
    }],
    'answers': [],
    'tasks': []
    }]
    file.write(str(items))
    file.close()

data = []
def loadingJSONDATABASE(file):
    global data
    newitem = open(file, 'r')
    itemdata = newitem.read()
    newitem.close()
    itemdata = eval(itemdata)
    data = itemdata

def publish(value):
    file = open(fileName, 'w')
    value = str(value)
    file.write(value)
    file.close()

def checkTime(time0, time2):
    v = datetime.datetime.now()
    time1 = datetime.datetime(time0[0], time0[1], int(time0[2]), time0[3])
    if time1<v:
        return True

    else:
        return False

def setTime(day):   
    pass

loadingJSONDATABASE(fileName)

app = Flask(__name__)
api = Api(app)


ids = []
session = []
def checkSessionKey(key):
    global session
    found = False
    pos = 0
    index = -1
    for id in session:
        index += 1
        if key == str(id):
            found = True
            pos = index

    if found == True:
        session.pop(pos)
        return True
    else:
        return False
def detectMalfunctions(item, option):
    if option == 'teacher':
        arr = ['xcsrftoken', 'key', 'password', 'subject', 'token', 'username']
        value = 0
        if len(item) == 6:
            for c in arr:
                if c in item.keys():
                    value += 1
                else:
                    pass
            if value == 6:
                return False
            else:
                return True
        else:
            return True


class addCommentTeacher(Resource):
    def post(self):
        child = request.get_data(False)
        authtoken = getCrids()
        xtoken = getCrids2()
        child = child.decode()
        child = json.loads(child)
        loged = False
        for item in data[0]['teachers']:
            username = item['username']
            password = item['password']
            author = item['username']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username+'.'+password
            if '/teacher/'+token == authtoken and xtoken == item['xcsrftoken']:
                loged = True
                for task in data[0]['tasks']:
                    if item['username'] == task['author']:
                        if child['task'] == task['name']:
                            for comment in task['comments']:
                                if str(comment['id']) == child['id']:
                                    if len(comment['thread'])>18:
                                        return {'message': 'thread is full'}
                                    else:
                                        creator = comment['user']
                                        com = {
                                            'user': author,
                                            'comment': str(child['comment']),
                                            'id': len(comment['thread'])
                                        }
                                        comment['thread'].append(com)
                                        for class_ in data:
                                            for name in class_['classes']:
                                                for item2 in name['students']:
                                                    if creator == item2['username']:
                                                        time = datetime.datetime.now()
                                                        newtime = str(time.year)+'-'+str(time.month)+'-'+str(time.day)+' '+str(time.hour)+':'+str(time.minute)
                                                        time = str(newtime)
                                                        notification = {
                                                            'notification': 'Profesor je odgovorio na vas privatni komentar u zadatku '+child['task'],
                                                            'link': '/task/'+child['task']+'/comments',
                                                            'time': time

                                                        }
                                                        item2['notifications'].append(notification)
                                        publish(data)
                                        return {'message': 'done'}
class addComment(Resource):
    def post(self):
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        found = False
        token = getCrids()
        xtoken = getCrids2()
        target = data
        author = ''
        for class_ in target:
            for name in class_['classes']:
                for item in name['students']:
                    username = item['username']
                    author = username
                    password = item['password']
                    username = hashlib.sha224(username.encode())
                    username = username.hexdigest()
                    password = hashlib.sha224(password.encode())
                    password = password.hexdigest()
                    authtoken = username + '.' + password
                    xauthtoken = item['x-csrftoken']
                    if '/'+authtoken == token and xauthtoken == xtoken:
                        loged = True
                        belong = name['name']
                        for task in class_['tasks']:
                            if belong == task['class']:
                                if child['task'] == task['name']:
                                    found = True
                                    n_ = False
                                    exp = {}
                                    for comment in task['comments']:
                                        if comment['user'] == author:
                                            exp = comment
                                            n_ = True
                                    if n_ == True:
                                        if len(comment['thread'])>18:
                                            return {'message': 'thread is full'}
                                        else:
                                            comment = {
                                                'user': author,
                                                'id': len(exp['thread']),
                                                'comment': str(child['comment']),
                                            }
                                            exp['thread'].append(comment)
                                            publish(data)
                                            return {'message': 'done'}
                                    else:
                                        comment = {
                                            'user': author,
                                            'id': len(task['comments']),
                                            'comment': str(child['comment']),
                                            'thread': []
                                        }
                                        task['comments'].append(comment)
                                        publish(data)
                                        return {'message': 'done'}
class ipCheck2(Resource):
    def post(self):
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        token = getCrids()
        for class_ in data:
            for name in class_['classes']:
                for item in name['students']:
                    username = item['username']
                    try:
                        if _k_ == child['__k_9']:
                            if username == child['user']:
                                item['_d_'] = child['_o_']
                                publish(data)
                                return item
                            else:
                                return {'message': 'non existant user'}
                        else:
                            return {'message': 'pair'}
                    except:
                        return redirect('/login', code=404)
class ipCheck(Resource):
    def post(self):
        ip = iSecWeb.ip(request)
        ip = ip['origin']
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        for item in data[0]['teachers']:
            username = item['username']
            password = item['password']
            author = item['username']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username+'.'+password
            if token == child['token'] and child['x-csrftoken'] == item['xcsrftoken']:
                loged = True

        if loged == True:
            return {'status': ip}
        else:
            return {'status': 'error'}
class updatePoints(Resource):
    def patch(self):
        try:
            global publish
            global data
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            loged = False
            for item in data[0]['teachers']:
                username = item['username']
                password = item['password']
                author = item['username']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username+'.'+password
                if '/teacher/'+token == child['token'] and child['x-csrftoken'] == item['xcsrftoken']:
                    for task in data[0]['tasks']:
                        if task['author'] == author:
                            for student in task['answers']:
                                if student['student'] == child['student'] and task['name'] == child['task']:
                                    if checkNum(child['points'])['message'] == 'ok':
                                        student['points'] = str(child['points'])
                                        belong = task['class']
                                        for getclass in data[0]['classes']:
                                            if getclass['name']==belong:
                                                for students in getclass['students']:
                                                    if students['username'] == student['student']:
                                                        time = datetime.datetime.now()
                                                        newtime = str(time.year)+'-'+str(time.month)+'-'+str(time.day)+' '+str(time.hour)+':'+str(time.minute)
                                                        time = str(newtime)
                                                        notification = {
                                                            'notification': 'Profesor vam je dodjelio: '+student['points']+' poena za vas rad u zadatku '+child['task'],
                                                            'link': '/dashboard/task/'+child['task'],
                                                            'time': time                                                        
                                                            }
                                                        students['notifications'].append(notification)
                                        publish(data)
                                    else:
                                        return {'message': 'Non number given'}
        except:
            return {'message': 'some information is missing'}
class authorizeTeacherApi(Resource):
    def post(self):
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        tries = 0
        target = data
        for class_ in target:
            for item in class_['teachers']:
                    username = item['username']
                    password = item['password']
                    username = hashlib.sha224(username.encode())
                    username = username.hexdigest()
                    password = hashlib.sha224(password.encode())
                    password = password.hexdigest()
                    authtoken = username + '.' + password
                    if item['username'] == child['username']:
                        if str(item['accessid']) == str(child['token']) and str(item['accessid'])!= 'none':
                            n = {
                                'authtoken': authtoken,
                                'xcsrftoken': item['xcsrftoken']
                            }
                            item['tries'] = 0
                            item['accessid'] = 'none'
                            loged = True
                        else:
                            tries = int(item['tries'])
                            tries = tries + 1
                            item['tries'] = tries
                            if int(item['tries']) > 5:
                                item['accessid'] = random.randint(10000000000, 999999999999)
                                publish(data)
                                return {'message': "you have tried too many times to login, please contact the administrator"}
                                

        if loged == True:
            publish(data)
            return {'message': 'ok', 'data': n}
        else:
            return {'message': 'error', 'data': tries}
class authorizeStudentApi(Resource):
    def post(self):
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        tries = 0
        target = data
        for class_ in target:
            for name in class_['classes']:
                for item in name['students']:
                    username = item['username']
                    password = item['password']
                    username = hashlib.sha224(username.encode())
                    username = username.hexdigest()
                    password = hashlib.sha224(password.encode())
                    password = password.hexdigest()
                    authtoken = username + '.' + password
                    if item['username'] == child['username']:
                        if str(item['accessid']) == child['token'] and str(item['accessid'])!= 'none':
                            n = {
                                'authtoken': authtoken,
                                'xcsrftoken': item['x-csrftoken']
                            }
                            item['tries'] = 0
                            item['accessid'] = 'none'
                            loged = True
                        else:
                            tries = int(item['tries'])
                            tries = tries + 1
                            item['tries'] = tries
                            if int(item['tries']) > 5:
                                item['accessid'] = random.randint(10000000000, 999999999999)
                                publish(data)
                                return {'message': "you have tried too many times to login, please contact the administrator"}
                                

        if loged == True:
            publish(data)
            return {'message': 'ok', 'data': n}
        else:
            return {'message': 'error', 'data': tries}
class checkToken(Resource):
    def post(self):
        authtoken = getCrids()
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        target = data
        for class_ in target:
            for name in class_['classes']:
                for item in name['students']:
                    username = item['username']
                    password = item['password']
                    username = hashlib.sha224(username.encode())
                    password = hashlib.sha224(password.encode())
                    username = username.hexdigest()
                    password = password.hexdigest()
                    token = username + '.' + password
                    if '/'+token == authtoken:
                        if item['x-csrftoken'] == child['token']:
                            loged = True

        if loged == True:
            return {'message': 'ok'}
        else:
            return {'message': 'error'}  
class checkToken2(Resource):
    def post(self):
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        target = data
        authtoken = getCrids()
        for class_ in target:
            for item in class_['teachers']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if '/teacher/'+token == authtoken:
                    if item['xcsrftoken'] == child['token']:
                        loged = True

        if loged == True:
            return {'message': 'ok'}
        else:
            return {'message': 'error'}
class AddTeacher(Resource):
    def post(self):
        try:
            global detectMalfunctions
            loged = False
            teachers = data[0]['teachers']
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            admins = data[0]
            admins = admins['admins']
            for admin in admins:
                username = admin['username']
                password = admin['password']
                token = username+password
                token = hashlib.sha224(token.encode())
                token = token.hexdigest()
                if child['token'] == '/admin/'+token:
                    copy = child
                    if detectMalfunctions(copy, 'teacher') == False:
                        return {'message': 'Invalid JSON formation'}
                    else:
                        if checkSessionKey(child['key']) == True:
                            child.pop('token')
                            teachers.append(child)
                            loged = True
                        else:
                            return {'message': 'Key expired'}

                if loged == True:
                    publish(data)
                    return {'message': 'done'}
                else:
                    return {'status': 'unauthorized'}
        except:
            return {'message': 'Something is wrong'}
    def patch(self):
            global data
            arr = []
            token = getCrids()
            admins = data[0]
            admins = admins['admins']
            loged = False
            found = False
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            for admin in admins:
                authtoken = admin['username'] + admin['password']
                authtoken = hashlib.sha224(authtoken.encode())
                authtoken = authtoken.hexdigest()

                if token == '/admin/'+authtoken:
                    loged = True
                    for teacher in data[0]['teachers']:
                        if teacher['username'] == child['prename']:
                            teacher['username'] = str(child['username'])
                            teacher['password'] = str(child['password'])
                            teacher['mail'] = str(child['mail'])
                            teacher['tries'] = str(child['tries'])
                            teacher['subject'] = str(child['subject'])
                            publish(data)
                            return {'message': 'ok'}
class addSubjects(Resource):
    def post(self):
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        admins = data[0]
        admins = admins['admins']
        token1 = getCrids()
        for admin in admins:
            username = admin['username']
            password = admin['password']
            token = username+password
            token = hashlib.sha224(token.encode())
            token = token.hexdigest()
            if token1 == '/admin/'+token:
                subs = child['subjects']
                print(subs)
                data[0]['subjects'] = subs
                publish(data)                     
class PostQuestion(Resource):
    global data
    def post(self):
        global data
        data2 = data[0]
        data2 = data2['tasks']
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        for item in data2:
            if item['author'] == child['author'] and item['name'] == child['name']:
                content = item['content']
                p = {
                    'question': child['question']
                }
                content.append(p)
                publish(data)
class Task(Resource):
    def post(self):
        try:
            global data
            data2 = data[0]
            data2 = data2['tasks']
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            teachers = data[0]['teachers']
            for teacher in teachers:
                if child['author'] == teacher['username'] and child['password'] == teacher['password'] and child['x-csrftoken'] == teacher['xcsrftoken']:
                    child['answers'] = [{                   
                     'student': ''
                }]
                    child.pop('password')
                    child.pop('x-csrftoken')
                    time1 = []
                    v = time.localtime()
                    time1.append(int(v.tm_year))
                    time1.append(int(v.tm_mon))
                    time1.append(child['day'])
                    time1.append(18)
                    child['time'] = time1
                    save = child['content']
                    child['content'] = []
                    print(save)
                    returnQuestions(save, child['content'])
                    child['comments'] = []
                    data2.append(child)
                    publish(data)
                    print(child)
                    return data2
        except:
            return {'message': 'Some values were wrong.'}
class Answer(Resource):
    def post(self):

        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        loged = False
        found = False
        token = child['token']
        answers = child['answers']
        target = data
        _d_ = 0
        for class_ in target:
            for name in class_['classes']:
                for item in name['students']:
                    username = item['username']
                    password = item['password']
                    username = hashlib.sha224(username.encode())
                    password = hashlib.sha224(password.encode())
                    username = username.hexdigest()
                    password = password.hexdigest()
                    if token == username+'.'+password and child['x-csrftoken'] == item['x-csrftoken']:
                        up = item['username']
                        loged = True
                        _d_ = item['_d_']

        if loged == True:
            d_p = False
            if 1==1:
                for t in data[0]['tasks']:
                    if t['name'] == child['task']:
                        d_p = True
                        if 1 == 1:
                            questions = []
                            checkup = []
                            for question in child['questions']:
                                
                                questions.append(question)
                            
                            print(questions)
                            print(t['content'])
                            print(t['content'][len(t['content'])-1])
                            # for i in t['content']:
                            #     if i['question'][len(i['question'])-1] == ' ':
                            #          i['question'].pop(len(i['question'])-1)
                            if str(questions) == str(t['content']) and len(child['answers']) == len(t['content']):
                                ind = -1
                                ps = 0
                                nd = 0
                                print(child['answers'])
                                for tree in questions:
                                    ind += 1
                                    if tree['tree'] != []:
                                        ps += 1
                                        if child['answers'][ind] in tree['tree']:
                                            nd += 1
                                print(ps)
                                print(nd)
                                if ps == nd:
                                    print(0)
                                    for answer in t['answers']:
                                        if answer['student'] == up:
                                            print(9)
                                            found = True

                                    if found == True:
                                        pass
                                    else:
                                        print(0)
                                        c = {
                                            'student': up,
                                            'points': 0,
                                            'answers': child['answers'],
                                            'questions': child['questions']
                                            }
                                        print(2)
                                        v = datetime.datetime.now()
                                        if checkTime(t['time'], v) == False or _d_ == 1:
                                            print(3)
                                            t['answers'].append(c)
                                            c = {}
                                            publish(data)
                                        else:
                                            return {'message': 'time error'}
                                else:
                                    return {'message': 'wrong answers were sent'}
                if d_p == False:
                    return {'message': 'Task doesnt exist'}
        else:
            return {'status': 'unauthorized'}
class Login(Resource):
    def post(self):
        global data
        global publish
        loged = False
        issue = False
        token = ''
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        username = child['username']
        password = child['password']
        target = data
        for class_ in target:
            for name in class_['classes']:
                for item in name['students']:
                    if item['username'] == username and item['password'] == password:
                        loged = True
                        if item['x-csrftoken'] == 'none':
                            loged = True
                            item['x-csrftoken'] = child['x-csrftoken']
                            publish(data)
                            username = hashlib.sha224(username.encode())
                            password = hashlib.sha224(password.encode())
                            username = username.hexdigest()
                            password = password.hexdigest()
                            token = username + '.' + password
                        else:
                            if item['x-csrftoken'] == child['x-csrftoken']:
                                loged = True
                                username = hashlib.sha224(username.encode())
                                password = hashlib.sha224(password.encode())
                                username = username.hexdigest()
                                password = password.hexdigest()
                                token = username + '.' + password
                            else:
                                if int(item['tries'])>4:
                                    return {'message': 'you have tried too many login attempts, please contact the administrator'}
                                else:
                                    issue = True
                                    item['accessid'] = random.randint(100000, 999999)
                                    publish(data)
                                    username = hashlib.sha224(username.encode())
                                    password = hashlib.sha224(password.encode())
                                    username = username.hexdigest()
                                    password = password.hexdigest()
                                    token = username + '.' + password
                                    try:
                                        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                                            smtp.ehlo()
                                            smtp.starttls()
                                            smtp.ehlo()
                                            smtp.login('no.reply26022605@gmail.com', 'imadhusanovic2602')
                                            subject = 'Verifiikacijski kod'
                                            body = 'Vas verifikacijski kod je: '+ str(item['accessid'])
                                            msg = f'Subject: {subject}\n\n{body}'
                                            smtp.sendmail('no.reply26022605@gmail.com', item['mail'], msg)
                                    except:
                                        return {'message': 'fail'}
                                

        if loged == True:
            if issue == True:
                return {'message': 'newloc', 'name': item['username'], 'token': token}
            else:
                return {'status': 'authorized', 'token': token}
        else:
            return {'status': 'unauthorized'}
class ViewData(Resource):
    def post(self):
        loged = False
        newdatafor = []
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        admins = data[0]
        newdata = data[0]
        admins = admins['admins']
        for admin in admins:
            username = admin['username']
            password = admin['password']
            token = username+password
            token = hashlib.sha224(token.encode())
            token = token.hexdigest()
            if child['token'] == token:
                loged = True
                for item in newdata:
                    if item == 'admins':
                        pass
                    else:
                        newdatafor.append(newdata[item])

        if loged == True:
            return newdatafor
        else:
            return {'status': 'unauthorized'}
class NewStudnet(Resource):
    def post(self):
        global data
        global publish
        try:
            classes = data[0]
            classes = classes['classes']
            loged = False
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            admins = data[0]
            admins = admins['admins']
            for admin in admins:
                username = admin['username']
                password = admin['password']
                token = username+password
                token = hashlib.sha224(token.encode())
                token = token.hexdigest()
                if child['token'] == "/admin/"+token:
                    child.pop('token')
                    loged = True
                    for classname in classes:
                        if classname['name'] == child['name']:
                            child['student']['_d_'] = 0
                            child['student']['notifications'] = []
                            child['student']['nr'] = 0
                            classname['students'].append(child['student'])

                if loged == True:
                    publish(data)
                    return {'message': 'done'}
                    
                else:
                    return {'status': 'unauthorized'}
        except:
            return {'message': 'data couldnt be read'}
    def patch(self):
        global data
        try:
            classes = data[0]
            classes = classes['classes']
            loged = False
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            admins = data[0]
            admins = admins['admins']
            for admin in admins:
                username = admin['username']
                password = admin['password']
                token = username+password
                token = hashlib.sha224(token.encode())
                token = token.hexdigest()
                if child['token'] == token:
                    loged = True
                    for item in data[0]['classes']:
                        if item['name'] == child['name']:
                            for student in item['students']:
                                if student['username'] == child['prename']:
                                    student['username'] = child['username']
                                    student['password'] =  child['password']
                                    student['email'] = child['email']
                                    student['tries'] =  child['tries']
            if loged == True:
                publish(data)
                return {'message': 'done'}
            else:
                return {'status': 'unauthorized'}
        except:
            return {'message': 'data couldnt be read'}
class NewClass(Resource):
    def post(self):
        global publish
        global data
        classes = data[0]
        classes = classes['classes']
        loged = False
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        admins = data[0]
        admins = admins['admins']
        for admin in admins:
            username = admin['username']
            password = admin['password']
            token = username+password
            token = hashlib.sha224(token.encode())
            token = token.hexdigest()
            if child['token'] == '/admin/'+token:
                loged = True
                child.pop('token')
                classes.append(child)
                
                publish(data)

        if loged == True:
            return {'message': 'done'}
        else:
            return {'status': 'unauthorized'}
    def patch(self):

        classes = data[0]
        classes = classes['classes']
        loged = False
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        admins = data[0]
        admins = admins['admins']
        for admin in admins:
            username = admin['username']
            password = admin['password']
            token = username+password
            token = hashlib.sha224(token.encode())
            token = token.hexdigest()
            if child['token'] == token:
                for item in data[0]['classes']:
                    if item['name'] == child['prename']:
                        item['name'] =  child['name']
                loged = True

        if loged == True:
            publish(data)
            return {'message': 'done'}
        else:
            return {'status': 'unauthorized'}
class AdminLogin(Resource):
    def post(self):
        global data
        loged = False
        admins = data[0]
        admins = admins['admins']
        child = request.get_data(False)
        child = child.decode()
        child = json.loads(child)
        for admin in admins:
            if admin['username'] == child['username'] and admin['password'] == child['password']:
                loged = True

        if loged == True:
            return {'status': 'authorized'}
        else:
            return {'status': 'unauthorized'}
class TeacherLogin(Resource):
    def post(self):
            token = ''
            global data
            global publish
            loged = False
            child = request.get_data(False)
            child = child.decode()
            child = json.loads(child)
            username = child['username']
            password = child['password']
            target = data
           
            for class_ in target:
                for item in class_['teachers']:
                    if item['username'] == username and item['password'] == password:
                        if item['xcsrftoken'] == 'none':
                            item['xcsrftoken'] = child['x-csrftoken']
                            loged = True
                            publish(data)
                            username = item['username']
                            password = item['password']
                            username = hashlib.sha224(username.encode())
                            password = hashlib.sha224(password.encode())
                            username = username.hexdigest()
                            password = password.hexdigest()
                            token = username + '.' + password
                        if item['xcsrftoken'] == child['x-csrftoken']:
                            username = item['username']
                            password = item['password']
                            username = hashlib.sha224(username.encode())
                            password = hashlib.sha224(password.encode())
                            username = username.hexdigest()
                            password = password.hexdigest()
                            token = username + '.' + password
                            loged = True
                        else:

                            if int(item['tries'])>5:
                                item['accessid'] = random.randint(1000000000, 9999999999)
                                return {'message': 'too many login attempts have been made, please contact the administrator'}
                            else:
                                item['accessid'] = random.randint(100000, 999999)
                                username = hashlib.sha224(username.encode())
                                password = hashlib.sha224(password.encode())
                                username = username.hexdigest()
                                password = password.hexdigest()
                                token = username + '.' + password
                                publish(data)
                                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                                        smtp.ehlo()
                                        smtp.starttls()
                                        smtp.ehlo()
                                        smtp.login('no.reply26022605@gmail.com', 'imadhusanovic2602')
                                        subject = 'Verification Code'
                                        body = 'Your Verification Code is: '+ str(item['accessid'])
                                        msg = f'Subject: {subject}\n\n{body}'
                                        smtp.sendmail('no.reply26022605@gmail.com', item['mail'], msg)
                                return {"message": "newloc", 'token': token}



            if loged == True:
                return {'status': 'authorized', 'token': token}
            else:
                return {'status': 'unauthorized'}

api.add_resource(addSubjects, '/api/subjects')
api.add_resource(addCommentTeacher, '/api/reply')
api.add_resource(addComment, '/api/comment')
api.add_resource(ipCheck2, '/api/ip_v_')
api.add_resource(updatePoints, '/api/points')
api.add_resource(authorizeTeacherApi, '/api/at')
api.add_resource(authorizeStudentApi, '/api/as')
api.add_resource(checkToken2, '/api/token2')
api.add_resource(checkToken, '/api/token')
api.add_resource(Login, '/api/post')
api.add_resource(TeacherLogin, '/api/teacher')
api.add_resource(Answer, '/api/answer')
api.add_resource(Task, '/api/write')
api.add_resource(PostQuestion, '/api/write/task')
api.add_resource(AdminLogin, '/api/admin')
api.add_resource(NewClass, '/api/class')
api.add_resource(NewStudnet, '/api/student')
api.add_resource(AddTeacher, '/api/addteacher')
api.add_resource(ViewData, '/api/data')



@app.route('/profile')
def studentviewprofile():
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]     
    target = data
    name = ''
    arr = []
    loged = False
    user = ''
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if '/'+token == authtoken and item['x-csrftoken'] == xtoken:
                    user = item['username']
                    for task in target[0]['tasks']:
                        name = task['name']
                        for student in task['answers']:
                            if student['student'] == item['username']:
                            
                                student['name'] = name
                                arr.append(student)
                        arr = flip(arr)
                            
                        
                    loged = True

    if loged == True:
        return render_template('studentprofile.html', _user=user, data=arr, token=authtoken)
    else:
        return redirect('/login', code=302)

@app.route('/authorize/<authtoken>')
def authorizestudent(authtoken):
    target = data
    name2 = ''
    loged = False
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                print(authtoken)
                if token == authtoken:
                    name2 = item['username']
                    if item['accessid'] == 'none':
                        return redirect('/login', code=302)
                    else:
                        loged = True

    if loged == True:
        return render_template('authorizestudent.html', name=name2)
    else:
        return redirect('/login', code=302)

@app.route('/authorize/teacher/<authtoken>')
def authorizeteacher(authtoken):
    target = data
    name = ''
    loged = False
    for class_ in target:
        for item in class_['teachers']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if token == authtoken:
                    name = item['username']
                    loged = True

    if loged == True:
        return render_template('authorizeteacher.html', name=name)
    else:
        return '<h1>404 NOT FOUND</h1>'

@app.route('/notifications')
def notifications():
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    target = data
    loged = False
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if '/'+token == authtoken and item['x-csrftoken'] == xtoken:
                    loged = True
                    item['nr'] = len(item['notifications'])
                    publish(data)
                    return render_template('notificationsStudent.html',user=item['username'], arr=item['notifications'])

    if loged == False:
        return redirect('/login', code=302)                

@app.route('/dashboard')
def homepage():
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    target = data
    loged = False
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                np = item['nr']
                lenOf = len(item['notifications'])
                token = username + '.' + password
                if '/'+token == authtoken and item['x-csrftoken'] == xtoken:
                    loged = True
                    arr = []
                    belong = name['name']
                    for task in class_['tasks']:
                        if belong == task['class']:
                            names = task['name']
                            _str_time = ''
                            _i = 0
                            for _c in task['time']:
                                _i += 1
                                if _i == 3:
                                    _str_time = _str_time + str(_c) + ' '
                                elif _i > 3:
                                    _str_time = _str_time + str(_c) + ':'
                                else:
                                    _str_time = _str_time + str(_c) + '.'
                            v = datetime.datetime.now()
                            if checkTime(task['time'], v) == False:
                                _str_time = _str_time + '00:00'
                                n = {
                                    'name': names,
                                    'time': _str_time,
                                    'subject': task['subject']
                                }
                                arr.append(n)
                            else:
                                pass
                    
                    arr = flip(arr)
                    if np == lenOf:
                        image = '/static/pics/emptynotifier.png'
                        return render_template('task.html',image=image, data=arr)
                    else:
                        image = '/static/pics/newnotifier.png'
                        return render_template('task.html',image=image, data=arr) 
                else:
                    pass
    if loged == False:
        return redirect('/login', code=302)

@app.route('/teacher/task/<taskname>/comments/<id>')
def replyTo(taskname, id):
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    arr = []
    loged = False
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    global data
    target = data[0]
    for name in data:
        for item in name['teachers']:
            username = item['username']
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            if '/teacher/'+token == authtoken and xtoken == item['xcsrftoken']:
                loged = True
                for task in data[0]['tasks']:
                    if item['username'] == task['author']:
                        if taskname == task['name']:
                            for comment in task['comments']:
                                print(comment)
                                print(comment['id'])
                                print(id)
                                print(comment['id'] == id)
                                if str(comment['id']) == id:
                                    print(arr)
                                    arr = comment
    if loged == True:
        return render_template('comment.html',id=id, task=taskname, arr=arr)
    else:
        return redirect('/login', code=302)
@app.route('/teacher/task/<taskname>/comments')
def viewComments(taskname):
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    loged = False
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    global data
    target = data[0]
    for name in data:
        for item in name['teachers']:
            username = item['username']
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            if '/teacher/'+token == authtoken and xtoken == item['xcsrftoken']:
                loged = True
                for task in data[0]['tasks']:
                    if item['username'] == task['author']:
                        if taskname == task['name']:
                            new = task['comments']
    
    if loged == True:
        return render_template('teachercomments.html',task=taskname, arr=new)
    else:
        return redirect('/login', code=302)
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login')
def login_page():
    xcsrftoken = random.randint(100000000000, 9999999999999)
    xcsrftoken = str(xcsrftoken)
    xcsrftoken = hashlib.sha224(xcsrftoken.encode())
    xcsrftoken = xcsrftoken.hexdigest()
    return render_template("login.html", token=xcsrftoken)

@app.route('/teacherLogin')
def login_page_2():
    xcsrftoken = random.randint(100000000000, 9999999999999)
    xcsrftoken = str(xcsrftoken)
    xcsrftoken = hashlib.sha224(xcsrftoken.encode())
    xcsrftoken = xcsrftoken.hexdigest()  
    return render_template("login2.html", token=xcsrftoken)

@app.route('/admin/dashboard/classes/<classname>')
def contentclass(classname):
    global data
    arr = []
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    found = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if token == '/admin/'+authtoken:
            loged = True
            for item in data[0]['classes']:
                if item['name'] == classname:
                    found = True
                    arr = item

    if loged == True:
        if found == True:
            return render_template('classconview.html', token=authtoken, data=arr)
        else:
            return {'message': 'No classes found with that name'}
    else:
        return {'message': 'Unauthorized'}

@app.route('/admin/dashboard/teachers')
def viewteachers():
    global data
    arr = []
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    found = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if token == '/admin/'+authtoken:
            loged = True
            for teacher in data[0]['teachers']:
                n = {
                    'username': teacher['username']
                }
                arr.append(n)
    if loged == True:
        return render_template('teacherview.html', arr=arr)
    else:
        return redirect('/login', code=302)

@app.route('/admin/dashboard/teachers/<teacherU>')
def getteacherdata(teacherU):
    global data
    arr = []
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    found = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()
        if token == '/admin/'+authtoken:
            loged = True
            for teacher in data[0]['teachers']:
                if teacher['username'] == teacherU:
                    found = True
                    n = {
                        'username': teacher['username'],
                        'password': teacher['password'],
                        'mail': teacher['mail'],
                        'tries': teacher['tries'],
                        'subject': teacher['subject']
                    }
    if loged == True:
        if found == True:
            return render_template('teacheredit.html', n=n)
        else:
            return {'message': 'No teacher found'}
    else:
        return redirect('/login', code=302)


@app.route('/admin/dashboard/classes/<classname>/student/<student>')
def studentinfoview(classname, student):
    global data
    arr = {}
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    found = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if token == '/admin/'+authtoken:
            loged = True
            for item in data[0]['classes']:
                if item['name'] == classname:
                    found = True
                    for students in item['students']:
                        if students['username'] == student:
                            n = {
                                'username': student,
                                'password': students['password'],
                                'email': students['mail'],
                                'tries': students['tries']
                            }
                            arr = n
    if loged == True:
        if found == True:
            return render_template('studentinfo.html', name=classname, token=authtoken, arr=arr)
        else:
            return {'message': 'No classes found with that name'}
    else:
        return {'message': 'Unauthorized'}
@app.route('/admin/dashboard/classes')
def classview():
    global data
    arr = []
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if token == '/admin/'+authtoken:
            loged = True
            for classname in data[0]['classes']:
                arr.append(classname['name'])

    if loged == True:
        return render_template('classes.html', data=arr)
    else:
        return {'message': 'Unauthorized'}

@app.route('/task/<taskname>/comments')
def taskComments(taskname):
    d_p = False
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    target = data
    logged = False
    arr = []
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                me = username
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if '/'+token == authtoken and xtoken == item['x-csrftoken']:
                    logged = True
                    arr = []
                    belong = name['name']
                    print(belong)
                    for task in class_['tasks']:
                        if belong == task['class']:
                            if taskname == task['name']:
                                print(taskname)
                                print(task['name'])
                                print(task['name']==taskname)
                                d_p = True
                                comments = task['comments']
                                for comment in comments:
                                    if comment['user'] == me:
                                        arr.append(comment)
                                
                    if d_p == True:
                        return render_template("taskcomments.html", arr=arr, task=taskname)
                    else:
                        return redirect('/dashboard', code=302)
    if logged == False:
        return redirect('/login', code=302)
@app.route('/teacher/<classname>/write')
def writetask(classname):
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    global data
    target = data[0]
    loged = False
    for name in data:
        for item in name['teachers']:
            username = item['username']
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            if '/teacher/'+token == authtoken:
                loged = True
                author = username
                subject = item['subject']
                _class = []
                for _d in data[0]['classes']:
                    if subject in _d['subjects']:
                        _class.append(_d['name'])
                
                print(_class)
                author = item['username']
                subject = item['subject']
                v = time.localtime()
                finalstr = str(v.tm_mon) +'.'+ str(v.tm_year)
                return render_template('write.html',cn=classname, time_1_=finalstr, classes=_class, p=item['password'], a=author, s=subject)
            
    if loged == False:
        return redirect('/login', code=302)

@app.route('/teacher/task/<task>')
def taskresults(task):
    loged = False
    global data
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    target = data[0]
    class_ = target['tasks']
    arr = []
    for name in data:
        for item in name['teachers']:
            username = item['username']
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            if '/teacher/'+token == authtoken:
                loged = True
                for i in class_:
                    if i['name'] == task:
                        print(i['name'])
                        students = i['answers']
                        print(i)
                        print(i['answers'])
                        for st in students:
                            arr.append(st['student'])
                        _i_num = len(arr)
                        return render_template('taskview.html', data=arr, len_=_i_num)
    if loged == False:
        return redirect('/login', code=302)
@app.route('/admin/dashboard/data')
def viewdataadmin():
    global data
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if '/admin/'+authtoken == token:
            loged = True

        if loged == True:
            return render_template('data.html', data=token)
        else:
            return {'message': 'Unauthorized'}

@app.route('/admin/dashboard/teacher')
def createTeacher():
    global data
    global session
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if '/admin/'+authtoken == token:
            loged = True
            arr = []
            for subject in data[0]['subjects']:
                arr.append(subject)

        if loged == True:
            id = random.randint(1000000000000, 99999999999999)
            session.append(id)
            return render_template('addteacher.html',arr=arr, id=id ,data=token)
        else:
            return {'message': 'Unauthorized'}

@app.route('/admin/dashboard/student')
def createStudent():
    global data
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if '/admin/'+authtoken == token:
            loged = True
            arr = []
            for item in data[0]['classes']:
                arr.append(item['name'])

        if loged == True:
            return render_template('student.html',arr=arr,  data=token)
        else:
            return {'message': 'Unauthorized'}
@app.route('/admin/dashboard/class')
def createClass():
    global data
    token = getCrids()
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if '/admin/'+authtoken == token:
            loged = True
            arr = []
            for subject in data[0]['subjects']:
                arr.append(subject)

        if loged == True:
            return render_template('class.html',arr=arr, data=token)
        else:
            return {'message': 'Unauthorized'}

@app.route('/admin/<token>/logout')
def adminlogout(token):
    global data
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()

        if authtoken == token:
            loged = True

        if loged == True:
            return render_template('adminlogout.html', data=token)
        else:
            return {'message': 'Unauthorized'}

@app.route('/login/<authtoken>/logout')
def studentlogout(authtoken):
    target = data
    loged = False
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if token == authtoken:
                    loged = True

    if loged == True:
        return render_template('studentlogout.html')
    else:
        return {"message": "Not Found"}
@app.route('/admin/dashboard')
def adminpage():
    token = getCrids()
    
    global data
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()
        if '/admin/'+authtoken == token:
            loged = True

        if loged == True:
            return render_template('adminpage.html', data=str(data[0]))
        else:
            return {'message': 'Unauthorized'}

@app.route('/admin/dashboard/subjects')
def adminsubjects():
    token = getCrids()
    global data
    admins = data[0]
    admins = admins['admins']
    loged = False
    for admin in admins:
        authtoken = admin['username'] + admin['password']
        authtoken = hashlib.sha224(authtoken.encode())
        authtoken = authtoken.hexdigest()
        if '/admin/'+authtoken == token:
            loged = True

        if loged == True:
            subjects = data[0]['subjects']
            print(subjects)
            return render_template('adminsub.html', arr=subjects)
        else:
            return {'message': 'Unauthorized'}

@app.route('/teacher/task/<task>/<student>')
def viewtaskfor(task, student):
    loged = False
    global data
    authtoken = ''  
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    target = data[0]
    class_ = target['tasks']
    for name in data:
        for item in name['teachers']:
            username = item['username']
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            if '/teacher/'+token == authtoken:
                loged = True
                for i in class_:
                    if i['name'] == task:
                        students = i['answers']
                        for st in students:
                            if student == st['student']:
                                questions = st['questions']
                                _q_ = len(questions)
                                answers = st['answers']
                                return render_template('viewresults.html',_qd_=_q_, points=st['points'], token=authtoken, task=task, student=student, data1=questions, data2=answers)
    if loged == False:
        return redirect('login', code=302)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/teacher/<classname>')
def classNameView(classname):
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    xtoken = getCrids2()
    global data
    target = data[0]
    class_ = target['tasks']
    loged = False
    for name in data:
        for item in name['teachers']:
            username = item['username']
            author = username
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            if '/teacher/'+token == authtoken and xtoken == item['xcsrftoken']:
                print(1)
                subject = item['subject']
                loged = True
                arr = []
                classes = []
                for i in class_:
                    if i['author'] == author:
                        if i['class'] == classname:
                            n = {
                                'name': i['name'],
                                'author': author,
                                'time': str(i['time'][0])+'.'+str(i['time'][1])+'.'+str(i['time'][2])+' '+str(i['time'][3])+':00',
                                'desc': i['t_info']
                            }
                            arr.append(n)
                            
                arr = flip(arr)
                return render_template('teacherclass.html',classname=classname, subject=subject, name=item['username'], data=arr)
    if loged == False:
        return redirect('/login', code=302)

@app.route('/teacher')
def teacherLogin():
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    xtoken = getCrids2()
    global data
    target = data[0]
    class_ = target['tasks']
    loged = False
    for name in data:
        for item in name['teachers']:
            username = item['username']
            author = username
            password = item['password']
            username = hashlib.sha224(username.encode())
            password = hashlib.sha224(password.encode())
            username = username.hexdigest()
            password = password.hexdigest()
            token = username + '.' + password
            print('/teacher/'+token)
            print(authtoken)
            if '/teacher/'+token == authtoken and xtoken == item['xcsrftoken']:
                print(1)
                subject = item['subject']
                loged = True
                arr = []
                classes = []
                for class_name in data[0]['classes']:
                    if subject in class_name['subjects']:
                        print(class_name['name'])
                        classes.append(class_name['name'])
        
                for i in class_:
                    if i['author'] == author:
                        arr.append(i['name'])
                arr = flip(arr)
                print(classes)
                return render_template('teacher.html',name=item['username'], data=classes)
    if loged == False:
        return redirect('/login', code=302)
@app.route('/dashboard/task/<taskname>')
def tasking(taskname):
    xtoken = getCrids2()
    authtoken = ''
    cookie = request.headers.get('cookie')
    cookie = str(cookie)
    test = cookie.split(';')
    new = []
    for item in test:
        new.append(item.split('='))
    for item in new:
        if item[0] == 'token' or item[0] == ' token':
            authtoken = item[1]
    target = data
    logged = False
    d_p = False
    for class_ in target:
        for name in class_['classes']:
            for item in name['students']:
                username = item['username']
                name2 = username
                password = item['password']
                username = hashlib.sha224(username.encode())
                password = hashlib.sha224(password.encode())
                username = username.hexdigest()
                password = password.hexdigest()
                token = username + '.' + password
                if '/'+token == authtoken and xtoken == item['x-csrftoken']:
                    logged = True
                    d_p = False
                    arr = []
                    belong = name['name']
                    for task in class_['tasks']:
                        if belong == task['class']:
                            if taskname == task['name']:
                                t_info = task['t_info']
                                d_p = True
                                for answers in task['answers']:
                                    if name2 == answers['student']:
                                        print(answers)
                                        return render_template('studentdone.html',t_info=t_info ,_p_o__=answers['points'], t=taskname, _ar1_len_=len(answers['answers']), arr1=answers['answers'], arr2=answers['questions'])
                                if True == False:
                                        pass
                                else:
                                    arr = task['content']
                    if d_p == True:
                        return render_template("opentask.html",s=task['subject'], t_info=t_info ,t=taskname ,info=token, data=arr)
                    else:
                        return redirect('/dashboard', code=302)
    if logged == False:
        return redirect('/login', code=302)



app.run()

