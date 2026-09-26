"""Regression checks for prose extraction and CLI diagnostics."""

import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).with_name("check-wording.py")
spec = importlib.util.spec_from_file_location("wording", SCRIPT)
wording = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wording)


class WordingTests(unittest.TestCase):
    def check(self, source):
        output = io.StringIO()
        with redirect_stdout(output):
            count = wording.check_text(source, "fixture.md", wording.load_terms(wording.DEFAULT_TERMS), [])
        return count, output.getvalue()

    def test_prohibited_and_unregistered_words(self):
        for text in ["Astro 向け", "固有の変換", "Build 用", "実行用", "専用", "活用", "応用"]:
            with self.subTest(text=text):
                self.assertEqual(self.check(text)[0], 1)

    def test_allowlist_does_not_hide_neighboring_suffix(self):
        self.assertEqual(self.check("利用 採用 適用 用意 用途 用語 汎用 引用 使用 再利用 未使用")[0], 0)
        self.assertEqual(self.check("利用用")[0], 1)
        # Existing prohibitions still win over compound allowances.
        self.assertEqual(self.check("処理と運用")[0], 3)

    def test_display_text_and_notes(self):
        samples = [
            "# Astro 向け", "<!--\n固有の変換\n-->", "<p>Build 用</p>",
            '<img alt="Astro 向け" title="利用" src="./固有.png" />',
            '<a aria-label="固有">利用</a>',
            '<img alt=固有 />',
            '<p v-text="\'Build 用\'" />',
            "{{ $clicks === 0 ? 'Build 用' : '利用' }}",
            "{{ `Build 用 ${count}` }}",
            '<Overview :roles="{ compiler: \'Astro 向け\' }" />',
            '<div :title="`Build 用 ${count}`" />',
            '<script setup>const label = "固有の変換";</script>',
            '<script setup>const label = `Build 用 ${count}`;</script>',
            '[Astro 向け](https://example.com/固有)',
        ]
        for text in samples:
            with self.subTest(text=text):
                self.assertEqual(self.check(text)[0], 1)

    def test_code_urls_and_paths_are_excluded(self):
        source = '''````md
```js
const 固有 = "実行用";
```
向け
````
~~~html
<p>固有</p>
~~~
`向け` と ``固有``
<pre><code>処理と専用</code></pre>
<code>固有</code>
<style>.専用 { color: red }</style>
<p class="専用" id="固有">利用</p>
<p :class="'専用'" :id="'固有'">利用</p>
<script>const 固有 = 1; const data = { '固有': '利用' }; // 処理
/* 向け */</script>
{{ 固有 + count }}
[利用](../固有/専用.md)
[ref]: https://example.com/向け
https://example.com/固有 ../専用.md /tmp/向け.md
固有/専用.md 固有.ts
'''
        self.assertEqual(self.check(source)[0], 0)

    def test_original_line_and_column(self):
        count, output = self.check('`固有`\n<img src="/固有" alt="固有" />\n<!--\nBuild 用\n-->')
        self.assertEqual(count, 2)
        self.assertIn("fixture.md:2:21:", output)
        self.assertIn("fixture.md:4:7:", output)

    def test_stdin_and_existing_symbols(self):
        run = lambda *args: subprocess.run([sys.executable, str(SCRIPT), "--stdin", *args], input="「利用」", capture_output=True, text=True)
        result = run()
        self.assertEqual(result.returncode, 1)
        self.assertIn("<stdin>:1:1: discouraged symbol", result.stdout)
        self.assertEqual(run("--skip-symbols").returncode, 0)

    def test_cli_globs_and_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "ok.md").write_text("利用と採用", encoding="utf-8")
            run = lambda *args: subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
            self.assertEqual(run(str(root / "**/*.md")).returncode, 0)
            bad = root / "bad.md"
            bad.write_text("Build 用", encoding="utf-8")
            result = run(str(root / "**/*.md"))
            self.assertEqual(result.returncode, 1)
            self.assertIn(f"{bad}:1:7:", result.stdout)
            self.assertEqual(run(str(root / "missing.md")).returncode, 2)


if __name__ == "__main__":
    unittest.main()
