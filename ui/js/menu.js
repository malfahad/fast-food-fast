function prepareMenu(_for){
    make_network_call(api_domain+'/menu',
    null,
    'GET',
    function(data){
      //on success
      //document.getElementById("menu").innnerHTML = ""
      emptyMenu()
      console.log('success',JSON.stringify(data))
      menu = data
      Object.keys(data).forEach(function(key){addMenuItem(data[key],_for)});
      if(Object.keys(data).length == 0)document.getElementById("menu").appendChild("<p>No Menu items. Please add menu items.</p>");

    },
    function(data){
        console.log('failed',data)
    })
}

  if(document.getElementById('order-submit') != null)
  document.getElementById('order-submit').onclick = function(){
    submitOrder()
  }

if(document.getElementById('form-menu-item') != null)
document.getElementById('form-menu-item').onsubmit = function(e){
  e.preventDefault();
  document.getElementById('server-error').style.display = "none"
  var t = document.getElementById('menu-item-title').value;
  var d = document.getElementById('menu-item-desc').value;
  var a = document.getElementById('menu-item-amount').value;
  var i = document.getElementById('menu-item-img').value;

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
      document.getElementById('server-error').innerHTML = data['error']
      document.getElementById('server-error').style.display = "block";
      console.log('failed',JSON.stringify(data))
    });
}



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
    document.getElementById("menu").appendChild(makeHTMLObject(itemstring));
    document.getElementById("remove-"+item.id).onclick = function(){remove_menu_item(item.id)}
  }else{
    var itemstring = "<div class=\"menu-item\">\n"+i+"\n"+t+"\n"+d+"\n"+a+"\n"+i_a+"\n"+i_r+"</div>"
    document.getElementById("menu").appendChild(makeHTMLObject(itemstring));
    document.getElementById("item-btn-add-"+item.id).onclick = function(){add_to_order(item.id)}
    document.getElementById("item-btn-remove-"+item.id).onclick = function(){remove_from_order(item.id)}
  }

}
function emptyMenu()
{
  var menu = document.getElementById('menu')
  while(menu.firstChild)menu.removeChild(menu.firstChild)
}

function makeHTMLObject(htmlString)
{
  var htmlObject = document.createElement('template')
  htmlObject.innerHTML = htmlString
  return htmlObject.content.firstChild;
}

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
