function prepareMenu(_for){
    make_network_call(api_domain+'/menu',
    null,
    'GET',
    function(data){
      //on success
      $("#menu").empty();
      console.log('success',JSON.stringify(data))
      menu = data
      Object.keys(data).forEach(function(key){addMenuItem(data[key],_for)});
      if(Object.keys(data).length == 0)$("#menu").append("<p>No Menu items. Please add menu items.</p>")
    },
    function(data){
        console.log('failed',data)
    })
}

  $("#order-submit").click(function(){
      submitOrder()
  })

$('#form-menu-item').submit(function(e){
  e.preventDefault();
  $('#server-error').hide();
  var t = $('#menu-item-title').val();
  var d = $('#menu-item-desc').val();
  var a = $('#menu-item-amount').val();
  var i = $('#menu-item-img').val();
  console.log({'title':t,'desc':d,'amount':a,'img':i})
  alert('hello')


    make_network_call(api_domain+'/menu',
    {'title':t,'description':d,'amount':a,'img_url':i},
    'POST',
    function(data){
        //onSuccess
          console.log('success',JSON.stringify(data))
          console.log('menu item saved')
          window.location.reload()
    },
    function(data){
      //on error
      $('#server-error').text(data['error'])
      $('#server-error').show();
      console.log('failed',JSON.stringify(data))
    });
});



function addMenuItem(item,_for){
  //image
  i = "<img class=\"menu-item-img\" src=\""+item.image_url+"\" alt=\"menu Image\">";
  t = "<h4 class=\"heading menu-item-title\"> "+item.title+" </h4>"
  d = "<p> "+item.description+" </p>"
  a = "<p> Price: Ush "+item.amount+" </p>"
  r = "<a id=\"remove-"+item.id+"\" class=\"menu-item-button\" >Remove</a>";
  i_a = "<a class=\"menu-item-button\" id=\"item-btn-add-"+item.id+"\">Add</a>"
  i_r = "<a class=\"menu-item-button\" id=\"item-btn-remove-"+item.id+"\" hidden>Remove</a>"
  if(_for == 'admin'){
    var itemstring = "<div class=\"menu-item\">\n"+i+"\n"+t+"\n"+d+"\n"+a+"\n"+r+"</div>"
    $("#menu").append(itemstring);
    $("#remove-"+item.id).click(function(){remove_menu_item(item.id)})
  }else{
    var itemstring = "<div class=\"menu-item\">\n"+i+"\n"+t+"\n"+d+"\n"+a+"\n"+i_a+"\n"+i_r+"</div>"
    $("#menu").append(itemstring);
    $("#item-btn-add-"+item.id).click(function(){add_to_order(item.id)})
    $("#item-btn-remove-"+item.id).click(function(){remove_from_order(item.id)})
  }}


function remove_menu_item(id)
{
  make_network_call(api_domain+'/menu/'+id,
  null,
  'DELETE',
  function(data){
    console.log('success',JSON.stringify(data))
    window.location.reload();
  },
  function(data){
      console.log('failed',data)
      moveto('admin-login.html')

  })

}
