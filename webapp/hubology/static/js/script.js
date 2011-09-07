
function get_location() {
    if (Modernizr.geolocation) {
        navigator.geolocation.getCurrentPosition(process_location);
    } else {
        //No native location support
        //Let the user choose?
    }
}


function process_location(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    console.log(position);
    //Save coords? Plot?
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