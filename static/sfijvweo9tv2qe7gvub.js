sd = []
    function send() {
        (function(){let j = true; var p = []; let f; let d = document.getElementsByClassName('subjects'); let s = d; for (var i = 0; i < d.length; i++) {o = i;if (s[o].checked == j){ p.push(s[i].value);}}var n = document.getElementById('name'); n = n.value; fetch('/api/class', {
            method: 'POST',
            body: JSON.stringify({
                'token': t,
                'name': n,
                'students': sd,
                'subjects': p
            })}).then(resp => {return resp.json()}).then(function (data) {console.log(data)});alert('Razred dodan.')})()
    }

    