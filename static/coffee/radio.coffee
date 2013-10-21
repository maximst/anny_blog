play_pause = () ->
  radio = document.getElementById 'radio'
  find_track radio
  if radio.paused
    radio.play()
  else
    radio.pause()
  false

find_track = (radio) ->
  if radio.src
    if radio.currentTime
      return null
    else
      [current_time, id] = get_from_coocies()
      if current_time
        radio.currentTime = current_time
      return null
  else
    [current_time, id] = get_from_coocies()
    if id
      for track in PLAYLIST
        if track.id == id
          set_track track, radio
          if current_time is undefined
            current_time = 0
          radio.currentTime = current_time
          return null

  track = get_random_track()
  set_track track, radio


get_random_track = () ->
  max = PLAYLIST.length - 1
  num_track = Math.floor(Math.random() * (max - 0 + 1)) + 0
  track = PLAYLIST[num_track]
  return track

set_track = (track, radio) ->
  if radio.canPlayType 'audio/ogg; codecs="vorbis"'
    radio.src = track.ogg
    if radio.duration == NaN
      radio.src = track.mp3
  else
    radio.src = track.mp3

  console.log "NOW PLAYING: \"#{track.full_title}\""


get_from_coocies = () ->
  return [null, null]

next_track = (e) ->
  track = get_random_track()
  set_track track, this
  this.play()


$(document).on 'click', '#play_pause', play_pause

$(document).on 'ended', '#radio', next_track