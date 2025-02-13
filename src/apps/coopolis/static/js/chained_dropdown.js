jQuery(function($){
    $(document).ready(function(){
        let cloneService = document.getElementById("id_service")
        let cloneSubService = document.getElementById("id_sub_service")
    
        if (cloneService && cloneSubService){
            cloneService = cloneService.cloneNode(true);
            cloneSubService = cloneSubService.cloneNode(true);
            subsidyPeriod = document.getElementById("id_subsidy_period");
            dateStart = document.getElementById("id_date_start");
            if (subsidyPeriod) {
                $("#id_subsidy_period").change(function(){
                    const selectedSubsidyPeriodText = $('#id_subsidy_period option[value="' + $(this).val() + '"]').text();
                    update_services_and_sub_services(selectedSubsidyPeriodText, cloneService, "id_service", "get_subsidy_period", true);
                    $("#id_sub_service").empty();
                });
                const selectedSubsidyPeriodText = $('#id_subsidy_period option[value="' + $("#id_subsidy_period").val() + '"]').text();
                update_services_and_sub_services(selectedSubsidyPeriodText, cloneService, "id_service", "get_subsidy_period")
            } else if (dateStart) {
                $("#id_date_start").change(function(){
                    update_services_and_sub_services_by_date($(this).val(), cloneService, "id_service", "get_subsidy_period", true);
                    $("#id_sub_service").empty();
                });
                update_services_and_sub_services_by_date($("#id_date_start").val(), cloneService, "id_service", "get_subsidy_period")
            }
            $("#id_service").change(function(){
                update_sub_services($(this).val(), cloneSubService, "id_sub_service", "get_sub_services", true)
            });
            update_sub_services($("#id_service").val(), cloneSubService, "id_sub_service", "get_sub_services")
        }
    });

    function update_services_and_sub_services_by_date(date_start, clone, id, url, cap=false) {
        $.ajax({
            url:`/chained_dropdowns/${url}/`,
            type:"GET",
            data:{date_start: date_start,},
            success: function(result) {
                const cols = document.getElementById(id);
                cols.innerHTML = clone.innerHTML
                if (cap) $(`#${id}`).val("");
                Array.from(cols.options).forEach(function(option_element) {
                    let existing = false;
                    for (let k in result) {
                        if (option_element.value == k || option_element.value == "") {
                            existing = true
                        }
                    }
                    if (existing == false) {
                        $(`#${id} option[value='${option_element.value}']`).remove();
                    }
                })
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        })
    }

    function update_sub_services(service, clone, id, url, cap=false) {
        $.ajax({
            url:`/chained_dropdowns/${url}/`,
            type:"GET",
            data:{data: service,},
            success: function(result) {
                const cols = document.getElementById(id);
                cols.innerHTML = clone.innerHTML
                if (cap) $(`#${id}`).val("");
                Array.from(cols.options).forEach(function(option_element) {
                    let existing = false;
                    for (let k in result) {
                        if (option_element.value == k || option_element.value == "") {
                            existing = true
                        }
                    }
                    if (existing == false) {
                        $(`#${id} option[value='${option_element.value}']`).remove();
                    }
                })
            },
            error: function(e){
                console.error(JSON.stringify(e));
            },
        })
    }
});
