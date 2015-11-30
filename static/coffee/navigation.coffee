NavigationCache = new Array()
$(document).ready () ->
  NavigationCache[window.location.pathname] = $('#container').html()
  history.pushState {page: window.location.pathname, type: 'page'}, document.title, window.location.pathname

delay = (ms, func) -> setTimeout func, ms

set_page = (page) ->
  PAGE = page

  $('.preloader').show()

  $.get page, (data) ->
    delay 30000, -> $('.preloader').hide

    if typeof data != 'object'
      window.location = PAGE

    data = eval data

    $('title').html data.title
    $('meta[property="og:title"]').attr 'content', data.title
    $('meta[name="description"]').attr 'content', data.description
    $('meta[property="og:description"]').attr 'content', data.description
    $('meta[name="keywords"]').attr 'content', data.keywords
    og_image = $('meta[property="og:image"]')
    image = $('link[rel="image_src"]')

    if image
      image.attr 'href', data.image
    if og_image
      og_image.attr 'content', data.image

    $('#container').html data.content
    $('.preloader').hide()

    NavigationCache[page] = data.content
    history.pushState {page: page, type: 'page'}, document.title, page

    yaCounter20829157.hit PAGE, data.title

    FB.XFBML.parse()
    $('.fb-like span').css 'width', '105px'

$(document).ready () ->
  window.onpopstate = (event) ->
    if event.state
      if event.state.type.length > 0
        if NavigationCache[event.state.page].length > 0
          $('#container').html NavigationCache[event.state.page]

  return null

$(document).on 'click', '.ajax-nav', () ->
  url = $(this).attr 'href'
  console.log "Go to: #{url}"
  set_page url
  false
