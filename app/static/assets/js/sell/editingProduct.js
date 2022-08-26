const editingProduct = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/sell'
    + '/edit_product'
    + '/'
    
);



function edit(id) {
    obj = document.getElementById('amount-'+id);
    value = obj.value;
    
    // send message
    editingProduct.send(JSON.stringify({
        'message': {'id': id, 'value': value}
    }));

    // receive message
    editingProduct.onmessage = function(e) {
        const data = JSON.parse(e.data);
        message = data.message;

        if (message == 'not enough') {
            var alert_obj = document.getElementById('alert');
            alert_obj.style.display = "block";
            var alert_div = document.createElement('div');
            var alert_text = document.createTextNode('Недостаточно средств');
            alert_div.appendChild(alert_text);
            alert_obj.appendChild(alert_div);

            setTimeout(function(){
                alert_obj.style.opacity = 0;
            }, 5000);
            setTimeout(function(){
                alert_obj.removeChild(alert_obj.lastChild);
                alert_obj.style.display = "none";
                alert_obj.style.opacity = 1;
            },8000);
            obj.value = obj.defaultValue;
            return 0;
        }

        if (message == 'error') {
            alert('error');
        } else {
            price_obj = document.getElementById("price-"+id);
            price_obj.innerHTML = message;
            obj.defaultValue = obj.value;
        }


    }
    
    editingProduct.onclose = function(e) {
        // console.log('Chat socket closed unexpectedly');
        
    };

}




// amounts = document.getElementsByClassName('amount');
// for (var i = 0; i < amounts.length; i++) {
//     // var amount = document.getElementById(amounts[i].id);

//     amounts[i].addEventListener('click', function() {
//         // console.log(amounts[i].id);
//         const n = i;
//         console.log(n);
//     });
// }
