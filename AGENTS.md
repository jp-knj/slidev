# Writing preferences

- In prose, headings, speaker notes, reference labels, and diagram labels, use the Japanese conjunction `と` instead of slash separators (both `/` and `／`) or the middle dot `・`.
- Apply this preference to future writing and revisions in this project, including chat responses.
- Preserve syntax in code, URLs, file paths, HTML tags, and exact identifiers. Do not replace operators or other syntactically required characters.
- Omit the unnecessary modifier `各` in prose.
- Separate English words, abbreviations, product names, and inline code from adjacent Japanese text with one ASCII space, for example `Astro の API を使う`. Apply this to prose, headings, speaker notes, reference labels, diagram labels, and chat responses. Preserve the contents of code, URLs, paths, and exact identifiers.
- Apply the spacing rule to newly written or revised sentences and labels. Do not reformat unrelated existing prose solely to add spaces.
- Do not use `向け`, `固有`, or the purpose suffix `用` in prose, headings, diagram labels, speaker notes, source documents, or chat responses. Name the recipient, action, or execution stage explicitly instead.
- Allow the compounds `利用`, `採用`, `適用`, `用意`, `用途`, `用語`, `汎用`, `引用`, and `使用`. Flag other expressions containing `用` for review. Preserve code, exact identifiers, URLs, and paths.
- Run `npm run lint:text` to check the deck, image source documents, and Vue display strings. The checker reports file names, lines, and columns and fails on findings, including the existing prohibited terms.

# Slide layout preferences

- Do not add decorative left borders beside agenda entries, headings, or explanatory text. Use spacing and typography to group these items.
- When removing a decorative left border, also remove padding that existed only to separate the text from that border.
- Keep lines that convey meaning in diagrams, such as the nesting guides on slide 19. This preference does not ban functional diagram lines or code block borders.
- Apply this preference to future slide edits. Do not restyle unrelated existing slides unless requested.

# Typography

- Use M PLUS 2 for prose, headings, diagram labels, and reference labels, including cover and section slides. Use the existing MDIO stack for code blocks, inline code, and monospaced position displays.
- Keep upper-left body-page headings at 36px with a 40px line height.
- Use 24px text with a 32px line height for code examples, including handwritten `pre` blocks and position displays. Inline code retains the size appropriate to its surrounding text.
- If examples overlap or overflow, use a page-scoped exception of 22px with a 30px line height, then 20px with a 28px line height only if still needed. Document the reason in CSS. Keep every code example on the page at the same size across columns and click states.
- Preserve code contents, line breaks, highlighting, and click directives when adjusting typography.
