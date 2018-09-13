$('#form-user-login').submit(function(e){
  e.preventDefault();
  //alert('form submit prevented');
  var u = $('#user_login_username').val();
  var p = $('#user_login_password').val();
  alert(u,p);
  $.post('http://localhost:5000/api/v1/login',{'username':u,'password':p},function(data,status){
    alert(data,status);
  })

})
