// File paths

const IMAGE_EXTENSIONS = 'apng,gif,ico,jpg,jpeg,png,svg,webp'
const AUDIO_EXTENSIONS = 'aac,alac,mp3,flac,ogg,wav'
const VIDEO_EXTENSIONS = 'av1,avi,mov,mkv,mp4,mpg,mpeg,webm,wmv'
const DOCUMENT_EXTENSIONS = 'doc,docx,md,pdf,rtf,txt,xls,xlsx'
const WEBFONT_EXTENSIONS = 'woff,woff2'
const MEDIA_EXTENSIONS = `${IMAGE_EXTENSIONS},${AUDIO_EXTENSIONS},${VIDEO_EXTENSIONS},${DOCUMENT_EXTENSIONS}`

const source = 'website'
const destination = 'build'
const statics = 'static'
const assets = `${source}/assets`
const components = `${source}/components`
const templates = `${source}/templates`

module.exports.project = {
  sourcePath: source,
  destinationPath: destination,
  staticURI: `/${statics}`
}

module.exports.stylesheets = {
  sourceGlobs: `${assets}/stylesheets/main.scss`,
  watchGlobs: [`${assets}/stylesheets/**/*.scss`, `${components}/**/*.scss`],
  lintGlobs: [`${assets}/stylesheets/**/*.scss`, `${components}/**/*.scss`],
  sourcePath: `${assets}/stylesheets`,
  destinationPath: `${destination}/${statics}/stylesheets`
}

module.exports.icons = {
  sourceGlobs: `${assets}/icons/**/*.svg`,
  watchGlobs: `${assets}/icons/**/*.svg`,
  sourcePath: `${assets}/icons`,
  destinationPath: `${destination}/${statics}/icons`
}

module.exports.images = {
  sourceGlobs: `${assets}/images/**/*.{${IMAGE_EXTENSIONS}}`,
  watchGlobs: `${assets}/images/**/*.{${IMAGE_EXTENSIONS}}`,
  sourcePath: `${assets}/images`,
  destinationPath: `${destination}/${statics}/images`
}

module.exports.media = {
  sourceGlobs: `${assets}/media/**/*.{${MEDIA_EXTENSIONS}}`,
  watchGlobs: `${assets}/media/**/*.{${MEDIA_EXTENSIONS}}`,
  sourcePath: `${assets}/media`,
  destinationPath: `${destination}/${statics}/media`
}

module.exports.fonts = {
  sourceGlobs: `${assets}/fonts/**/*.{${WEBFONT_EXTENSIONS}}`,
  watchGlobs: `${assets}/fonts/**/*.{${WEBFONT_EXTENSIONS}}`,
  sourcePath: `${assets}/fonts`,
  destinationPath: `${destination}/${statics}/fonts`
}

module.exports.scripts = {
  sourceGlobs: `${assets}/scripts/*.js`,
  watchGlobs: [`${assets}/scripts/**/*.js`, `${components}/**/*.js`],
  lintGlobs: [`${assets}/scripts/**/*.js`, `${components}/**/*.js`],
  sourcePath: `${assets}/scripts`,
  destinationPath: `${destination}/${statics}/scripts`,
  relativeDestinationPath: `/${statics}/scripts`
}

module.exports.templates = {
  sourceGlobs: `${templates}/pages/**/*.html`,
  watchGlobs: [templates, `${components}/**/*.html`, `${assets}/icons/**/*.svg`, `${assets}/scripts/base.js`],
  sourcePath: `${templates}/pages`,
  destinationPath: `${destination}`
}

module.exports.vendor = {
  sourceGlobs: [`${assets}/vendor/**/*`, `!${assets}/vendor/readme.md`],
  watchGlobs: `${assets}/vendor/**/*`,
  sourcePath: `${assets}/vendor`,
  destinationPath: `${destination}/${statics}/vendor`
}
