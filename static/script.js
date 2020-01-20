$(document).ready(function() {
    // Materialize js initializations
    $(".button-collapse").sideNav();
    $(".tooltipped").tooltip();
    $("select").formSelect();
    $("input#input_text, textarea#textarea2").characterCounter();
});

// Shows the added-to-FR toast
$("#save-term-button").click(function() {
    $("#saved-to-FR-toast").animate({top: "2em"}).delay(950).animate({top: "-6em"});
});

