module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    "airbnb",
    "airbnb-typescript",
    "airbnb/hooks",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended",
  ],
  ignorePatterns: ["dist", ".eslintrc.cjs"],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: "tsconfig.json",
    tsconfigRootDir: __dirname,
    sourceType: "module",
  },
  plugins: ["react-refresh"],
  rules: {
    "react-refresh/only-export-components": [
      "warn",
      { allowConstantExport: true },
    ],
    "@typescript-eslint/quotes": ["error", "double"],
    "react/react-in-jsx-scope": "off",
    "linebreak-style": "off",
    "arrow-body-style": "off",
    "no-param-reassign": "off",
    "import/prefer-default-export": "off",
    "react/function-component-definition": "off",
    "@typescript-eslint/comma-dangle": "off",
    "@typescript-eslint/no-unused-vars": "warn",
  },
};
