class Radio
  init: ->
    @playList = window.PLAYLIST
    @initRadioPlayer()
    state = @getCookie('radio_pause')

    if state == "0"
      current_time = @getCookie('radio_current_time')

      setTimeout (=>
        now_current_time = @getCookie('radio_current_time')
        diff = (now_current_time * 1.0) - (current_time * 1.0)

        if not diff
          @findTrack()
          @radio.addEventListener 'canplay', =>
            @radio.currentTime = @getCookie('radio_current_time')
            @radio.play()
            @radio.removeEventListener 'canplay', arguments.callee, false
          @radioImg.setAttribute('src', '/static/img/radio_play.png')
      ), 600
    cron()
    document.getElementById('play_pause').addEventListener('click', @playPause)

  initRadioPlayer: ->
    @radio = document.getElementById('radio')
    @radioImg = document.getElementById('radio-img')
    @radio.addEventListener('ended', @nextTrack)

  playPause: =>
    if @radio.paused
      @findTrack()
      @radio.play()
      @setCookie('radio_pause', 0)
      @radioImg.setAttribute('src', '/static/img/radio_play.png')
    else
      @radio.pause()
      @setCookie('radio_pause', 1)
      @setCookie('radio_current_time', @radio.currentTime)
      @radioImg.setAttribute('src', '/static/img/radio.png')
    false

  findTrack: ->
    if @radio.src
      if @radio.currentTime
        return null
      else
        cookies = @getFromCookies()
        if cookies.currentTime
          @radio.currentTime = cookies.currentTime
        return null
    else
      cookies = @getFromCookies()
      if cookies.trackId
        _id = cookies.trackId * 1
        for track in @playList
          if track.id == _id
            @setTrack(track)

            if cookies.currentTime
              try
                @radio.currentTime = cookies.currentTime
              catch error
                @radio.addEventListener 'canplay', =>
                  @radio.currentTime = @getCookie('radio_current_time')
                  @radio.removeEventListener 'canplay', arguments.callee, false
            return null

    #track = @getRandomTrack()
    track = @playList[0]
    @setTrack(track)

  getRandomTrack: ->
    max = @playList.length - 1
    numTrack = Math.floor(Math.random() * (max - 0 + 1)) + 0
    track = @playList[numTrack]
    return track

  setTrack: (track) ->
    if @radio.canPlayType 'audio/ogg; codecs="vorbis"'
      @radio.src = track.ext_ogg
    else
      @radio.src = track.ext_mp3


    @setCookie('radio_track_id', track.id)
    #@setCookie('radio_current_time', @radio.currentTime)
    @radio.dataset.id = track.id
    @initRadioPlayer()
    @radio.onerror = (e) =>
      e.target.onerror = null
      if e.target.canPlayType 'audio/ogg; codecs="vorbis"'
        e.target.src = track.ogg
      else
        e.target.src = track.mp3
      e.target.play()

    console.log "NOW PLAYING: \"#{track.full_title}\""

  getCookie: (name) ->
    parts = document.cookie.split "#{name}="
    if parts.length == 2
      return parts.pop().split(";").shift()

    null

  setCookie: (name, value) ->
    document.cookie = name+"="+value+"; path=/"


  getFromCookies: ->
    data =
      currentTime: null
      trackId: null

    trackId = @getCookie('radio_track_id')
    currentTime = @getCookie('radio_current_time')
    if currentTime
      data.currentTime = currentTime
    if trackId
      data.trackId = trackId

    data

  nextTrack: (e) =>
    #track = @getRandomTrack()
    max = @playList.length - 1
    current_track = @radio.dataset.id * 1
    for track in @playList
      if current_track == track.id
        next_track = _i + 1
    if next_track > max
      next_track = 0
    track = @playList[next_track]
    @setTrack(track)
    @radio.play()

window.radioApp = new Radio
document.addEventListener 'DOMContentLoaded', () ->
  window.radioApp.init()
