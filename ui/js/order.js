function submitOrder(){
  var a = []


    Array.from(document.getElementById("order-summary").children).forEach(function(item,index){
    a.push(item.innerHTML)
    console.log(item.innerHTML);
    if(document.getElementById("order-summary").children.length - index == 1){
      var t = document.getElementById("order-total").innerHTML.split(' ')[2];
      console.log({'total':t,'items':a,'status':'CREATED'})
      make_network_call(api_domain+'/orders',
        {'total':t,'items':a,'status':'CREATED'},
        'POST',
        function(data){
          console.log('success',data)
          moveto('orders-history.html')
        },
        function(data){
          alert(data["error"]);
        }
      );

    }
  });
}


function add_to_order(itemId){
  itemId = ''+itemId
  console.log('added item with id '+itemId)
if(Object.keys(myOrder).indexOf(itemId) == -1)
{
  myOrder[itemId] = {
    qty:1,
    title:menu[itemId]["title"],
    amount:1*menu[itemId]["amount"]
  }
  document.getElementById("item-btn-remove-"+itemId).style.display = "block"
  prepareOrderSummary()
}
else{
  let new_count = myOrder[itemId]["qty"]+1
      myOrder[itemId] = {
      qty:new_count,
      title:menu[itemId]["title"],
      amount:new_count*menu[itemId]["amount"]
    }
    prepareOrderSummary()
}
console.log(JSON.stringify(myOrder));
}

function remove_from_order(itemId){
  console.log('removed item with id '+itemId)
  if(myOrder[itemId]['qty'] == 1)
  {
    delete myOrder[itemId]
    document.getElementById("item-btn-remove-"+itemId).style.display = "none"
    prepareOrderSummary()
  }
  else{
    let new_count = myOrder[itemId]["qty"]-1
      myOrder[itemId] = {
        qty:new_count,
        title:menu[itemId]["title"],
        amount:new_count*menu[itemId]["amount"]
      }
      prepareOrderSummary()
  }
}

function prepareOrderSummary(){
  document.getElementById("order-summary").innerHTML = ""
  document.getElementById("order-total").style.display = "none"
  document.getElementById("order-submit").style.display = "none"

  var m = Object.keys(myOrder)
  var total = 0
  for (i =0;i<m.length;i++){
    let itemstring =   "<li>"+myOrder[m[i]]['qty']+"x "+myOrder[m[i]]['title']+"  -  "+myOrder[m[i]]['amount']+"</li>"+"\n"
    total+=myOrder[m[i]]['amount']
    document.getElementById("order-summary").appendChild(makeHTMLObject(itemstring))
  }

  if(m.length>0){
    console.log(''+total);
    document.getElementById("order-total").innerHTML = 'Total Ush '+total
    document.getElementById("order-total").style.display = "block"
    document.getElementById("order-submit").style.display = "block"
  }

}

function prepareOrderHistory(_for){
  console.log("fetch order history here");
  emptyOrders()
  make_network_call(api_domain+'/orders',null,'GET',function(data){
    //on success
    console.log(JSON.stringify(data["data"]))
    data = data["data"]
    Object.keys(data).reverse().forEach(function(key){addOrderHistoryItem(data[key],_for)});
    if(Object.keys(data).length == 0)document.getElementById('orders-list').appendChild(makeHTMLObject("<p>No recent orders.</p>"))
    },
    function(data){
    //on error
    console.log(JSON.stringify(data));
  })

}
function emptyOrders(){
  var orders = document.getElementById('orders-list')
  while(orders.firstChild)orders.removeChild(orders.firstChild)
}

function addOrderHistoryItem(item,_for){
  i = "<img class=\"menu-item-img\" src=\"http://placehold.it/200x200\">\n";
  t = "<h4 class=\"heading menu-item-title\"> Order id #"+item.order_id+" </h4>\n"
  d =   "<ul> "+makeHtml(item.items)+" </ul>\n"
  a = "<p> Total Ush: "+item.total+" </p>\n"
  m1 = "<p> Manage Order Status:<select id=\"select-"+item.order_id+"\">\n"
  m2 =  "<option value=\"Created\""+addSelectedTag('Created',item.status)+"> Created</option>\n"
  m3 =  "<option value=\"Confirmed\""+addSelectedTag('Confirmed',item.status)+">Confirmed</option>\n"
  m4 =  "<option value=\"Rejected\" "+addSelectedTag('Rejected',item.status)+">Rejected</option>\n"
  m5 =  "<option value=\"Completed\" "+addSelectedTag('Completed',item.status)+">Completed</option>\n"
  m6 =  "</select>\n"
  m7 =  "</p>\n"
  console.log(item.status);
  n = "<p>Order Status: <span class=\"order-status "+item.status.toLowerCase()+"\">"+item.status+"</span> </p>\n";
  //  r =     "<a id=\"remove-"+item.id+"\" class=\"menu-item-button\" >Remove</a>";
  //i_a = "<a class=\"menu-item-button\" id=\"item-btn-add-"+item.id+"\">Add</a>"
  //i_r = "<a class=\"menu-item-button\" id=\"item-btn-remove-"+item.id+"\" hidden>Remove</a>"
  if(_for == 'admin'){
    //for admin
    var itemstring = "<div class=\"menu-item\">\n"+i+t+d+a+m1+m2+m3+m4+m5+m6+m7+"</div>"
    document.getElementById('orders-list').appendChild(makeHTMLObject(itemstring));


    document.getElementById("select-"+item.order_id).onchange = function(){
      var x = document.getElementById('select-'+item.order_id)
      x = x.options[x.selectedIndex].value

      make_network_call(api_domain+'/orders/'+item.order_id,
      {"status":x},
      'PUT',function (data) {
        console.log(data);
        alert(data['success'])
      },
      function (data) {
        console.log(data);
        alert(data['error'])
      });

    }

  }else{
    //for user
    var itemstring = "<div class=\"menu-item\">\n"+i+t+d+a+n+"</div>\n";
    document.getElementById("orders-list").appendChild(makeHTMLObject(itemstring));
  }
}

function makeHtml(items){
    var x = ""
    for(var i =0;i<items.length;i++){
      x+="<li> "+items[i]+" </li>\n"
    }
    return x
}

function addSelectedTag(a,b) {
  if( a.toLowerCase() == b.toLowerCase())
  return "selected"
  else {
    return ""
  }
}
