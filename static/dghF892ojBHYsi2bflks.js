var url = document.cookie
        var content = url.split(';')
        var data = []
        var token = 'none'
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
                            
                        }
                    }
        fetch('/api/token2', {
            method: 'POST',
            body: JSON.stringify({
                'token': token
            })
        }).then(resp => {
            return resp.json()
        }).then(function(x) {
            if (x['message'] == 'ok') {

            }
            else {
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
                document.cookie = 'xcsrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
                window.location.href = '/login'
            }
        })