show_image = () ->
    $('.blog-image').addClass 'show-image'

$ () =>
    css = 
        'opacity': 0,
        'transform': 'scale(0.1)',
        '-moz-transform': 'scale(0.1)',
        '-webkit-transform': 'scale(0.1)',
        '-khtml-transform': 'scale(0.1)',
        '-o-transform': 'scale(0.1)',
        '-ms-transform': 'scale(0.1)'

    $('.blog-image').css css
    setTimeout('$(".blog-image").addClass("show-image");', 20000)
    $('.blog-image').load show_image
