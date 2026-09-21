import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { parse, convertToTSX } from '@astrojs/compiler/sync';
import * as astroParser from 'astro-eslint-parser';
import { Linter } from 'eslint';
import * as prettier from 'prettier';
import * as astroPlugin from 'prettier-plugin-astro';
import ts from 'typescript';
import { getLanguageService } from 'vscode-html-languageservice';
import { TextDocument } from 'vscode-languageserver-textdocument';
import { TraceMap, originalPositionFor } from '@jridgewell/trace-mapping';
import { parseHTML } from '@astrojs/language-server/dist/core/parseHTML.js';
import { astro2tsx } from '@astrojs/language-server/dist/core/astro2tsx.js';

const require = createRequire(import.meta.url);
const fixture = (name) => readFileSync(new URL(name, import.meta.url), 'utf8');
const output = {};
const source = fixture('linter.astro');
const expression = parse(source, { position: true }).ast.children[1].children[0];
assert.equal(expression.children[0].value, 'pirce * amount');
assert.deepEqual([expression.position.start.offset, expression.position.end.offset], [47, 80]);
assert.equal(source.length, 91);
assert.equal(source.slice(48, 64), '{pirce * amount}');
assert.equal(source.slice(49, 54), 'pirce');

let virtualTSX;
const captureParser = {
  parseForESLint(code, options) {
    virtualTSX = code;
    return { ast: require('espree').parse(code, options) };
  },
};
const parsed = astroParser.parseForESLint(source, {
  parser: captureParser,
  ecmaVersion: 2022,
  sourceType: 'module',
  eslintScopeManager: true,
});
let binaryExpression;
function visit(node) {
  if (node.type === 'BinaryExpression') binaryExpression = node;
  for (const key of parsed.visitorKeys[node.type] ?? []) {
    const children = Array.isArray(node[key]) ? node[key] : [node[key]];
    for (const child of children) if (child?.type) visit(child);
  }
}
visit(parsed.ast);
assert.deepEqual(
  [binaryExpression?.operator, binaryExpression?.left.name, binaryExpression?.right.name],
  ['*', 'pirce', 'amount'],
);
const fixedExpression = parsed.services.getAstroAst().children[1].children[0];
assert.deepEqual([fixedExpression.position.start.offset, fixedExpression.position.end.offset], [48, 64]);
const moduleScope = parsed.scopeManager.scopes.find((scope) => scope.type === 'module');
assert.deepEqual(moduleScope.variables.map((variable) => variable.name), ['price', 'amount']);
assert.deepEqual(parsed.scopeManager.globalScope.through.map((ref) => ref.identifier.name), ['pirce']);
assert.deepEqual(parsed.scopeManager.globalScope.through[0].identifier.range, [49, 54]);
assert(moduleScope.references.some((ref) => ref.identifier.name === 'amount' && ref.resolved?.name === 'amount'));
const lintDiagnostics = new Linter().verify(source, [{
  files: ['**/*.astro'],
  languageOptions: { parser: astroParser, ecmaVersion: 2022, sourceType: 'module' },
  rules: { 'no-undef': 'error' },
}], { filename: 'example.astro' });
assert.equal(lintDiagnostics.length, 1);
assert.deepEqual(
  ['ruleId', 'message', 'line', 'column', 'endLine', 'endColumn'].map((key) => lintDiagnostics[0][key]),
  ['no-undef', "'pirce' is not defined.", 6, 5, 6, 10],
);
output.linter = {
  source,
  compilerExpression: expression,
  correctedExpressionRange: [fixedExpression.position.start.offset, fixedExpression.position.end.offset],
  binaryExpression: { type: binaryExpression.type, operator: binaryExpression.operator,
    left: binaryExpression.left.name, right: binaryExpression.right.name },
  virtualTSX,
  declarations: moduleScope.variables.map((variable) => variable.name),
  unresolvedRange: parsed.scopeManager.globalScope.through[0].identifier.range,
  diagnostics: lintDiagnostics,
};

const babelInputs = [];
const capturingPlugin = {
  ...astroPlugin,
  parsers: {
    ...astroPlugin.parsers,
    astroExpressionParser: {
      ...astroPlugin.parsers.astroExpressionParser,
      preprocess(text, options) {
        const wrapped = astroPlugin.parsers.astroExpressionParser.preprocess(text, options);
        babelInputs.push(wrapped);
        return wrapped;
      },
    },
  },
};
const formattingOptions = {
  parser: 'astro', plugins: [capturingPlugin], printWidth: 80, tabWidth: 2, endOfLine: 'lf',
};
const formatted = await prettier.format(fixture('formatter.astro'), formattingOptions);
const expected = '<ul>\n  {\n    products.map((product) => (\n      <li>\n        {product.name}:{product.price}\n      </li>\n    ))\n  }\n</ul>\n';
assert.equal(formatted, expected);
assert(babelInputs.includes('<>{products.map(product=><li>\n{product.name}:{product.price}</li>)\n}</>'));
const doc = await prettier.__debug.printToDoc(fixture('formatter.astro'), formattingOptions);
assert.equal((await prettier.__debug.printDocToString(doc, formattingOptions)).formatted, expected);
output.formatter = { input: fixture('formatter.astro'), babelInputs: [...new Set(babelInputs)], formatted };

