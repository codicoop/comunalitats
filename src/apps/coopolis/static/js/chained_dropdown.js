jQuery(function($){
  $(document).ready(function(){
      let cloneService = document.getElementById("id_service")
      let cloneSubService = document.getElementById("id_sub_service")
      if (cloneService && cloneSubService){
          cloneService = cloneService.cloneNode(true);
          cloneSubService = cloneSubService.cloneNode(true);
          $("#id_subsidy_period").change(function(){
              const selectedSubsidyPeriodText = $('#id_subsidy_period option[value="' + $(this).val() + '"]').text();
              update_services_and_sub_services(selectedSubsidyPeriodText, cloneService, "id_service", "get_subsidy_period", true); 
              $("#id_sub_service").empty();
          });
          $("#id_service").change(function(){
            update_services_and_sub_services($(this).val(), cloneSubService, "id_sub_service", "get_sub_services", true)
          });
          const selectedSubsidyPeriodText = $('#id_subsidy_period option[value="' + $("#id_subsidy_period").val() + '"]').text();
          update_services_and_sub_services(selectedSubsidyPeriodText, cloneService, "id_service", "get_subsidy_period")
          update_services_and_sub_services($("#id_service").val(), cloneSubService, "id_sub_service", "get_sub_services")   
      }
  });

  function update_services_and_sub_services(data, clone, id, url,cap=false) {
      $.ajax({
          url:`/chained_dropdowns/${url}/`,
          type:"GET",
          data:{data: data,},
          success: function(result) {
              const cols = document.getElementById(id);
              cols.innerHTML = clone.innerHTML
              cap && $(`#${id}`).val("");
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