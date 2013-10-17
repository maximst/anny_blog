NavigationCache = new Array()
$(document).ready () ->
  NavigationCache[window.location.pathname] = $('#container').html()
  history.pushState {page: window.location.pathname, type: 'page'}, document.title, window.location.pathname


set_page = (page) ->
  $.get page, (data) ->
    data = eval data
    $('#container').html data.content
    NavigationCache[page] = data.content
    history.pushState {page: page, type: 'page'}, document.title, page


$(document).ready () ->
  console.log 'start'
  window.onpopstate = (event) ->
    if event.state.type.length > 0
      if NavigationCache[event.state.page].length > 0
        $('#container').html NavigationCache[event.state.page]

  return null

$(document).on 'click', 'a', () ->
  url = $(this).attr 'href'
  console.log url
  if url[0] == '/' or 'follow-chic.com' in url
    set_page url
    return false

  true
