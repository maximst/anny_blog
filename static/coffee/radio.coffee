play_pause = () ->
  if $('radio').paused
    $('radio').play()
  else
    $('radio') .pause()

next_track = (e) ->
  player.src = next
  player.play()


$(document).on 'click', '#play_pause', play_pause

$(document).ready () ->
  $('radio').addEventListener 'ended', next_track