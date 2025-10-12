module.exports = {
    root: true,
    env: {
      node: true,
    },
    extends: [
      'plugin:vue/vue3-essential', // Для Vue 3
      'eslint:recommended', // Рекомендуемая конфигурация ESLint
    ],
    parserOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
    },
    rules: {
      // Ваши кастомные правила ESLint
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    },
  };