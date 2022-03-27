$(".more-btn").on("click", function(){
    $(this).parent().parent().siblings(".info").slideToggle(400).css("display", "flex");
})

$(".show-btn").on("click", function (){
    $(this).text(($(this).text() == "Подробнее") ? "Скрыть" : "Подробнее")
})

setTimeout(function (){
    let messages = $('.messages');
    messages.fadeTo(3000, 0);
}, 5000)