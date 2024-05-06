jQuery(function ($) {
  $(document).ready(function () {
    let cloneService1 = document.getElementById("id_service");
    let cloneService0 = document.getElementById("id_stages-0-service");
    let cloneSubService1 = document.getElementById("id_sub_service");
    let cloneSubService0 = document.getElementById("id_stages-0-sub_service");
    if (cloneService1 || cloneService0) {
      let id_service, id_subsidy_period, cloneService, id_sub_service, cloneSubService;
      if (cloneService0 && cloneSubService0) {
        cloneService = cloneService0.cloneNode(true);
        cloneSubService = cloneSubService0.cloneNode(true);
        id_subsidy_period = "id_stages-0-subsidy_period";
        id_service = "id_stages-0-service";
        id_sub_service = "id_stages-0-sub_service";
      } else if (cloneService1 && cloneSubService1) {
        cloneService = cloneService1.cloneNode(true);
        cloneSubService = cloneSubService1.cloneNode(true);
        id_subsidy_period = "id_subsidy_period";
        id_service = "id_service";
        id_sub_service = "id_sub_service";
      }
      $(`#${id_subsidy_period}`).change(function () {
        const selectedSubsidyPeriodText = $(`#${id_subsidy_period} option[value="${$(this).val()}"]`).text();
        update_services_and_sub_services(selectedSubsidyPeriodText, cloneService, id_service, "get_subsidy_period");
        $(`#${id_sub_service}`).empty();
      });
      $(`#${id_service}`).change(function () {
        update_services_and_sub_services($(this).val(), cloneSubService, id_sub_service, "get_sub_services");
      });
      const selectedSubsidyPeriodText1 = $(
        `#${id_subsidy_period} option[value="${$(`#${id_subsidy_period}`).val()}"]`
      ).text();
      update_services_and_sub_services(selectedSubsidyPeriodText1, cloneService, id_service, "get_subsidy_period");
      update_services_and_sub_services($(`#${id_service}`).val(), cloneSubService, id_sub_service, "get_sub_services");
    }
  });

  function update_services_and_sub_services(data, clone, id, url) {
    $.ajax({
      url: `/chained_dropdowns/${url}/`,
      type: "GET",
      data: { data: data },
      success: function (result) {
        const cols = document.getElementById(id);
        cols.innerHTML = clone.innerHTML;
        $(`#${id}`).val("").prop('selected', true);
        Array.from(cols.options).forEach(function (option_element) {
          let existing = false;
          for (let k in result) {
            if (option_element.value == k || option_element.value == "") {
              existing = true;
            }
          }
          if (existing == false) {
            $(`#${id} option[value='${option_element.value}']`).remove();
          }
        });
      },
      error: function (e) {
        console.error(JSON.stringify(e));
      },
    });
  }
});
