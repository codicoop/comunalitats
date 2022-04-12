jQuery(function($){
    $(document).ready(function(){
        $("#id_service").change(function(){
            update_sub_services($(this).val())
        });
        update_sub_services($("#id_service").val())
    });

    function update_sub_services(service) {
        $.ajax({
            url:"/chained_dropdowns/get_sub_services/",
            type:"GET",
            data:{service: service,},
            success: function(result) {
                console.log(result);
                cols = document.getElementById("id_sub_service");
                cols.options.length = 0;
                for(var k in result){
                    cols.options.add(new Option(k, result[k]));
                }
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        });
    }
});

