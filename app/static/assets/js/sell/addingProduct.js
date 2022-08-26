const addingProduct = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/sell'
    + '/add_product'
    + '/'
    
);
var product = document.getElementById('id_products');
var selected = product.options[product.selectedIndex].value;
// amount = document.getElementById("amount");
// amount.addEventListener('change', function(){
//     console.log(amount.value);
    
// });

product.addEventListener('change', function(){
    // sending message
    product_id = product.value;
    selling_data_id = document.getElementById('get_obj_id').value;
    addingProduct.send(JSON.stringify({
        'message': {'product_id': product_id, 'selling_data_id': selling_data_id}
    }));

    // receiving message
    addingProduct.onmessage = function(e) {
        const data = JSON.parse(e.data);
        message = data.message
        
        // check product is not added already

        // check message
        if (message == 'pass') {
            // end function
            return
        }

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
            return
        }

        var product_obj = message
        // ################################ start EDITING table
        
        // getting objects
        table = document.getElementById('table');
        tbody = document.getElementById('tbody');
        
        // creating column
        tr = document.createElement('tr');
        tr.setAttribute('id', 'tr-'+product_obj['id'])
        
        // creating row
        // product
        product_td = document.createElement('td');
        product_text = document.createTextNode(product_obj['title']);
        product_td.appendChild(product_text);
        tr.appendChild(product_td);
        
        // amount
        amount_td = document.createElement('td');
        amount_input = document.createElement('input');
        amount_input.setAttribute("style", "width: 200px;");
        amount_input.setAttribute("id", "amount-"+product_obj['id']);
        amount_input.setAttribute("class", "form-control amount");
        amount_input.setAttribute("type", "number");
        amount_input.setAttribute("onchange", "edit(" + product_obj['id'] + ");");
        // amount_input.addEventListener("change", edit(product_obj['id']));
        amount_input.value = product_obj['amount'];
        amount_td.appendChild(amount_input);
        tr.appendChild(amount_td);
        
        // price
        price_td = document.createElement('td');
        price_td.setAttribute('id', 'price-'+product_obj['id'])
        price_text = document.createTextNode(product_obj['price']);
        price_td.appendChild(price_text);
        tr.appendChild(price_td);
        
        // action
        action_td = document.createElement('td');
        action_a = document.createElement('a');
        action_a.setAttribute('id', 'a');
        action_a.setAttribute('role', 'button');
        action_a.setAttribute('class', 'btn btn-danger rounded-pill mt-2');
        action_a.setAttribute('onclick', "del(" + product_obj['id'] + ");");
        
        action_i = document.createElement('i');
        action_i.setAttribute('class', 'fas fa-trash');
        action_i.setAttribute('aria-hidden', 'true');
        action_a.appendChild(action_i);
        action_td.appendChild(action_a);
        tr.appendChild(action_td);
        
        // add tr to body
        tbody.appendChild(tr);
        
        // add listener to remove tr
        // action_a.addEventListener('click', function(){
            
        //     tr = document.getElementById(id);
        //     tr.parentNode.removeChild(tr);
            
        // });

        // add listener when changed input
        // amount_input.addEventListener('change', function(){
        //     console.log('new input: ' + amount_input.value);
        // });
        // ################################ end EDITING table
        
    };

    addingProduct.onclose = function(e) {
        // console.log('Chat socket closed unexpectedly');

    };


    

});