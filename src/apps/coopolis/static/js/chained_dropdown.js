jQuery(function($){
    $(document).ready(function(){
        var clone = document.getElementById("id_sub_service").cloneNode(true);
        $("#id_service").change(function(){
            update_sub_services($(this).val(), clone)
        });
        update_sub_services($("#id_service").val(), clone)
    });

    function update_sub_services(service, clone) {
        $.ajax({
            url:"/chained_dropdowns/get_sub_services/",
            type:"GET",
            data:{service: service,},
            success: function(result) {
                var cols = document.getElementById("id_sub_service");
                cols.innerHTML = clone.innerHTML
                Array.from(cols.options).forEach(function(option_element) {
                    var existing = false;
                    for (var k in result) {
                        if (option_element.value == k || option_element.value == "") {
                            existing = true
                        }
                    }
                    if (existing == false) {
                        $("#id_sub_service option[value='"+option_element.value+"']").remove();
                    }
                })
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        });
    }
});

