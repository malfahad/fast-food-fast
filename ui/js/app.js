//localhost
var api_domain = "http://127.0.0.1:5000/api/v1"
//remote
//var api_domain = "https://andelafastfoodfast.herokuapp.com/api/v1"


$('#form-admin-login').submit(function(e){
  e.preventDefault();
  $('#server-error').hide();
  var u = $('#admin_login_username').val();
  var p = $('#admin_login_password').val();

    make_network_call(api_domain+'/auth/admin/login',
    {'email':u,'password':p},
    'POST',
    function(data){
          token = data['authorization'];
          //alert(token)
          localStorage.setItem("authorization",token);
          moveto('admin-menu.html');

    },
    function(data){
      $('#server-error').text(data['error'])
      $('#server-error').show();
    });
});



$('#form-user-login').submit(function(e){
  e.preventDefault();
  $('#server-error').hide();
  var u = $('#user_login_username').val();
  var p = $('#user_login_password').val();


  make_network_call(api_domain+'/auth/login',
  {'email':u,'password':p},
  'POST',
  function(data){
        console.log('success',JSON.stringify(data))
        token = data['authorization'];
        //alert(client_id)
        localStorage.setItem("authorization",token);
        moveto('orders.html')
  },
  function(data){
    $('#server-error').text(data['error'])
    $('#server-error').show();
    console.log('failed',JSON.stringify(data))
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
    console.log({'full name':fn,'email':u,'password':p})

    make_network_call(api_domain+'/auth/register',
    {'full name':fn,'email':u,'password':p},
    'POST',
    function(data){
      console.log('success',JSON.stringify(data))
      token = data['authorization'];
      //alert(client_id)
      localStorage.setItem("authorization",token);
      moveto('orders.html');

    },
    function(data){
        $('#server-error').text(data['error'])
        $('#server-error').show();
        console.log('failed',data)
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
    make_network_call(api_domain+'/auth/logout',null,'GET',function(data){
      //on success
      console.log(JSON.stringify(data))
      localStorage.removeItem('authorization')
      moveto('login.html')
      },function(data){
      //on error
      console.log(JSON.stringify(data));
    })
  }
  else{
    make_network_call(api_domain+'/auth/admin/logout',null,'GET',function(data){
      //on success
      console.log(JSON.stringify(data))
      localStorage.removeItem('authorization')
      moveto('admin-login.html')
      },function(data){
      //on error
      console.log(JSON.stringify(data));
    })
  }
}
myOrder = {}
menu = {}
client_id = localStorage.getItem("client-id")
admin_id  = localStorage.getItem("admin-client-id")

$(document).ready(function(){
  console.log('ready')
  $('#server-error').hide()

  switch(getThisPage()){
    case 'orders.html':
        //ensure_auth('login.html')
        prepareMenu('user')
        prepareOrderSummary()
        break;
    case 'admin-menu.html':
       //ensure_auth('admin-login.html')
       prepareMenu('admin')
       break;
    case 'orders-history.html':
       //ensure_auth('login.html')
       prepareOrderHistory('user')
       break;
      case 'admin-orders.html':
       //ensure_auth('admin-login.html')
       prepareOrderHistory('admin')
       break;
  }

});
function make_network_call(url,data,type,onSuccess,onError){

if(type == 'GET'){
  fetchdata = {
    method : type,
    headers: {'content-type':'application/json','Authorization':localStorage.getItem('authorization')}
  }
}else{
   fetchdata = {
    method : type,
    body :JSON.stringify(data),
    headers: {'content-type':'application/json','Authorization':localStorage.getItem('authorization')}
  }
}

  failed = false;

  fetch(url,fetchdata)
  .then(function(response){
    if(response.status >=400)
    failed = true
    return response.json()
  })
  .then(function(data){
    if(failed)
      onError(data)
    else {
      onSuccess(data)
    }
  }).catch(function(error){
    console.log(error);
  })

}
