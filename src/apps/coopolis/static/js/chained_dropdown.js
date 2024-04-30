jQuery(function($){
    $(document).ready(function(){
        var cloneService = document.getElementById("id_service").cloneNode(true);
        $("#id_subsidy_period").change(function(){
           update_services($(this).val(), cloneService); 
        });
        update_services($("#id_service").val(), cloneService)
        var clone = document.getElementById("id_sub_service").cloneNode(true);
        $("#id_service").change(function(){
            update_sub_services($(this).val(), clone)
        });
        update_sub_services($("#id_service").val(), clone)
    });

    function update_services(subsidy_period, clone) {
        $.ajax({
            url:"/chained_dropdowns/get_subsidy_period/",
            type:"GET",
            data:{subsidy_period: subsidy_period,},
            success: function(result) {
                var cols = document.getElementById("id_service");
                cols.innerHTML = clone.innerHTML
                Array.from(cols.options).forEach(function(option_element) {
                    var existing = false;
                    for (var k in result) {
                        if (option_element.value == k || option_element.value == "") {
                            existing = true
                        }
                    }
                    if (existing == false) {
                        $("#id_service option[value='"+option_element.value+"']").remove();
                    }
                })
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        });
    }
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

