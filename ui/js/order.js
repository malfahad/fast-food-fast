function submitOrder(){
  var a = []
  $("#order-summary").children().each(function(i){
    a.push($(this).text())
    if($("#order-summary").children().length - $(this).index() == 1){
      var t = $("#order-total").text().split(' ')[2];
      console.log({'total':t,'items':a,'status':'CREATED'})
      make_network_call(api_domain+'/orders',
        {'total':t,'items':a,'status':'CREATED'},
        'POST',
        function(data,status,request){
          if(data["error"] != undefined)
          alert(data["error"]);
          else{
            console.log('success',data)
            //moveto('orders-history.html')
            }
        },
        function(xhr){
          console.log(xhr);
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
  $("#item-btn-remove-"+itemId).show()
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
    $("#item-btn-remove-"+itemId).hide()
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
  $('#order-summary').empty()
  $('#order-total').hide()
  $('#order-submit').hide()
  var m = Object.keys(myOrder)
  var total = 0
  for (i =0;i<m.length;i++){
    let itemstring =   "<li>"+myOrder[m[i]]['qty']+"x "+myOrder[m[i]]['title']+"  -  "+myOrder[m[i]]['amount']+"</li>"+"\n"
    total+=myOrder[m[i]]['amount']
  $('#order-summary').append(itemstring)
  }
  if(m.length>0){
    $('#order-total').text('Total Ush '+total)
    $('#order-total').show()
    $('#order-submit').show()
  }
}

function prepareOrderHistory(_for){
  console.log("fetch order history here");
  $("#orders-list").empty();
  make_network_call(api_domain+'/orders',null,'GET',function(data){
    //on success
    console.log(JSON.stringify(data["data"]))
    data = data["data"]
    Object.keys(data).forEach(function(key){addOrderHistoryItem(data[key],_for)});
    if(Object.keys(data).length == 0)$("#orders-list").append("<p>No recent orders.</p>")
    },function(data){
    //on error
    console.log(JSON.stringify(data));
  })

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
    $("#orders-list").append(itemstring);
    $("#select-"+item.order_id).change(function(){
      var x = $('#select-'+item.order_id+' option:selected').text()
      make_network_call(api_domain+'/orders/'+item.order_id,
      {"status":x},
      'PUT',function (data,status,request) {
        if(data['error'] != undefined){
          console.log(data['error']);
          alert(data['error'])
        }else{
          console.log(data);
        }
      },
      function (xhr) {
        console.log(xhr);
      }
    )
    })
  }else{
    //for user
    var itemstring = "<div class=\"menu-item\">\n"+i+t+d+a+n+"</div>\n";
    $("#orders-list").append(itemstring);
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
