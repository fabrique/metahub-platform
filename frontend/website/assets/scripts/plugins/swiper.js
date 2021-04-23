
import A11y from 'swiper/src/components/a11y/a11y'
// import Autoplay from 'swiper/src/components/autoplay/autoplay'
// import Controller from 'swiper/src/components/controller/controller'
import Swiper from 'swiper/src/components/core/core-class'
// import EffectCoverflow from 'swiper/src/components/effect-coverflow/effect-coverflow'
// import EffectCube from 'swiper/src/components/effect-cube/effect-cube'
// import EffectFade from 'swiper/src/components/effect-fade/effect-fade'
// import EffectFlip from 'swiper/src/components/effect-flip/effect-flip'
// import HashNavigation from 'swiper/src/components/hash-navigation/hash-navigation'
// import Keyboard from 'swiper/src/components/keyboard/keyboard'
// import Lazy from 'swiper/src/components/lazy/lazy'
// import Mousewheel from 'swiper/src/components/mousewheel/mousewheel'
import Navigation from 'swiper/src/components/navigation/navigation'
import Pagination from 'swiper/src/components/pagination/pagination'
// import Parallax from 'swiper/src/components/parallax/parallax'
// import Scrollbar from 'swiper/src/components/scrollbar/scrollbar'
// import Thumbs from 'swiper/src/components/thumbs/thumbs'
// import Virtual from 'swiper/src/components/virtual/virtual'
// import Zoom from 'swiper/src/components/zoom/zoom'
import Browser from 'swiper/src/modules/browser/browser'
import Device from 'swiper/src/modules/device/device'
import Observer from 'swiper/src/modules/observer/observer'
import Resize from 'swiper/src/modules/resize/resize'
import Support from 'swiper/src/modules/support/support'

export default function loadSwiper () {
  if (typeof Swiper.use === 'undefined') {
    Swiper.use = Swiper.Class.use
    Swiper.installModule = Swiper.Class.installModule
  }

  Swiper.use([
    A11y,
    Navigation,
    Pagination,
    Browser,
    Device,
    Observer,
    Resize,
    Support
  ])

  return Swiper
}
