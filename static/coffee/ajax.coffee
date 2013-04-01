vote = () ->
  $.get $(this).attr('href'), (data) =>
    id = $(this).attr('id')
    score_votes = $ "#score_votes#{id}"
    vote_block = $ "#vote_block#{id}"
    score_votes.html data.score

    vote_block.attr 'title', "Likes: #{data['score']}"

    link_list = $(this).attr('href').split('/')
    link_list[link_list.length - 2] = data['user_vote']
    $(this).attr('href', link_list.join('/'))

    $("#success_alert#{id}").show 300, () =>
      setTimeout '$(".success_alert").hide(300)', 5000

hide_div = (event) ->
  if $(event.target).closest('#success_alert').length
    return
  $('.success_alert').hide 300
  event.stopPropagation()

$ () =>
  $(document).click hide_div
  $('.down_vote').click vote
  $('.up_vote').click vote
