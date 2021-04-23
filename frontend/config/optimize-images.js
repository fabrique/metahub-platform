
const jpegoptim = {
  stripComments: true,
  stripEXIF: true,
  stripIPTC: true,
  stripICC: true,
  stripXMP: true,
  forceProgressive: true,
  max: null,
  size: null
}

const pngquant = {
  quality: [30, 50],
  speed: 4,
  disableDithering: false,
  strip: true
}

const svgoPlugins = [
  { addAttributesToSVGElement: false },
  { addClassesToSVGElement: false },
  { cleanupAttrs: true },
  { cleanupEnableBackground: true },
  { cleanupIDs: true },
  { cleanupListOfValues: true },
  { cleanupNumericValues: true },
  { collapseGroups: true },
  { convertColors: { currentColor: true, names2hex: true, rgb2hex: true, shorthex: true, shortname: true } },
  { convertPathData: true },
  { convertShapeToPath: false },
  { convertStyleToAttrs: true },
  { convertTransform: true },
  { mergePaths: false },
  { minifyStyles: true },
  { moveElemensAttrsToGroup: true },
  { moveGroupAttrsToElements: false },
  { removeAttrs: { attrs: '(stroke|fill)' } },
  { removeComments: true },
  { removeDesc: true },
  { removeDimensions: false },
  { removeDoctype: true },
  { removeEditorsNSData: true },
  { removeElementsByAttr: false },
  { removeEmptyAttrs: true },
  { removeEmptyContains: true },
  { removeEmptyText: true },
  { removeHiddenElems: true },
  { removeMetadata: true },
  { removeNonInheritableGroupAttrs: true },
  { removeRasterImages: true },
  { removeScriptElement: false },
  { removeStyleElement: false },
  { removeTitle: true },
  { removeUnknownsAndDefaults: true },
  { removeUnusedNS: true },
  { removeUselessDefs: true },
  { removeUselessStrokeAndFill: false },
  { removeViewBox: false },
  { removeXMLNS: false },
  { removeXMLProcInst: true },
  { sortAttrs: true }
]

const svgo = {
  plugins: svgoPlugins,
  js2svg: { pretty: true }
}

module.exports = {
  minDecrease: 16 * 1024, // 16KB
  maxBuffer: 64 * 1024 * 1024, // 64 MB
  jpegoptim,
  pngquant,
  svgo
}
