
$(document).ready(function () {

    $('#treadup').click(function (event) {
        /*
        var valueForInput1 = $("#input1").val();
        var valueForInput2 = $("#input2").val();
        var data =
        {
            key1: valueForInput1,
            key2: valueForInput2
        };
        var dataToSend = JSON.stringify(data);
        */
        $.ajax(
                {
                    url: '/tread/right',
                    type: 'GET',
                    //data: dataToSend,
                    success: function () {
                        //var objresponse = JSON.parse();
                        console.log("Excellent");
                    },
                    error: function () {
                        //var objresponse = JSON.parse(jsonResponse);
                        console.log("ERROR");
                    }
                });
        event.preventDefault();
    });
});

