
import A11y from 'swiper/esm/components/a11y/a11y'
// import Autoplay from 'swiper/esm/components/autoplay/autoplay'
import Controller from 'swiper/esm/components/controller/controller'
import Swiper from 'swiper/esm/components/core/core-class'
// import EffectCoverflow from 'swiper/esm/components/effect-coverflow/effect-coverflow'
// import EffectCube from 'swiper/esm/components/effect-cube/effect-cube'
// import EffectFade from 'swiper/esm/components/effect-fade/effect-fade'
// import EffectFlip from 'swiper/esm/components/effect-flip/effect-flip'
// import HashNavigation from 'swiper/esm/components/hash-navigation/hash-navigation'
// import Keyboard from 'swiper/esm/components/keyboard/keyboard'
// import Lazy from 'swiper/esm/components/lazy/lazy'
// import Mousewheel from 'swiper/esm/components/mousewheel/mousewheel'
import Navigation from 'swiper/esm/components/navigation/navigation'
import Pagination from 'swiper/esm/components/pagination/pagination'
// import Parallax from 'swiper/esm/components/parallax/parallax'
// import Scrollbar from 'swiper/esm/components/scrollbar/scrollbar'
// import Thumbs from 'swiper/esm/components/thumbs/thumbs'
// import Virtual from 'swiper/esm/components/virtual/virtual'
// import Zoom from 'swiper/esm/components/zoom/zoom'
import Observer from 'swiper/esm/modules/observer/observer'
import Resize from 'swiper/esm/modules/resize/resize'

export default function loadSwiper () {
  if (typeof Swiper.use === 'undefined') {
    Swiper.use = Swiper.Class.use
    Swiper.installModule = Swiper.Class.installModule
  }

  Swiper.use([
    A11y,
    Navigation,
    Pagination,
    Controller,
    Observer,
    Resize
  ])

  return Swiper
}
