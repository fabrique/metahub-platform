
const configExtends = []
const plugins = []
let rules = {}

// config-standard
configExtends.push('stylelint-config-standard')

rules = {
  ...rules,
  ...{
    'number-leading-zero': 'never',
    'block-closing-brace-newline-after': ['always', { ignoreAtRules: ['if', 'else'] }],
    'at-rule-empty-line-before': ['always', { except: ['first-nested'], ignore: ['after-comment', 'blockless-after-same-name-blockless'], ignoreAtRules: ['else'] }],
    'no-descending-specificity': null,
    'at-rule-no-unknown': null,
    'selector-max-id': 1
  }
}

// copy of stylelint-config-sass-guidelines
// - without the vendor-prefix rules (those take a long time to parse)
// - without all the name regex patterns
rules = {
  ...rules,
  ...{
    'block-no-empty': true,
    'block-opening-brace-space-before': 'always',
    'color-hex-case': 'lower',
    'color-hex-length': 'short',
    'color-named': 'never',
    'color-no-invalid-hex': true,
    'declaration-bang-space-after': 'never',
    'declaration-bang-space-before': 'always',
    'declaration-block-semicolon-newline-after': 'always',
    'declaration-block-semicolon-space-before': 'never',
    'declaration-block-single-line-max-declarations': 1,
    'declaration-block-trailing-semicolon': 'always',
    'declaration-colon-space-after': 'always-single-line',
    'declaration-colon-space-before': 'never',
    'declaration-property-value-blacklist': {
      border: ['none'],
      'border-top': ['none'],
      'border-right': ['none'],
      'border-bottom': ['none'],
      'border-left': ['none']
    },
    'function-comma-space-after': 'always-single-line',
    'function-parentheses-space-inside': 'never',
    'function-url-quotes': 'always',
    indentation: 2,
    'length-zero-no-unit': true,
    'max-nesting-depth': [5, { ignoreAtRules: ['each', 'media', 'supports', 'include'] }],
    'media-feature-parentheses-space-inside': 'never',
    'no-missing-end-of-source-newline': true,
    'number-no-trailing-zeros': true,
    'property-no-unknown': true,
    'rule-empty-line-before': ['always-multi-line', { except: ['first-nested'], ignore: ['after-comment'] }],
    'selector-class-pattern': null,
    'selector-list-comma-newline-after': 'always',
    'selector-max-compound-selectors': 6,
    'selector-max-id': 1,
    'selector-no-qualifying-type': null,
    'selector-pseudo-element-colon-notation': 'double',
    'selector-pseudo-element-no-unknown': true,
    'shorthand-property-no-redundant-values': true,
    'string-quotes': 'single'
  }
}

// stylelint-scss
configExtends.push('stylelint-config-recommended-scss')
plugins.push('stylelint-scss')

rules = {
  ...rules,
  ...{
    'scss/at-extend-no-missing-placeholder': true,
    'scss/at-import-no-partial-leading-underscore': true,
    'scss/at-import-partial-extension-blacklist': ['scss'],
    'scss/at-rule-no-unknown': true,
    'scss/dollar-variable-colon-space-after': 'always',
    'scss/dollar-variable-colon-space-before': 'never',
    'scss/selector-no-redundant-nesting-selector': true,
    'scss/at-each-key-value-single-line': true,
    'scss/at-else-closing-brace-newline-after': 'always-last-in-chain',
    'scss/at-else-if-parentheses-space-before': 'always',
    // 'scss/at-function-named-arguments': ['always', { 'ignore': [ 'single-argument' ]}],
    'scss/at-function-parentheses-space-before': 'never',
    'scss/at-if-no-null': true,
    'scss/at-import-partial-extension': 'never',
    'scss/at-mixin-argumentless-call-parentheses': 'never',
    // 'scss/at-mixin-named-arguments': ['always', { 'ignore': [ 'single-argument' ]}],
    // 'scss/at-mixin-parentheses-space-before': 'always',
    // 'scss/at-rule-conditional-no-parentheses': true,
    // 'scss/dollar-variable-default': [true, { 'ignore': [ 'local' ]}],
    // 'scss/dollar-variable-empty-line-before': [ 'always', { 'except': [ 'first-nested', 'after-comment', 'after-dollar-variable' ], 'ignore': [ 'inside-single-line-block' ]}],
    'scss/dollar-variable-no-missing-interpolation': true,
    'scss/percent-placeholder-pattern': '/^$/', // disable extends completely
    'scss/comment-no-loud': true,
    'scss/declaration-nested-properties': 'never',
    // 'scss/dimension-no-non-numeric-values': true,
    // 'scss/map-keys-quotes': 'always',
    'scss/operator-no-newline-after': true,
    'scss/operator-no-newline-before': true,
    'scss/operator-no-unspaced': true,
    // 'scss/partial-no-import': null,
    // 'scss/selector-nest-combinators': 'always',
    'scss/selector-no-union-class-name': true
  }
}

// stylelint-order
plugins.push('stylelint-order')
rules = {
  ...rules,
  ...{
    'order/order': [['custom-properties', 'dollar-variables', { type: 'at-rule', name: 'extend' }, { type: 'at-rule', name: 'include', hasBlock: false }, 'rules']],
    'order/properties-alphabetical-order': true
  }
}

module.exports = {
  extends: configExtends, plugins, rules
}
