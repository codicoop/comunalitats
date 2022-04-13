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
                cols = document.getElementById("id_sub_service");
                Array.from(cols.options).forEach(function(option_element) {
                    var existing = false;
                    for (var k in result) {
                        if (option_element.value == result[k]) {
                            existing = true
                        }
                    }
                    if (existing == false) {
                        cols.options.remove(option_element);
                    }
                })
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        });
    }
});

