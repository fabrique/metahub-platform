
const computedStyle = getComputedStyle(document.documentElement)

const MOBILE = parseInt(computedStyle.getPropertyValue('--breakpoint-mobile'), 10)
const PORTRAIT = parseInt(computedStyle.getPropertyValue('--breakpoint-portrait'), 10)
const LANDSCAPE = parseInt(computedStyle.getPropertyValue('--breakpoint-landscape'), 10)
const NOTEBOOK = parseInt(computedStyle.getPropertyValue('--breakpoint-notebook'), 10)
const DESKTOP = parseInt(computedStyle.getPropertyValue('--breakpoint-desktop'), 10)
const DESKTOP_LARGE = parseInt(computedStyle.getPropertyValue('--breakpoint-desktop-large'), 10)

const isMobile = () => window.matchMedia(`screen and (max-width: ${PORTRAIT - 1}px))`).matches

const isPortrait = () => window.matchMedia(`screen and (min-width: ${PORTRAIT}px)`).matches
const isLandscape = () => window.matchMedia(`screen and (min-width: ${LANDSCAPE}px)`).matches
const isNotebook = () => window.matchMedia(`screen and (min-width: ${NOTEBOOK}px)`).matches
const isDesktop = () => window.matchMedia(`screen and (min-width: ${DESKTOP}px)`).matches
const isDesktopLarge = () => window.matchMedia(`screen and (min-width: ${DESKTOP_LARGE}px)`).matches

const isMobileOnly = () => window.matchMedia(`screen and (min-width: ${MOBILE}px) and (max-width: ${PORTRAIT - 1})`).matches
const isPortraitOnly = () => window.matchMedia(`screen and (min-width: ${PORTRAIT}px) and (max-width: ${LANDSCAPE - 1})`).matches
const isLandscapeOnly = () => window.matchMedia(`screen and (min-width: ${LANDSCAPE}px) and (max-width: ${NOTEBOOK - 1})`).matches
const isNotebookOnly = () => window.matchMedia(`screen and (min-width: ${NOTEBOOK}px) and (max-width: ${DESKTOP - 1})`).matches
const isDesktopOnly = () => window.matchMedia(`screen and (min-width: ${DESKTOP}px) and (max-width: ${DESKTOP_LARGE - 1})`).matches

export default {
  MOBILE,
  PORTRAIT,
  LANDSCAPE,
  NOTEBOOK,
  DESKTOP,
  DESKTOP_LARGE,

  isMobile,
  isPortrait,
  isLandscape,
  isNotebook,
  isDesktop,
  isDesktopLarge,
  isMobileOnly,
  isPortraitOnly,
  isLandscapeOnly,
  isNotebookOnly,
  isDesktopOnly
}
