play_pause = () ->
  if player.paused
    player.play()
  else
    player.pause()

next_track = (e) ->
  player.src = next
  player.play()



$(document).ready () ->
  player = Audio()
  player.id = 'radio'

$(document).on 'click', '#play_pause', play_pause

player.addEventListener 'ended', next_track