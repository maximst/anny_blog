PLAYLIST = [
  {
    aid: 354456564,
    artist: 'Test',
    title: 'Loreт Ipsum',
    ogg: '/media/radio/354456564.ogg',
    mp3: '/media/radio/354456564.mp3'
  },
  {
    aid: 6366467878,
    artist: 'Test',
    title: 'Loreт Ipsum',
    ogg: '/media/radio/6366467878.ogg',
    mp3: '/media/radio/6366467878.mp3'
  },
]

play_pause = () ->
  if player.paused
    player.play()
  else
    player.pause()


$(document).ready () ->
  player = Audio()
  player.id = 'radio'

$(document).on 'click', '#play_pause', play_pause

player.addEventListener 'ended', next_track