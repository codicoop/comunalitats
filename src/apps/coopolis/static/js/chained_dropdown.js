jQuery(function($){
    $(document).ready(function(){
        let cloneService = document.getElementById("id_service")
        let cloneService0 = document.getElementById("id_stages-0-service")
        if (cloneService || cloneService0){
            let id_service
            let id_subsidy_period;
            if (cloneService0) {
                cloneService = cloneService0.cloneNode(true);
                id_service = "id_stages-0-service"
                id_subsidy_period = "id_stages-0-subsidy_period"
            } else if (cloneService) {
                cloneService = cloneService.cloneNode(true);
                id_service = "id_service"
                id_subsidy_period = "id_subsidy_period"
            }
            $(`#${id_subsidy_period}`).change(function(){
                const selectedSubsidyPeriodText = $(`#${id_subsidy_period} option[value="${$(this).val()}"]`).text();
                console.log($(`#${id_subsidy_period}`).val(), "period", id_service)
                update_services_and_sub_services(selectedSubsidyPeriodText, cloneService, id_service, "get_subsidy_period"); 
            });
            update_services_and_sub_services($(`#${id_subsidy_period}`).val(),cloneService, id_service, "get_subsidy_period")
        }
        let cloneSubService = document.getElementById("id_sub_service")
        let cloneSubService0 = document.getElementById("id_stages-0-service")
        if (cloneSubService || cloneSubService0){
            let id_service
            let id_sub_service;
            if (cloneSubService0) {
                cloneSubService = cloneSubService0.cloneNode(true);
                id_service = "id_stages-0-service"
                id_sub_service = "id_stages-0-sub_service"
            } else if (cloneSubService) {
                cloneSubService = cloneSubService.cloneNode(true);
                id_service = "id_service"
                id_sub_service = "id_subsidy_period"
            }
            $(`#${id_service}`).change(function(){
                update_services_and_sub_services($(this).val(), cloneSubService, id_sub_service, "get_sub_services")
            });
            update_services_and_sub_services($(`#${id_service}`).val(), cloneSubService, id_sub_service, "get_sub_services")
        }   
    });

    function update_services_and_sub_services(data, clone, id, url) {
        console.log("id:", id, data, clone, url)
        $.ajax({
            url:`/chained_dropdowns/${url}/`,
            type:"GET",
            data:{data: data,},
            success: function(result) {
                const cols = document.getElementById(id);
                cols.innerHTML = clone.innerHTML
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
        });
    }
});

