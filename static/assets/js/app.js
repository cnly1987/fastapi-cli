var adapter = new LocalStorage('airwaybill')
var db = low(adapter)

var objectifyForm =function(formArray) {
    var returnArray = {};
    for (var i = 0; i < formArray.length; i++) {
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}
var intVal = function ( i ) {
    return typeof i === 'string' ?
        i.replace(/[\$,]/g, '')*1 :
        typeof i === 'number' ?
            i : 0;
};

db.defaults({ 
    username:'',
    user:{},
    token:'',
    permissions:[],
    isLogin:false,
    isLoading:false,
    awb:[],
 }).write()

var app = {
    data:{
        awb:[]
    },
    mounted:function(){

    },
    methods:{
        loading:{
            set:function(){
                var loading= document.createElement('div')
                loading.className = 'loading'
                document.body.appendChild(loading)
            },
            remove:function(){
                var el = document.querySelector('.loading')
                el.remove()
            }
        },
        awb:function(){
            var awb = document.querySelector('#awb').value;
            if(awb !=''){
                var a = document.createElement('a')
                var awbs = db.get('awb').value()
                awbs.push(awb)
                db.set('awb', awbs).write()
                a.href = '/cargo?awb='+awb
                a.target = '_blank'
                a.click()
            }else{
                M.toast({html: '主单号不能为空!'})
            } 
        },
        iata:{
            search:function(){
                var iata = document.querySelector('#iata').value;
                if(iata !=''){
                    app.methods.loading.set()
                    axios.get('/api/airline/airports/?q='+iata).then(function(res){
                        var sdata = res.data
                        if(sdata.length === 1){
                            var a = document.createElement('a')
                            a.href='/iata/detail/'+sdata[0].iata+'.html'
                            a.target = '_blank'
                            setTimeout(function(){
                                a.click()
                                app.methods.loading.remove()
                            },1000) 
                        }else{ 
                            var tb =''
                            _.each(sdata, function(item){
                                tb += `<li><a  target="_balnk" href="/iata/detail/${item.iata}.html">${item.iata}---${item.name}</a></li>`
                            }) 
                            setTimeout(function(){
                                $("#warning").empty().append('<p class="text-danger">查询结果包含多个数据，请在下方列表选择:</p>')
                                $("#mlist").empty().append(tb)
                                app.methods.loading.remove()
                            },1000)
                             
                        }
                    }).catch(function(e){
                        app.methods.loading.remove()
                    })
                }else{
                    M.toast({html: '三字码不能为空!'})
                } 
            }
        },
     
         
    },
    init:function(){
        $('.sidenav').sidenav();
        $('.dropdown-trigger').dropdown();
        $('select').formSelect();
    }
}

app.init()