
export default class Component {
  constructor (element) {
    this.element = element
    this.init()

    // TODO: Add generic intersection observer to all components

    // We return this object to bind the instance.
    return this
  }

  static init () {
    // Override this method
  }
}
