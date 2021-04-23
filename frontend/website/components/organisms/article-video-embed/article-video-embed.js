
import Component from '../../../assets/scripts/modules/component'

export default class ArticleVideoEmbedComponent extends Component {
  init () {
    // this.observedIntersectionElements = this.element.querySelectorAll('.article-video-embed__wrapper')
  }
}

window.addEventListener('init-load', () => document.querySelectorAll('.article-video-embed').forEach(element => {
  element.instance = element.instance || new ArticleVideoEmbedComponent(element)
}))
