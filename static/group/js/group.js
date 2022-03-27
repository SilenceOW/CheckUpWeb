$(document).ready(function () {
    $('.non-creator').hover(function () {
        $(this).find(".kick-btn").fadeTo(1, 1);
    }, function () {
        $(this).find(".kick-btn").fadeTo(1, 0);
    })
})

setTimeout(function (){
    let messages = $('.messages');
    messages.fadeTo(3000, 0);
}, 5000)


