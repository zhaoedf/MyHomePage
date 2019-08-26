

$(document).ready(function(){
     $('.header').height($(window).height());

     $(".navbar a").click(function(){

        if("#" + $(this).data('value') == '#undefined')
        {
            $("body,html").animate({
                scrollTop: 0
            })
        }
        else
        {
            $("body,html").animate({
            scrollTop:$("#" + $(this).data('value')).offset().top
        },800)

        }
     })

})

$(window).scroll(function () {

    var index = 0
    var toTop = $(window).scrollTop()
    console.log(toTop)

     console.log($('#about').offset().top)
     console.log($('#portfolio').offset().top)
     console.log($('#blog').offset().top)
     console.log($('#team').offset().top)
     console.log($('#contact').offset().top)
    console.log('1111111111111111111111111111')

    if($(window).scrollTop() < $('#about').offset().top-30 && $(window).scrollTop() >= 0)
    {

        $('.nav-item').css({background: 'rgba(0,0,0,0.1)'})
        $('#navBar').css({background: 'rgba(0,0,0,0.1)', transition: '1.2s'})
        console.log('1')

        return false
    }

    if($(window).scrollTop() >= $('#about').offset().top-30 && $(window).scrollTop() < 1400)
    {
        $('.nav-item').css({background: 'rgb(30,144,255)',opacity: 1})
        $('.nav-item').eq(index).css({background:'#4682B4'})

        return false
    }

    index+=1
    if($(window).scrollTop() >= 1400 && $(window).scrollTop() < 2400)
    {
        $('.nav-item').css({background: 'rgb(30,144,255)',opacity: 1})
        $('.nav-item').eq(index).css({background:'#4682B4'})

        return false
    }


    index+=1
    if($(window).scrollTop() >= 2400 && $(window).scrollTop()-30 < 2950)
    {
        $('.nav-item').css({background: 'rgb(30,144,255)',opacity: 1})
        $('.nav-item').eq(index).css({background:'#4682B4'})

         return false
    }


    index+=1
    if($(window).scrollTop() >= 2950 && $(window).scrollTop() < 3100)
    {
        $('.nav-item').css({background: 'rgb(30,144,255)',opacity: 1})
        $('.nav-item').eq(index).css({background:'#4682B4'})

         return false
    }


    index+=1
    if($(window).scrollTop() >= 3100)
    {
        $('.nav-item').css({background: 'rgb(30,144,255)',opacity: 1})
        $('.nav-item').eq(index).css({background:'#4682B4'})

         return false
    }


})

$('#seemore').click(function () {
    console.log('***************************')
    $("body,html").animate({
            scrollTop:$('#about').offset().top-30
        },800)
})






