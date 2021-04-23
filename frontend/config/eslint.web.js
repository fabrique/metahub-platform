
const settings = {}

const parser = 'espree'
const parserOptions = {
  ecmaVersion: 2020,
  sourceType: 'module',
  ecmaFeatures: {
    globalReturn: false,
    impliedStrict: true,
    jsx: false
  }
}

const globals = {
  document: 'readonly',
  navigator: 'readonly',
  window: 'readonly',
  WEBPACK_ENV: 'readonly',
  require: true
}

const env = {
  browser: true,
  node: false,
  es6: true
}

const plugins = []

const extendsRulesets = [
  'eslint:recommended'
]

let rules = {
  // Fix for: https://github.com/eslint/eslint/issues/11899
  'require-atomic-updates': 0,

  // configuration lifted from eslint-config-standard
  'accessor-pairs': 'error',
  'array-bracket-spacing': ['error', 'never'],
  'arrow-spacing': ['error', { before: true, after: true }],
  'block-spacing': ['error', 'always'],
  'brace-style': ['error', '1tbs', { allowSingleLine: true }],
  camelcase: ['error', { properties: 'never' }],
  'comma-dangle': ['error', { arrays: 'never', objects: 'never', imports: 'never', exports: 'never', functions: 'never' }],
  'comma-spacing': ['error', { before: false, after: true }],
  'comma-style': ['error', 'last'],
  'computed-property-spacing': ['error', 'never'],
  'constructor-super': 'error',
  curly: ['error', 'multi-line'],
  'dot-location': ['error', 'property'],
  'dot-notation': ['error', { allowKeywords: true }],
  'eol-last': 'error',
  eqeqeq: ['error', 'always', { null: 'ignore' }],
  'func-call-spacing': ['error', 'never'],
  'generator-star-spacing': ['error', { before: true, after: true }],
  'handle-callback-err': ['error', '^(err|error)$'],
  indent: ['error', 2, { SwitchCase: 1, VariableDeclarator: 1, outerIIFEBody: 1, MemberExpression: 1, FunctionDeclaration: { parameters: 1, body: 1 }, FunctionExpression: { parameters: 1, body: 1 }, CallExpression: { arguments: 1 }, ArrayExpression: 1, ObjectExpression: 1, ImportDeclaration: 1, flatTernaryExpressions: false, ignoreComments: false, ignoredNodes: ['TemplateLiteral *'] }],
  'key-spacing': ['error', { beforeColon: false, afterColon: true }],
  'keyword-spacing': ['error', { before: true, after: true }],
  'lines-between-class-members': ['error', 'always', { exceptAfterSingleLine: true }],
  'new-cap': ['error', { newIsCap: true, capIsNew: false, properties: true }],
  'new-parens': 'error',
  'no-array-constructor': 'error',
  'no-async-promise-executor': 'error',
  'no-caller': 'error',
  'no-case-declarations': 'error',
  'no-class-assign': 'error',
  'no-compare-neg-zero': 'error',
  'no-cond-assign': 'error',
  'no-const-assign': 'error',
  'no-constant-condition': ['error', { checkLoops: false }],
  'no-control-regex': 'error',
  'no-debugger': 'error',
  'no-delete-var': 'error',
  'no-dupe-args': 'error',
  'no-dupe-class-members': 'error',
  'no-dupe-keys': 'error',
  'no-duplicate-case': 'error',
  'no-empty-character-class': 'error',
  'no-empty-pattern': 'error',
  'no-eval': 'error',
  'no-ex-assign': 'error',
  'no-extend-native': 'error',
  'no-extra-bind': 'error',
  'no-extra-boolean-cast': 'error',
  'no-extra-parens': ['error', 'functions'],
  'no-fallthrough': 'error',
  'no-floating-decimal': 'error',
  'no-func-assign': 'error',
  'no-global-assign': 'error',
  'no-implied-eval': 'error',
  'no-inner-declarations': ['error', 'functions'],
  'no-invalid-regexp': 'error',
  'no-irregular-whitespace': 'error',
  'no-iterator': 'error',
  'no-labels': ['error', { allowLoop: false, allowSwitch: false }],
  'no-lone-blocks': 'error',
  'no-misleading-character-class': 'error',
  'no-prototype-builtins': 'error',
  'no-useless-catch': 'error',
  'no-mixed-operators': ['error', { groups: [['==', '!=', '===', '!==', '>', '>=', '<', '<='], ['&&', '||'], ['in', 'instanceof']], allowSamePrecedence: true }],
  'no-mixed-spaces-and-tabs': 'error',
  'no-multi-spaces': 'error',
  'no-multi-str': 'error',
  'no-multiple-empty-lines': ['error', { max: 1, maxEOF: 0 }],
  'no-negated-in-lhs': 'error',
  'no-new': 'error',
  'no-new-func': 'error',
  'no-new-object': 'error',
  'no-new-require': 'error',
  'no-new-symbol': 'error',
  'no-new-wrappers': 'error',
  'no-obj-calls': 'error',
  'no-octal': 'error',
  'no-octal-escape': 'error',
  'no-path-concat': 'error',
  'no-proto': 'error',
  'no-redeclare': ['error', { builtinGlobals: false }],
  'no-regex-spaces': 'error',
  'no-return-assign': ['error', 'except-parens'],
  'no-return-await': 'error',
  'no-self-assign': ['error', { props: true }],
  'no-self-compare': 'error',
  'no-sequences': 'error',
  'no-shadow-restricted-names': 'error',
  'no-sparse-arrays': 'error',
  'no-tabs': 'error',
  'no-template-curly-in-string': 'error',
  'no-this-before-super': 'error',
  'no-throw-literal': 'error',
  'no-trailing-spaces': 'error',
  'no-undef': 'error',
  'no-undef-init': 'error',
  'no-unexpected-multiline': 'error',
  'no-unmodified-loop-condition': 'error',
  'no-unneeded-ternary': ['error', { defaultAssignment: false }],
  'no-unreachable': 'error',
  'no-unsafe-finally': 'error',
  'no-unsafe-negation': 'error',
  'no-unused-expressions': ['error', { allowShortCircuit: true, allowTernary: true, allowTaggedTemplates: true }],
  'no-unused-vars': ['error', { vars: 'all', args: 'none', ignoreRestSiblings: true }],
  'no-use-before-define': ['error', { functions: false, classes: false, variables: false }],
  'no-useless-call': 'error',
  'no-useless-computed-key': 'error',
  'no-useless-constructor': 'error',
  'no-useless-escape': 'error',
  'no-useless-rename': 'error',
  'no-useless-return': 'error',
  'no-void': 'error',
  'no-whitespace-before-property': 'error',
  'no-with': 'error',
  'object-curly-newline': ['error', { multiline: true, consistent: true }],
  'object-curly-spacing': ['error', 'always'],
  'object-property-newline': ['error', { allowMultiplePropertiesPerLine: true }],
  'one-var': ['error', { initialized: 'never' }],
  'operator-linebreak': ['error', 'after', { overrides: { '?': 'before', ':': 'before', '|>': 'before' } }],
  'padded-blocks': ['error', { blocks: 'never', switches: 'never', classes: 'never' }],
  'prefer-const': ['error', { destructuring: 'all' }],
  'prefer-promise-reject-errors': 'error',
  'quote-props': ['error', 'as-needed'],
  quotes: ['error', 'single', { avoidEscape: true, allowTemplateLiterals: true }],
  'rest-spread-spacing': ['error', 'never'],
  semi: ['error', 'never'],
  'semi-spacing': ['error', { before: false, after: true }],
  'space-before-blocks': ['error', 'always'],
  'space-before-function-paren': ['error', 'always'],
  'space-in-parens': ['error', 'never'],
  'space-infix-ops': 'error',
  'space-unary-ops': ['error', { words: true, nonwords: false }],
  'spaced-comment': ['error', 'always', { line: { markers: ['*package', '!', '/', ',', '='] }, block: { balanced: true, markers: ['*package', '!', ',', ':', '::', 'flow-include'], exceptions: ['*'] } }],
  'symbol-description': 'error',
  'template-curly-spacing': ['error', 'never'],
  'template-tag-spacing': ['error', 'never'],
  'unicode-bom': ['error', 'never'],
  'use-isnan': 'error',
  'valid-typeof': ['error', { requireStringLiterals: true }],
  'wrap-iife': ['error', 'any', { functionPrototypeMethods: true }],
  'yield-star-spacing': ['error', 'both'],
  yoda: ['error', 'never']
}

// eslint-plugin-smells
plugins.push('smells')
rules = {
  ...rules,
  ...{
    'smells/no-switch': 2,
    'smells/no-complex-switch-case': 2,
    'smells/no-setinterval': 1,
    'smells/no-this-assign': 2,
    'smells/no-complex-string-concat': 2
  // 'smells/no-complex-chaining': 2,
  }
}

// eslint-plugin-promise
plugins.push('promise')
extendsRulesets.push('plugin:promise/recommended')
rules = {
  ...rules,
  ...{
    'promise/param-names': 'error',
    'promise/prefer-await-to-then': 1,
    'promise/prefer-await-to-callbacks': 0
  }
}

// eslint-plugin-simple-import-sort
plugins.push('simple-import-sort')
rules = {
  ...rules,
  ...{
    'sort-imports': 0,
    'simple-import-sort/sort': 1
  }
}

// eslint-plugin-prefer-object-spread
plugins.push('prefer-object-spread')
rules = {
  ...rules,
  ...{
    'prefer-object-spread/prefer-object-spread': 1
  }
}

module.exports = { settings, parser, parserOptions, globals, env, plugins, extends: extendsRulesets, rules }
