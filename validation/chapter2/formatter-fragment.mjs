import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { parse } from '@astrojs/compiler/sync';
import { transform } from '@astrojs/compiler';
import { serialize } from '@astrojs/compiler/utils';
import * as prettier from 'prettier';
import * as astroPlugin from 'prettier-plugin-astro';
import * as babelPlugin from 'prettier/plugins/babel';

// Reproduce the historical failure described in the empty-fragment report.
// https://github.com/withastro/prettier-plugin-astro/issues/444
const source = '{true ? <p>OK</p> : <></>}\n';
const ast = parse(source, { position: true }).ast;
const expression = ast.children[0];
const fragment = expression.children.find((node) => node.type === 'fragment');
assert.deepEqual(fragment.children, []);
assert.equal(expression.children[0].value, 'true ? ');

const compilation = await transform(source);
assert.equal(typeof compilation.code, 'string');
assert.ok(compilation.code.length > 0);
assert.ok(!compilation.diagnostics?.some((item) => item.severity === 1));

// Match printRaw(): invoke serialize separately with its default options.
// Passing serialize directly to Array.map would pass the index as options.
const regenerated = expression.children.map((node) => serialize(node)).join('');
assert.equal(regenerated, 'true ? <p>OK</p> : < />');
await prettier.format('<>{true ? <p>OK</p> : <></>}</>', {
  parser: 'babel-ts',
  plugins: [babelPlugin],
});
let formatError;
try {
  await prettier.format(source, { parser: 'astro', plugins: [astroPlugin] });
} catch (error) {
  formatError = error.message;
}
assert.match(formatError ?? '', /Unexpected token/);
assert.ok(formatError.includes(regenerated));

const result = {
  source,
  compilerVersion: JSON.parse(readFileSync(new URL('node_modules/@astrojs/compiler/package.json', import.meta.url))).version,
  pluginVersion: JSON.parse(readFileSync(new URL('node_modules/prettier-plugin-astro/package.json', import.meta.url))).version,
  prettierVersion: prettier.version,
  compilerTransformSucceeded: true,
  fragmentRetainedInAst: true,
  originalExpressionAcceptedByBabel: true,
  regenerated,
  formatError,
};
writeFileSync(new URL('formatter-fragment-results.json', import.meta.url), JSON.stringify(result, null, 2) + '\n');
console.log('Verified compiler conversion, fragment preservation, regeneration failure, and formatting error.');