const languageSource = fixture('language.astro');
const sourceDoc = TextDocument.create('file:///example.astro', 'astro', 0, languageSource);
const frontmatterEnd = languageSource.indexOf('---', 3) + 3;
const html = parseHTML(ts.ScriptSnapshot.fromString(languageSource), frontmatterEnd).virtualCode;
const htmlText = html.snapshot.getText(0, html.snapshot.getLength());
assert.equal(htmlText.length, languageSource.length);
assert.equal(htmlText.slice(0, frontmatterEnd), ' '.repeat(frontmatterEnd));
assert.equal(htmlText.indexOf('nmae'), 95);
const htmlDoc = TextDocument.create('file:///example.html', 'html', 0, htmlText);
assert.notEqual(htmlDoc.positionAt(95).line, sourceDoc.positionAt(95).line);
const cursorOffset = languageSource.indexOf('href');
const htmlService = getLanguageService();
const completions = htmlService.doComplete(htmlDoc, htmlDoc.positionAt(cursorOffset), htmlService.parseHTMLDocument(htmlDoc));
for (const name of ['target', 'title']) assert(completions.items.some((item) => item.label === name));
output.html = {
  virtualHTML: htmlText,
  sourcePosition: sourceDoc.positionAt(cursorOffset),
  virtualPosition: htmlDoc.positionAt(cursorOffset),
  cursorOffset,
  verifiedCompletions: ['target', 'title'],
  mappings: html.mappings,
};

const converted = convertToTSX(languageSource, { filename: 'example.astro' });
const virtualCode = astro2tsx(languageSource, 'example.astro').virtualCode;
const tsx = virtualCode.snapshot.getText(0, virtualCode.snapshot.getLength());
assert.equal(languageSource.indexOf('nmae'), 95);
assert.equal(converted.code.indexOf('nmae'), 129);
assert.equal(tsx.indexOf('nmae'), 129);
const fileName = fileURLToPath(new URL('example.astro.tsx', import.meta.url));
const tsOptions = { target: ts.ScriptTarget.ESNext, jsx: ts.JsxEmit.Preserve, strict: true, noEmit: true, types: [], skipLibCheck: true };
const host = ts.createCompilerHost(tsOptions);
const originalGetSourceFile = host.getSourceFile.bind(host);
host.getSourceFile = (name, languageVersion, onError, shouldCreateNewSourceFile) =>
  name === fileName ? ts.createSourceFile(name, tsx, languageVersion, true, ts.ScriptKind.TSX)
    : originalGetSourceFile(name, languageVersion, onError, shouldCreateNewSourceFile);
const program = ts.createProgram([
  fileName,
  require.resolve('@astrojs/language-server/types/env.d.ts'),
  require.resolve('@astrojs/language-server/types/jsx-runtime-fallback.d.ts'),
], tsOptions, host);
const allDiagnostics = program.getSemanticDiagnostics();
assert.equal(allDiagnostics.length, 1, 'Expected only the property-name diagnostic');
const diagnostic = allDiagnostics.find((item) => item.code === 2339 && item.start === 129);
assert(diagnostic, 'Expected TS2339 on nmae');
assert.equal(diagnostic.length, 4);
assert.match(ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'), /Property 'nmae' does not exist/);
const generatedDoc = TextDocument.create('', 'typescriptreact', 0, tsx);
const sourceMap = new TraceMap(converted.map);
for (let offset = 129; offset <= 133; offset++) {
  const pos = generatedDoc.positionAt(offset);
  const original = originalPositionFor(sourceMap, { line: pos.line + 1, column: pos.character });
  assert.equal(sourceDoc.offsetAt({ line: original.line - 1, character: original.column }), offset - 34);
  const mapping = virtualCode.mappings.find((item) =>
    item.generatedOffsets[0] <= offset && offset < item.generatedOffsets[0] + item.lengths[0]);
  assert(mapping, `Expected Volar mapping for ${offset}`);
  assert.equal(mapping.sourceOffsets[0] + offset - mapping.generatedOffsets[0], offset - 34);
}
const range = { start: sourceDoc.positionAt(95), end: sourceDoc.positionAt(99) };
assert.deepEqual(range, { start: { line: 7, character: 11 }, end: { line: 7, character: 15 } });
output.language = {
  source: languageSource,
  virtualTSX: tsx.split('//# sourceMappingURL=')[0],
  diagnostic: { code: diagnostic.code, start: diagnostic.start, length: diagnostic.length,
    message: ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n') },
  sourceRange: [95, 99], generatedRange: [129, 133], editorRange: range,
  otherDiagnosticCodes: [...new Set(allDiagnostics.filter((item) => item !== diagnostic).map((item) => item.code))],
};

// Keep the displayed full inputs and the actual formatting output synchronized.
const deck = readFileSync(new URL('../../slides-compiler-rs.md', import.meta.url), 'utf8');
const chapter = deck.slice(deck.indexOf('## 三つのEditor toolは別の問いに答える'), deck.indexOf('# 3. 前提の変化'));
for (const input of [source, fixture('formatter.astro'), languageSource, formatted]) {
  assert(chapter.includes('```astro\n' + input + '```'), 'Slide code differs from validated fixture');
}
writeFileSync(new URL('results.json', import.meta.url), JSON.stringify(output, null, 2) + '\n');
console.log('PASS: Compiler ranges, Linter scope and no-undef, Babel input, Doc output, HTML completion, TS2339, Source map, Volar mapping, slide fixtures');
