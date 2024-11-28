$(document).ready(function(){

    // Hide categories on medium screens
    if ($(window).width() < 960) {
        $('#country-form, #category-form').attr('hidden', 'hidden');
    }

    console.log("Document ready");
});