    
        var url = document.cookie
        var content = url.split(';')
        var data = []
        var token = ''
                    var content = url.split(';')
                    var data = []
                    for (var i = 0; i < content.length; i++) {
                        data.push(content[i].split('='));
                    }
                    for (var i = 0; i < data.length; i++) {
                        if (data[i][0]==' xcsrftoken' || data[i][0]=='xcsrftoken') {
                            token = data[i][1]
                        }
                        else {
                            token = t_
                        }
                    }
        var url = document.cookie
        var content = url.split(';')
        var data = []
        for (var i = 0; i < content.length; i++) {
            data.push(content[i].split('='));
        }
        for (var i = 0; i < data.length; i++) {
            if (data[i][0]==' data' || data[i][0]=='data') {
                if (data[i][1]='1') {
                    window.location.href = '/dashboard'
                }
                else if (data[0][1]=='2') {
                    window.location.href = '/teacher'
                }
                else if (data[0][1]=='0') {
                    window.location.href = '/admin'
                }
            }
                
        }
        var selected = 0
        function opt1() {
            var p1 =  document.getElementById('checked1')
            var p2 = document.getElementById('checked2')

            p1.style.background = "rgb(19, 19, 19)"
            p2.style.background = "whitesmoke"
            selected = 1
        }
        function opt2() {
            var p1 =  document.getElementById('checked1')
            var p2 = document.getElementById('checked2')

            p2.style.background = "rgb(19, 19, 19)"
            p1.style.background = "whitesmoke"
            selected = 2
        }
        function login() {
            var text = document.getElementById('text1')
            text.innerHTML = "..."
            if (selected == 0) {
                
            }
            else {
                if (selected==2) {
                    var cookie = document.cookie
                    
                    var u = document.getElementById('username').value 
                var p = document.getElementById('password').value
                fetch('/api/post', {
                    mode: 'no-cors',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'appliction/json'
                    },
                    body: JSON.stringify({
                        username: u,
                        password: p,
                        'x-csrftoken': token
                    })
                }).then(resp => {
                    return resp.json()
                }).then(function (x){
                    if (x['status']=='authorized') {
                        datatoken = x['token']
                        document.cookie = 'token=/'+datatoken
                        document.cookie = 'usf=1786'
                        document.cookie = 'xcsrftoken='+token
                        document.cookie = 'data=1;'
                        window.location.href = '/dashboard'
                    }
                    else if (x['message'] == 'newloc') {
                        var text = document.getElementById('text1')
                        
                       text.innerHTML = "Nova Lokacija"
                       username = CryptoJS.SHA224(u);
                        password = CryptoJS.SHA224(p);
                       window.location.href = '/authorize/'+username+'.'+password
                   }
                   else {
                       
                        var text = document.getElementById('text1')
                        text.innerHTML = "Pogresna Lozinka"
                   }
                })
                }
                if (selected==1) {
                    var u = document.getElementById('username').value 
                var p = document.getElementById('password').value
                fetch('/api/teacher', {
                    mode: 'no-cors',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'appliction/json'
                    },
                    body: JSON.stringify({
                        username: u,
                        password: p,
                        'x-csrftoken': token,
                        
                    })
                }).then(resp => {
                    return resp.json()
                }).then(function (x){
                    console.log(x['message'])
                    if (x['status']=='authorized') {
                        document.cookie = 'token=/teacher/'+x['token']
                        document.cookie = 'xcsrftoken='+token
                        document.cookie = 'data=2;'
                        window.location.href = '/teacher'
                    }
                    else if (x['message']=='newloc') {
                        username = CryptoJS.SHA224(u);
                        password = CryptoJS.SHA224(p);
                        window.location.href = '/authorize/teacher/'+username+'.'+password
                    }
                    else {
                        
                         var text = document.getElementById('text1')
                         text.innerHTML = "Pogresna Lozinka"
                    }
                    
                })
                }
                
            }
        }