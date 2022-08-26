const removingProduct = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/sell'
    + '/delete_product'
    + '/'
    
);

function del(id) {

    tr_obj = document.getElementById('tr-'+id);
    
    // send message
    removingProduct.send(JSON.stringify({
        'message': id,
    }));

    // receive message
    removingProduct.onmessage = function(e) {
        const data = JSON.parse(e.data);
        message = data.message;
        tr_obj.parentNode.removeChild(tr_obj);

    }


}

removingProduct.onclose = function(e) {
    alert('fafaf');
}