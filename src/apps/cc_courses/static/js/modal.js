function makeModal (modalSelector) {
    var modal = $(modalSelector).clone();
    var modalParent = $(modalSelector).parent();
    $(modalSelector).remove();
    var _idModal = modal.attr("id");
    modal.removeAttr("id");

    var divBackground = $("<div></div>");
    divBackground.addClass("modal-background");
    divBackground.attr("id", _idModal);
    divBackground.click(function() {
        divBackground.css("display", "none");
    });

    modal.click(function (event) {
        event.stopPropagation();
    });
    modal.css("display", "block");

    divBackground.append(modal);
    modalParent.append(divBackground);
}

function showModal(modalSelector) {
    $(modalSelector).css("display", "block");
}

function hideModal(modalSelector) {
    $(modalSelector).css("display", "none");
}