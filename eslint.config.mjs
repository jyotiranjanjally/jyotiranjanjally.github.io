// ESLint 9 flat config for the static hub; the legacy Astro config is retained.
const rules = {
  'no-undef': 'error',
  'no-unused-vars': ['error', { args: 'after-used', caughtErrors: 'none' }],
  'no-dupe-args': 'error',
  'no-dupe-keys': 'error',
  'no-unreachable': 'error',
  'valid-typeof': 'error',
  'no-constant-condition': 'error',
};
export default [
  { ignores: ['assets/hub/vendor/**', '_site/**', 'node_modules/**'] },
  {
    files: ['assets/hub/*.js'],
    languageOptions: {
      ecmaVersion: 2022, sourceType: 'script',
      globals: Object.fromEntries(['document', 'window', 'location', 'history', 'URLSearchParams',
        'navigator', 'setTimeout', 'requestAnimationFrame', 'IntersectionObserver', 'module'].map(name => [name, 'readonly'])),
    },
    rules,
  },
  {
    files: ['scripts/*.cjs'],
    languageOptions: { ecmaVersion: 2022, sourceType: 'commonjs', globals: { console: 'readonly', __dirname: 'readonly' } },
    rules,
  },
];
