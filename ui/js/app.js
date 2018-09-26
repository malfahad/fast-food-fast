//localhost
var api_domain = "http://127.0.0.1:5000/api/v1"
//remote
//var api_domain = "https://andelafastfoodfast.herokuapp.com/api/v1"

$('#form-admin-login').submit(function(e){
  e.preventDefault();
  $('#server-error').hide();
  var u = $('#admin_login_username').val();
  var p = $('#admin_login_password').val();

    make_network_call(api_domain+'/admin/login',
    {'username':u,'password':p},
    'POST',
    function(data,status,request){
      console.log('success',data)
      if(status == 'success'){
        if(data['error'] != undefined){
          $('#server-error').text(data['error'])
            $('#server-error').show();
        }else{
          admin_client_id = request.getResponseHeader('admin-client-id');
          //alert(admin_client_id)
          localStorage.setItem("admin-client-id",admin_client_id);
          moveto('admin-menu.html');
        }
      }
    },
    function(xhr){
      console.log('failed',xhr)
    });
});



$('#form-user-login').submit(function(e){
  e.preventDefault();
  $('#server-error').hide();
  var u = $('#user_login_username').val();
  var p = $('#user_login_password').val();


  make_network_call(api_domain+'/login',
  {'username':u,'password':p},
  'POST',
  function(data,status,request){
    console.log('success',data)
    if(status == 'success'){
      if(data['error'] != undefined){
        $('#server-error').text(data['error'])
          $('#server-error').show();
      }else{
        client_id = request.getResponseHeader('client-id');
        //alert(client_id)
        localStorage.setItem("client-id",client_id);
        moveto('orders.html')
      }
    }
  },
  function(xhr){
    console.log('failed',xhr)
  });

});


$('#form-user-signup').submit(function(e){
  e.preventDefault();
  $('#server-error').hide();
  var fn = $('#user_signup_fullname').val();
  var u = $('#user_signup_username').val();
  var p = $('#user_signup_password').val();
  var p2 = $('#user_signup_password2').val();

  if(p != p2){
    $('#server-error').text("passwords do not match")
      $('#server-error').show();
      return;
    }
    console.log({'full name':fn,'username':u,'password':p})

    make_network_call(api_domain+'/register',
    {'full name':fn,'username':u,'password':p},
    'POST',
    function(data,status,request){
      console.log('success',data)
      if(status == 'success'){
        if(data['error'] != undefined){
          $('#server-error').text(data['error'])
            $('#server-error').show();
        }else{
          client_id = request.getResponseHeader('client-id');
          //alert(client_id)
          localStorage.setItem("client-id",client_id);
          moveto('orders.html');
        }
      }
    },
    function(xhr){
      console.log('failed',xhr)
    })
});

$("#admin-logout").click(function(e){
  e.preventDefault()
  logOut('admin')
})

$("#user-logout").click(function(e){
  e.preventDefault()
  logOut('user')
})

function moveto(page){
  a = window.location.toString().split('/')
  a.pop()
  a.push(page)
  window.location =  a.join('/')
}

function getThisPage(){
  a = window.location.toString().split('/')
  return a.pop()
}

function logOut(who){
  if (who == 'user'){
    localStorage.removeItem('client-id')
    make_network_call(api_domain+'/logout',null,'GET',null,null)
    moveto('login.html')
  }
  else{
    localStorage.removeItem('admin-client-id')
    make_network_call(api_domain+'/admin/logout',null,'GET',null,null)
    moveto('admin-login.html')
  }
}
myOrder = []
menu = {}
client_id = localStorage.getItem("client-id")
admin_id  = localStorage.getItem("admin-client-id")

$(document).ready(function(){
  console.log('ready')
  $('#server-error').hide()

  switch(getThisPage()){
    case 'orders.html':
        ensure_auth('login.html')
        prepareMenu('user')
        prepareOrderSummary()
        break;
    case 'admin-menu.html':
        ensure_auth('admin-login.html')
       prepareMenu('admin')
       break;
    case 'orders-history.html':
       ensure_auth('login.html')
       prepareOrderHistory('user')
       break;
    case 'admin-orders.html':
      ensure_auth('admin-login.html')
       prepareOrderHistory('admin')
       break;
  }

});

function ensure_auth(failed_page){
  var x = null;
  if (failed_page =="login.html")
  x = api_domain+'/me'
  else
  x = api_domain+'/admin/me'

  make_network_call(x,null,'GET',
  function(data,status,request){
    console.log('success',data)
    client_id = request.getResponseHeader('client-id')
  //  localStorage.setItem("client-id",client_id);
  },
  function(xhr){
    console.log('failed',xhr)
    moveto(failed_page);
  })
}

function make_network_call(url,data,type,onSuccess,onError){
  //alert(client_id,admin_id)
  $.ajax({
    url:url,
    type:type,
    data:data,
    headers:{
    'admin-client-id':admin_id,
    'client-id':client_id,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': true
  },
  success:onSuccess,
  error:onError
  });
}
