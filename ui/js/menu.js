function prepareMenu(_for){
  console.log(window.location.toString()+' is ready')
  $.get(api_domain+'/menu',function(data,status){
    $("#menu").empty();
    console.log(status);
    console.log(data);
    menu = data
    Object.keys(data).forEach(function(key){addMenuItem(data[key],_for)});

    if(Object.keys(data).length == 0)$("#menu").append("<p>No Menu items. Please add menu items.</p>")

  })

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

  if(t == undefined){
    $('#server-error').text("you must submit a title")
      $('#server-error').show();
      return;
    }

  console.log({'title':t,'desc':d,'amount':a,'img':i})
  $.post(api_domain+'/menu',{'title':t,'desc':d,'amount':a,'img':i},function(data,status){
    if(status == 'success'){
      if(data['error'] != undefined){
        $('#server-error').text(data['error'])
          $('#server-error').show();
      }else{
        console.log('menu item saved')
        window.location.reload()
      }
    }
  });
});

}



function addMenuItem(item,_for){
  //image
  i = "<img class=\"menu-item-img\" src=\""+item.img+"\">";
  t = "<h4 class=\"heading menu-item-title\"> "+item.title+" </h4>"
  d =   "<p> "+item.desc+" </p>"
  a = "<p> Price: Ush "+item.amount+" </p>"
  r =     "<a id=\"remove-"+item.id+"\" class=\"menu-item-button\" >Remove</a>";
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
  $.post(api_domain+'/menu/remove',{'id':id},function(data,status){
    console.log(status)
    console.log(data)
    if(data["success"] != undefined)window.location.reload();
    else{
      alert(data["error"])
    }

  })
}
