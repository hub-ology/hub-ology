
function get_location(process_location) {
    if (Modernizr.geolocation) {
        navigator.geolocation.getCurrentPosition(process_location);
    } else {
        //No native location support
        //Let the user choose?
    }
}

// Dropdown example for topbar nav
// ===============================

$("body").bind("click", function (e) {
  $('.dropdown-toggle, .menu').parent("li").removeClass("open");
});
$(".dropdown-toggle, .menu").click(function (e) {
  var $li = $(this).parent("li").toggleClass('open');
  return false;
});

$(function() {
    // //Document Ready
    // get_location();
});