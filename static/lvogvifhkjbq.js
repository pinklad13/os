let subs = []
var ds = []
var bs = []
var ts = []
var dt = []
subs = ot
let deletion = 0
function save() {
    fetch('/api/subjects', {
        method: 'POST',
        body: JSON.stringify({
            'subjects': subs
        })
    })
}

function addSub() {
    var subject = document.getElementById('subname').value
    ds[subs.length] = new SubjectItem(subs.length, subject)
    ds[subs.length].button()
    ds[subs.length].show()
    subs.push(subject)
}

class SubjectItem {
    constructor(position, text) {
        this.d = document.createElement('div')
        this.t = document.createElement('strong')
        this.b = document.createElement('img')
        this.db = document.createElement('img')
        this.position = position
        this.text = text
        this.editing = false
        this.values = []
        this.deletion = 0
    }
    show() {
        this.d.style.width = '700px'
        this.d.style.height = '30px'
        this.d.style.background = 'white'
        this.d.style.borderWidth = '1px'
        this.d.style.border = 'solid'
        this.d.style.borderColor = 'white'
        this.d.style.borderBottomColor = 'rgb(19, 19, 19)'
        this.d.style.marginBottom = '10px'
        this.d.className = 'subject'

        this.t.innerText = this.text
        this.t.style.position = 'relative'
        this.t.style.top = '4px'

        this.b.src = '/static/pics/edit.png'
        this.b.style.float = 'right'
        this.b.style.position = 'relative'
        this.b.style.top = '10px'
        // this.b.innerText = 'Uredi'
        this.b.style.width = '15px'
        this.b.style.height = '15px'

        this.db.src = '/static/pics/del.png'
        this.db.style.float = 'right'
        this.db.style.position = 'relative'
        this.db.style.top = '10px'
        // this.db.innerText = 'Obrisi'
        this.db.style.width = '15px'
        this.db.style.height = '15px'
        this.db.style.right = '20px'
        document.body.appendChild(this.d)
        this.d.appendChild(this.t)
        this.d.appendChild(this.b)
        this.d.appendChild(this.db)
        
    }
    button() {
        this.b.onclick = () => {
            if (this.editing == true) {
                subs[this.position] = this.input.value
                this.text = this.input.value
                this.input.remove()
                this.t.style.visibility = 'visible'
                this.t.innerText = this.text
                this.b.src = '/static/pics/edit.png'
                this.editing = false
                console.log(subs)
            }
            else if (this.editing == false) {
                this.b.src = '/static/pics/save.png'
                this.input = document.createElement('input')
                this.t.style.visibility = 'hidden'
                this.input.value = this.text
                this.input.style.width = '200px'
                this.input.style.float = 'left'
                this.input.style.position = 'relative'
                this.input.style.top = '4px'
                this.input.style.fontSize = '16px'
                this.d.appendChild(this.input)
                this.editing = true
            }
        }
        this.db.onclick = () => {
                deletion += 1
                if (deletion==1) {
                    //document.getElementById('subname').style.background = 'gray'
                    this.center = document.createElement('center')
                    document.body.appendChild(this.center)
                    this.confirm = document.createElement('div')
                    this.confirm.style.border = 'solid'
                    this.confirm.style.borderWidth = '1px'
                    this.confirm.style.borderColor = 'black'
                    this.confirm.style.width = '600px'
                    this.confirm.style.height = '150px'
                    this.confirm.style.borderRadius = '10px'
                    this.confirm.style.background = 'white'
                    this.center.appendChild(this.confirm)
                    //document.body.style.background = 'gray'
                    this.innert =  document.createElement('strong')
                    this.innert.innerText = 'Da li sigurno zelite obrisati ovaj predmet?'
                    this.innert.style.position = 'relative'
                    this.innert.style.top = '15px'
                    this.confirm.appendChild(this.innert)
    
                    this.yes = document.createElement('div')
                    this.yes.style.width = '150px'
                    this.yes.style.height = '30px'
                    this.yes.style.background = 'white'
                    this.yes.style.border = 'solid'
                    this.yes.style.borderRadius = '15px'
                    this.yes.style.borderColor = 'black'
                    this.yes.style.borderWidth = '2px'
                    this.yes.style.position = 'relative'
                    this.yes.style.left = '-150px'
                    this.yes.style.top = '60px'
                    this.yes.style.color = 'black'
                    this.yes.onmouseover = () => {
                        this.yes.style.background = 'black'
                        this.yes.style.color = 'white'
                        this.yes.style.cursor = 'pointer'
                    }
                    this.yes.onmouseleave = () => {
                        this.yes.style.background = 'white'
                        this.yes.style.color = 'black'
                        
                    }
                    this.yes.onclick = () => {
                        this.confirm.remove()
                        deletion = 0
                    }
                    this.confirm.appendChild(this.yes)
    
                    this.no = document.createElement('div')
                    this.no.style.width = '150px'
                    this.no.style.height = '30px'
                    this.no.style.background = 'white'
                    this.no.style.border = 'solid'
                    this.no.style.borderRadius = '15px'
                    this.no.style.borderColor = 'red'
                    this.no.style.borderWidth = '2px'
                    this.no.style.position = 'relative'
                    this.no.style.left = '150px'
                    this.no.style.top = '25px'
                    this.no.style.color = 'red'
                    this.no.onmouseover = () => {
                        this.no.style.background = 'red'
                        this.no.style.color = 'white'
                        this.no.style.cursor = 'pointer'
                    }
                    this.no.onmouseleave = () => {
                        this.no.style.background = 'white'
                        this.no.style.color = 'red'
                        
                    }
                    this.no.onclick = () => {
                        console.log(subs)
                        console.log(subs[this.position])
                        console.log(subs.splice(this.position, 1))
                        console.log(this.position)
                        this.d.remove()
                        this.confirm.remove()
                        deletion = 0
                    }
                    this.confirm.appendChild(this.no)
                    this.yestext = document.createElement('strong')
                    this.yestext.style.position = 'relative'
                    this.yestext.style.top = '5px'
                    this.yestext.innerText = 'Odbaci'
                    this.yes.appendChild(this.yestext)
    
                    this.notext = document.createElement('strong')
                    this.notext.style.position = 'relative'
                    this.notext.style.top = '5px'
                    this.notext.innerText = 'Obrisi'
                    this.no.appendChild(this.notext)
                }

        }
        
    }
}

window.onload = function() {
    (function() {
        for (var i = 0; i < ot.length; i++) { 
            pw = new SubjectItem(i, ot[i])
            ds.push(pw)
        }
        for (var t_1 = 0; t_1 < ds.length; t_1++) {
            ds[t_1].button()
            ds[t_1].show()
        }
    })()
    
}
