import Component from '../../../assets/scripts/modules/component'
import insertScript from '../../../assets/scripts/utilities/insert-script'
import randomHash from '../../../assets/scripts/utilities/random-hash'

function getCookie (name) {
  const parts = `; ${document.cookie}`.split(`; ${name}=`)
  return parts.length < 2 ? undefined : parts.pop().split(';').shift()
}

export default class VideoEmbedComponent extends Component {
  init () {
    this.container = this.element.querySelector('.video-embed__container')
    this.hitTarget = this.element.querySelector('.video-embed__hit-target')
    this.autoplay = this.element.classList.contains('video-embed--autoplay')
    this.picture = this.element.querySelector('picture')

    if (!this.container || !this.hitTarget) {
      // console.log('Video is missing either a container or a hit target')
      return
    }

    this.videoId = this.hitTarget.getAttribute('data-id')
    this.videoType = this.hitTarget.getAttribute('data-type')

    if (!this.videoId || !this.videoType) {
      // console.log('Video is missing either a video id or a video type')
      return
    }

    this.iframeId = `player-${randomHash()}`
    this.player = null

    const cookie = getCookie('cookies-accepted')

    if (!cookie || cookie.split(',').indexOf('embeds') === -1) {
      this.element.classList.add('video-embed--cookies-not-accepted')
      window.addEventListener('cookies-accepted', () => this.initVideo())
    } else {
      this.initVideo()
    }
  }

  initVideo () {
    const cookie = getCookie('cookies-accepted')

    if (!cookie || cookie.split(',').indexOf('embeds') === -1) {
      return
    }

    if (this.element.classList.contains('video-embed--cookies-not-accepted')) {
      return
    }

    this.element.classList.remove('video-embed--cookies-not-accepted')
    this.hitTarget.addEventListener('click', this.onHitTargetClick.bind(this))

    if (this.autoplay) {
      window.setTimeout(() => this.hitTarget.click(), 150) // Arbitrary timeout to make sure the wrapper styling is painted first.
    }
  }

  onHitTargetClick (event) {
    event.preventDefault()

    if (this.videoType === 'vimeo') {
      if (window.video_vimeoLoaded) {
        if (this.player) {
          this.player.playVideo()
        } else {
          this.insertVimeoContainer()
        }
      } else {
        insertScript(
          'vimeo-api-script',
          'https://player.vimeo.com/api/player.js',
          this.insertVimeoContainer.bind(this)
        )
      }
      this.picture.style.opacity = 0
    } else if (this.videoType === 'youtube') {
      if (window.YT) {
        if (this.player) {
          this.player.playVideo()
        } else {
          this.insertYouTubeContainer()
        }
      } else {
        insertScript(
          'youtube-api-script',
          '//youtube.com/iframe_api',
          this.insertYouTubeContainer.bind(this)
        )
      }
      this.picture.style.opacity = 0
    } else {
      throw Error(`Video #${this.videoId}: Video type "${this.videoType}" not supported`)
    }
  }

  /* jshint ignore:start */
  async insertVimeoContainer () {
    if (!window.Vimeo) {
      throw Error('Vimeo API not loaded correctly.')
    }

    this.vimeoOptions = {
      id: this.videoId, // can be either the ID or URL to the video
      autopause: true,
      autoplay: true,
      background: false, // Hide controls and autoplay
      byline: false, // Show byline
      color: 'ffffff',
      // height: 0,
      loop: false,
      // maxheight: 0,
      // maxwidth: 0,
      muted: false,
      playsinline: false, // Set to true to play inline on some mobile devices
      portrait: false, // Show the video portrait
      speed: false, // Show speed controls
      title: false, // Show title
      transparent: true
      // width: 0,
    }

    this.player = await new window.Vimeo.Player(this.container, this.vimeoOptions)
    this.container.removeChild(this.hitTarget)
  }
  /* jshint ignore:end */

  insertYouTubeContainer () {
    const div = document.createElement('div')

    div.id = this.iframeId
    div.className = 'video-embed__iframe'

    this.hitTarget.parentNode.replaceChild(div, this.hitTarget)
    this.hitTarget = null

    const afterLoad = () => {
      this.player = new window.YT.Player(this.iframeId, {
        width: 640,
        height: 360,
        videoId: this.videoId,
        playerVars: { autoplay: 1, hd: 1, showinfo: 0, modestbranding: 1, iv_load_policy: 3, rel: 0, origin: `${window.location.protocol}//${window.location.host}` },
        events: {
          onReady: () => {
            this.player.setPlaybackQuality('hd1080')

            if (this.element.getAttribute('data-autoplay') !== null) {
              this.player.playVideo()
            }
          }
        }
      })

      window.youtubeLoaded = true
    }

    if (!window.youtubeLoaded) {
      window.onYouTubeIframeAPIReady = afterLoad
    } else {
      afterLoad()
    }
  }
}

window.addEventListener('DOMContentLoaded', () => {
  for (const element of document.querySelectorAll('.video-embed')) {
    element.instance = element.instance || new VideoEmbedComponent(element)
  }
})
