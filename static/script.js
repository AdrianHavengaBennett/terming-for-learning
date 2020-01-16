$(document).ready(function() {
    // Materialize js initializations
    
    $(".button-collapse").sideNav();
    $("select").formSelect();
    $('input#input_text, textarea#textarea2').characterCounter();

    $(".dropdown-toggle").dropdown();
});

// // noob voting functionality
// var clicks = 0;
// document.getElementById("clicks").innerHTML = clicks;
// $('.like-counter').click(function() {
// clicks += 1;
// document.getElementById("clicks").innerHTML = clicks;
// $('.like-counter').addClass("liked");
// });
