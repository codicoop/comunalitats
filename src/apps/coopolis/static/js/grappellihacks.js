grp.jQuery(function() {
    grp.jQuery('.hasDatepicker').datepicker('option', 'firstDay', 1);

    // Terrible hack to handle inline forms, because when you add a new registry,
    // the rendered timepicker starts in sunday, so executing this with a delay makes the trick.
    grp.jQuery('.grp-add-handler').on("click", function() {
      setTimeout(function() {
        grp.jQuery('.hasDatepicker').datepicker('option', 'firstDay', 1);
      },200);
    });
});