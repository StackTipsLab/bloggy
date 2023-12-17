const path = require('path')
const tailwind = require('tailwindcss')
const postcss = require('postcss')
const typographyPlugin = require('.')

let html = String.raw
let css = String.raw

let defaults = css`
  *,
  ::before,
  ::after {
    --tw-translate-x: 0;
    --tw-translate-y: 0;
    --tw-rotate: 0;
    --tw-skew-x: 0;
    --tw-skew-y: 0;
    --tw-scale-x: 1;
    --tw-scale-y: 1;
    --tw-pan-x: ;
    --tw-pan-y: ;
    --tw-pinch-zoom: ;
    --tw-scroll-snap-strictness: proximity;
    --tw-ordinal: ;
    --tw-slashed-zero: ;
    --tw-numeric-figure: ;
    --tw-numeric-spacing: ;
    --tw-numeric-fraction: ;
    --tw-ring-inset: ;
    --tw-ring-offset-width: 0px;
    --tw-ring-offset-color: #fff;
    --tw-ring-color: rgb(59 130 246 / 0.5);
    --tw-ring-offset-shadow: 0 0 #0000;
    --tw-ring-shadow: 0 0 #0000;
    --tw-shadow: 0 0 #0000;
    --tw-shadow-colored: 0 0 #0000;
    --tw-blur: ;
    --tw-brightness: ;
    --tw-contrast: ;
    --tw-grayscale: ;
    --tw-hue-rotate: ;
    --tw-invert: ;
    --tw-saturate: ;
    --tw-sepia: ;
    --tw-drop-shadow: ;
    --tw-backdrop-blur: ;
    --tw-backdrop-brightness: ;
    --tw-backdrop-contrast: ;
    --tw-backdrop-grayscale: ;
    --tw-backdrop-hue-rotate: ;
    --tw-backdrop-invert: ;
    --tw-backdrop-opacity: ;
    --tw-backdrop-saturate: ;
    --tw-backdrop-sepia: ;
  }
`

function run(config, plugin = tailwind) {
  let { currentTestName } = expect.getState()
  config = {
    ...{ plugins: [typographyPlugin], corePlugins: { preflight: false } },
    ...config,
  }

  return postcss(plugin(config)).process(
    ['@tailwind base;', '@tailwind components;', '@tailwind utilities'].join('\n'),
    {
      from: `${path.resolve(__filename)}?test=${currentTestName}`,
    }
  )
}

test('specificity is reduced with :where', async () => {
  let config = {
    content: [{ raw: html`<div class="format"></div>` }],
    theme: {
      typography: {
        DEFAULT: {
          css: [
            {
              color: 'var(--tw-format-body)',
              maxWidth: '65ch',
              '[class~="lead"]': {
                color: 'var(--tw-format-lead)',
              },
              strong: {
                color: 'var(--tw-format-bold)',
                fontWeight: '600',
              },
              'ol[type="A"]': {
                listStyleType: 'upper-alpha',
              },
              'blockquote p:first-of-type::before': {
                content: 'open-quote',
              },
              'blockquote p:last-of-type::after': {
                content: 'close-quote',
              },
              'h4 strong': {
                fontWeight: '700',
              },
              'figure > *': {
                margin: 0,
              },
              'ol > li::marker': {
                fontWeight: '400',
                color: 'var(--tw-format-counters)',
              },
              '> ul > li p': {
                marginTop: '16px',
                marginBottom: '16px',
              },
              'code::before': {
                content: '"&#96;"',
              },
              'code::after': {
                content: '"&#96;"',
              },
            },
          ],
        },
      },
    },
  }

  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .format {
          color: var(--tw-format-body);
          max-width: 65ch;
        }
        .format :where([class~='lead']):not(:where([class~='not-format'] *)) {
          color: var(--tw-format-lead);
        }
        .format :where(strong):not(:where([class~='not-format'] *)) {
          color: var(--tw-format-bold);
          font-weight: 600;
        }
        .format :where(ol[type='A']):not(:where([class~='not-format'] *)) {
          list-style-type: upper-alpha;
        }
        .format :where(blockquote p:first-of-type):not(:where([class~='not-format'] *))::before {
          content: open-quote;
        }
        .format :where(blockquote p:last-of-type):not(:where([class~='not-format'] *))::after {
          content: close-quote;
        }
        .format :where(h4 strong):not(:where([class~='not-format'] *)) {
          font-weight: 700;
        }
        .format :where(figure > *):not(:where([class~='not-format'] *)) {
          margin: 0;
        }
        .format :where(ol > li):not(:where([class~='not-format'] *))::marker {
          font-weight: 400;
          color: var(--tw-format-counters);
        }
        .format :where(.format > ul > li p):not(:where([class~='not-format'] *)) {
          margin-top: 16px;
          margin-bottom: 16px;
        }
        .format :where(code):not(:where([class~='not-format'] *))::before {
          content: '&#96;';
        }
        .format :where(code):not(:where([class~='not-format'] *))::after {
          content: '&#96;';
        }
      `
    )
  })
})

test('modifiers', async () => {
  let config = {
    content: [{ raw: html`<div class="format format-lg"></div>` }],
    theme: {
      typography: {
        DEFAULT: {
          css: [
            {
              color: 'var(--tw-format-body)',
              maxWidth: '65ch',
              '[class~="lead"]': {
                color: 'var(--tw-format-lead)',
              },
              strong: {
                color: 'var(--tw-format-bold)',
                fontWeight: '600',
              },
              'ol[type="A"]': {
                listStyleType: 'upper-alpha',
              },
              'blockquote p:first-of-type::before': {
                content: 'open-quote',
              },
              'blockquote p:last-of-type::after': {
                content: 'close-quote',
              },
              'h4 strong': {
                fontWeight: '700',
              },
              'figure > *': {
                margin: 0,
              },
              'ol > li::marker': {
                fontWeight: '400',
                color: 'var(--tw-format-counters)',
              },
              'code::before': {
                content: '"&#96;"',
              },
              'code::after': {
                content: '"&#96;"',
              },
            },
          ],
        },
        lg: {
          css: [
            {
              fontSize: '18px',
              lineHeight: '1.75',
              p: {
                marginTop: '24px',
                marginBottom: '24px',
              },
              '[class~="lead"]': {
                fontSize: '22px',
              },
              blockquote: {
                marginTop: '40px',
                marginBottom: '40px',
              },
              h1: {
                fontSize: '48px',
                marginTop: '0',
                marginBottom: '40px',
              },
              h2: {
                fontSize: '30px',
                marginTop: '56px',
                marginBottom: '32px',
              },
              h3: {
                fontSize: '24px',
                marginTop: '40px',
                marginBottom: '16px',
              },
            },
          ],
        },
      },
    },
  }

  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .format {
          color: var(--tw-format-body);
          max-width: 65ch;
        }
        .format :where([class~='lead']):not(:where([class~='not-format'] *)) {
          color: var(--tw-format-lead);
        }
        .format :where(strong):not(:where([class~='not-format'] *)) {
          color: var(--tw-format-bold);
          font-weight: 600;
        }
        .format :where(ol[type='A']):not(:where([class~='not-format'] *)) {
          list-style-type: upper-alpha;
        }
        .format :where(blockquote p:first-of-type):not(:where([class~='not-format'] *))::before {
          content: open-quote;
        }
        .format :where(blockquote p:last-of-type):not(:where([class~='not-format'] *))::after {
          content: close-quote;
        }
        .format :where(h4 strong):not(:where([class~='not-format'] *)) {
          font-weight: 700;
        }
        .format :where(figure > *):not(:where([class~='not-format'] *)) {
          margin: 0;
        }
        .format :where(ol > li):not(:where([class~='not-format'] *))::marker {
          font-weight: 400;
          color: var(--tw-format-counters);
        }
        .format :where(code):not(:where([class~='not-format'] *))::before {
          content: '&#96;';
        }
        .format :where(code):not(:where([class~='not-format'] *))::after {
          content: '&#96;';
        }
        .format-lg {
          font-size: 18px;
          line-height: 1.75;
        }
        .format-lg :where(p):not(:where([class~='not-format'] *)) {
          margin-top: 24px;
          margin-bottom: 24px;
        }
        .format-lg :where([class~='lead']):not(:where([class~='not-format'] *)) {
          font-size: 22px;
        }
        .format-lg :where(blockquote):not(:where([class~='not-format'] *)) {
          margin-top: 40px;
          margin-bottom: 40px;
        }
        .format-lg :where(h1):not(:where([class~='not-format'] *)) {
          font-size: 48px;
          margin-top: 0;
          margin-bottom: 40px;
        }
        .format-lg :where(h2):not(:where([class~='not-format'] *)) {
          font-size: 30px;
          margin-top: 56px;
          margin-bottom: 32px;
        }
        .format-lg :where(h3):not(:where([class~='not-format'] *)) {
          font-size: 24px;
          margin-top: 40px;
          margin-bottom: 16px;
        }
      `
    )
  })
})

test('legacy target', async () => {
  let config = {
    plugins: [typographyPlugin({ target: 'legacy' })],
    content: [{ raw: html`<div class="format format-h1:text-center format-headings:text-ellipsis"></div>` }],
    theme: {
      typography: {
        DEFAULT: {
          css: [
            {
              color: 'var(--tw-format-body)',
              maxWidth: '65ch',
              '[class~="lead"]': {
                color: 'var(--tw-format-lead)',
              },
              strong: {
                color: 'var(--tw-format-bold)',
                fontWeight: '600',
              },
              'ol[type="A"]': {
                listStyleType: 'upper-alpha',
              },
              'blockquote p:first-of-type::before': {
                content: 'open-quote',
              },
              'blockquote p:last-of-type::after': {
                content: 'close-quote',
              },
              'h4 strong': {
                fontWeight: '700',
              },
              'figure > *': {
                margin: 0,
              },
              'ol > li::marker': {
                fontWeight: '400',
                color: 'var(--tw-format-counters)',
              },
              'code::before': {
                content: '"&#96;"',
              },
              'code::after': {
                content: '"&#96;"',
              },
            },
          ],
        },
      },
    },
  }

  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .format {
          color: var(--tw-format-body);
          max-width: 65ch;
        }
        .format [class~='lead'] {
          color: var(--tw-format-lead);
        }
        .format strong {
          color: var(--tw-format-bold);
          font-weight: 600;
        }
        .format ol[type='A'] {
          list-style-type: upper-alpha;
        }
        .format blockquote p:first-of-type::before {
          content: open-quote;
        }
        .format blockquote p:last-of-type::after {
          content: close-quote;
        }
        .format h4 strong {
          font-weight: 700;
        }
        .format figure > * {
          margin: 0;
        }
        .format ol > li::marker {
          font-weight: 400;
          color: var(--tw-format-counters);
        }
        .format code::before {
          content: '&#96;';
        }
        .format code::after {
          content: '&#96;';
        }
        .format-headings\:text-ellipsis h1 {
          text-overflow: ellipsis;
        }
        .format-headings\:text-ellipsis h2 {
          text-overflow: ellipsis;
        }
        .format-headings\:text-ellipsis h3 {
          text-overflow: ellipsis;
        }
        .format-headings\:text-ellipsis h4 {
          text-overflow: ellipsis;
        }
        .format-headings\:text-ellipsis h5 {
          text-overflow: ellipsis;
        }
        .format-headings\:text-ellipsis h6 {
          text-overflow: ellipsis;
        }
        .format-headings\:text-ellipsis th {
          text-overflow: ellipsis;
        }
        .format-h1\:text-center h1 {
          text-align: center;
        }
      `
    )
  })
})

test('custom class name', async () => {
  let config = {
    plugins: [typographyPlugin({ className: 'markdown' })],
    content: [{ raw: html`<div class="markdown"></div>` }],
    theme: {
      typography: {
        DEFAULT: {
          css: [
            {
              color: 'var(--tw-format-body)',
              maxWidth: '65ch',
              '[class~="lead"]': {
                color: 'var(--tw-format-lead)',
              },
              strong: {
                color: 'var(--tw-format-bold)',
                fontWeight: '600',
              },
              'ol[type="A"]': {
                listStyleType: 'upper-alpha',
              },
              'blockquote p:first-of-type::before': {
                content: 'open-quote',
              },
              'blockquote p:last-of-type::after': {
                content: 'close-quote',
              },
              'h4 strong': {
                fontWeight: '700',
              },
              'figure > *': {
                margin: 0,
              },
              'ol > li::marker': {
                fontWeight: '400',
                color: 'var(--tw-format-counters)',
              },
              'code::before': {
                content: '"&#96;"',
              },
              'code::after': {
                content: '"&#96;"',
              },
            },
          ],
        },
      },
    },
  }

  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .markdown {
          color: var(--tw-format-body);
          max-width: 65ch;
        }
        .markdown :where([class~='lead']):not(:where([class~='not-markdown'] *)) {
          color: var(--tw-format-lead);
        }
        .markdown :where(strong):not(:where([class~='not-markdown'] *)) {
          color: var(--tw-format-bold);
          font-weight: 600;
        }
        .markdown :where(ol[type='A']):not(:where([class~='not-markdown'] *)) {
          list-style-type: upper-alpha;
        }
        .markdown
          :where(blockquote p:first-of-type):not(:where([class~='not-markdown'] *))::before {
          content: open-quote;
        }
        .markdown :where(blockquote p:last-of-type):not(:where([class~='not-markdown'] *))::after {
          content: close-quote;
        }
        .markdown :where(h4 strong):not(:where([class~='not-markdown'] *)) {
          font-weight: 700;
        }
        .markdown :where(figure > *):not(:where([class~='not-markdown'] *)) {
          margin: 0;
        }
        .markdown :where(ol > li):not(:where([class~='not-markdown'] *))::marker {
          font-weight: 400;
          color: var(--tw-format-counters);
        }
        .markdown :where(code):not(:where([class~='not-markdown'] *))::before {
          content: '&#96;';
        }
        .markdown :where(code):not(:where([class~='not-markdown'] *))::after {
          content: '&#96;';
        }
      `
    )
  })
})

test('element variants', async () => {
  let config = {
    content: [
      {
        raw: html`<div
          class="
            format
            format-headings:underline
            format-lead:italic
            format-h1:text-3xl
            format-h2:text-2xl
            format-h3:text-xl
            format-h4:text-lg
            format-p:text-gray-700
            format-a:font-bold
            format-blockquote:italic
            format-figure:mx-auto
            format-figcaption:opacity-75
            format-strong:font-medium
            format-em:italic
            format-code:font-mono
            format-pre:font-mono
            format-ol:pl-6
            format-ul:pl-8
            format-li:my-4
            format-table:my-8
            format-thead:border-red-300
            format-tr:border-red-200
            format-th:text-left
            format-td:align-center
            format-img:rounded-lg
            format-video:my-12
            format-hr:border-t-2
        "
        ></div>`,
      },
    ],
    theme: {
      typography: {
        DEFAULT: {
          css: [
            {
              color: 'var(--tw-format-body)',
              '[class~="lead"]': {
                color: 'var(--tw-format-lead)',
              },
              strong: {
                color: 'var(--tw-format-bold)',
                fontWeight: '600',
              },
              'h4 strong': {
                fontWeight: '700',
              },
            },
          ],
        },
      },
    },
  }
  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .format {
          color: var(--tw-format-body);
        }
        .format :where([class~='lead']):not(:where([class~='not-format'] *)) {
          color: var(--tw-format-lead);
        }
        .format :where(strong):not(:where([class~='not-format'] *)) {
          color: var(--tw-format-bold);
          font-weight: 600;
        }
        .format :where(h4 strong):not(:where([class~='not-format'] *)) {
          font-weight: 700;
        }
        .format-headings\:underline
          :is(:where(h1, h2, h3, h4, h5, h6, th):not(:where([class~='not-format'] *))) {
          text-decoration-line: underline;
        }
        .format-h1\:text-3xl :is(:where(h1):not(:where([class~='not-format'] *))) {
          font-size: 1.875rem;
          line-height: 2.25rem;
        }
        .format-h2\:text-2xl :is(:where(h2):not(:where([class~='not-format'] *))) {
          font-size: 1.5rem;
          line-height: 2rem;
        }
        .format-h3\:text-xl :is(:where(h3):not(:where([class~='not-format'] *))) {
          font-size: 1.25rem;
          line-height: 1.75rem;
        }
        .format-h4\:text-lg :is(:where(h4):not(:where([class~='not-format'] *))) {
          font-size: 1.125rem;
          line-height: 1.75rem;
        }
        .format-p\:text-gray-700 :is(:where(p):not(:where([class~='not-format'] *))) {
          --tw-text-opacity: 1;
          color: rgb(55 65 81 / var(--tw-text-opacity));
        }
        .format-a\:font-bold :is(:where(a):not(:where([class~='not-format'] *))) {
          font-weight: 700;
        }
        .format-blockquote\:italic :is(:where(blockquote):not(:where([class~='not-format'] *))) {
          font-style: italic;
        }
        .format-figure\:mx-auto :is(:where(figure):not(:where([class~='not-format'] *))) {
          margin-left: auto;
          margin-right: auto;
        }
        .format-figcaption\:opacity-75 :is(:where(figcaption):not(:where([class~='not-format'] *))) {
          opacity: 0.75;
        }
        .format-strong\:font-medium :is(:where(strong):not(:where([class~='not-format'] *))) {
          font-weight: 500;
        }
        .format-em\:italic :is(:where(em):not(:where([class~='not-format'] *))) {
          font-style: italic;
        }
        .format-code\:font-mono :is(:where(code):not(:where([class~='not-format'] *))) {
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
            'Courier New', monospace;
        }
        .format-pre\:font-mono :is(:where(pre):not(:where([class~='not-format'] *))) {
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
            'Courier New', monospace;
        }
        .format-ol\:pl-6 :is(:where(ol):not(:where([class~='not-format'] *))) {
          padding-left: 1.5rem;
        }
        .format-ul\:pl-8 :is(:where(ul):not(:where([class~='not-format'] *))) {
          padding-left: 2rem;
        }
        .format-li\:my-4 :is(:where(li):not(:where([class~='not-format'] *))) {
          margin-top: 1rem;
          margin-bottom: 1rem;
        }
        .format-table\:my-8 :is(:where(table):not(:where([class~='not-format'] *))) {
          margin-top: 2rem;
          margin-bottom: 2rem;
        }
        .format-thead\:border-red-300 :is(:where(thead):not(:where([class~='not-format'] *))) {
          --tw-border-opacity: 1;
          border-color: rgb(252 165 165 / var(--tw-border-opacity));
        }
        .format-tr\:border-red-200 :is(:where(tr):not(:where([class~='not-format'] *))) {
          --tw-border-opacity: 1;
          border-color: rgb(254 202 202 / var(--tw-border-opacity));
        }
        .format-th\:text-left :is(:where(th):not(:where([class~='not-format'] *))) {
          text-align: left;
        }
        .format-img\:rounded-lg :is(:where(img):not(:where([class~='not-format'] *))) {
          border-radius: 0.5rem;
        }
        .format-video\:my-12 :is(:where(video):not(:where([class~='not-format'] *))) {
          margin-top: 3rem;
          margin-bottom: 3rem;
        }
        .format-hr\:border-t-2 :is(:where(hr):not(:where([class~='not-format'] *))) {
          border-top-width: 2px;
        }
        .format-lead\:italic :is(:where([class~="lead"]):not(:where([class~="not-format"] *))) {
          font-style: italic;
        }
      `
    )
  })
})

test('element variants with custom class name', async () => {
  let config = {
    plugins: [typographyPlugin({ className: 'markdown' })],
    content: [
      {
        raw: html`<div
          class="
            markdown
            markdown-headings:underline
            markdown-lead:italic
            markdown-h1:text-3xl
            markdown-h2:text-2xl
            markdown-h3:text-xl
            markdown-h4:text-lg
            markdown-p:text-gray-700
            markdown-a:font-bold
            markdown-blockquote:italic
            markdown-figure:mx-auto
            markdown-figcaption:opacity-75
            markdown-strong:font-medium
            markdown-em:italic
            markdown-code:font-mono
            markdown-pre:font-mono
            markdown-ol:pl-6
            markdown-ul:pl-8
            markdown-li:my-4
            markdown-table:my-8
            markdown-thead:border-red-300
            markdown-tr:border-red-200
            markdown-th:text-left
            markdown-td:align-center
            markdown-img:rounded-lg
            markdown-video:my-12
            markdown-hr:border-t-2
        "
        ></div>`,
      },
    ],
    theme: {
      typography: {
        DEFAULT: {
          css: [
            {
              color: 'var(--tw-format-body)',
              '[class~="lead"]': {
                color: 'var(--tw-format-lead)',
              },
              strong: {
                color: 'var(--tw-format-bold)',
                fontWeight: '600',
              },
              'h4 strong': {
                fontWeight: '700',
              },
            },
          ],
        },
      },
    },
  }
  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .markdown {
          color: var(--tw-format-body);
        }
        .markdown :where([class~='lead']):not(:where([class~='not-markdown'] *)) {
          color: var(--tw-format-lead);
        }
        .markdown :where(strong):not(:where([class~='not-markdown'] *)) {
          color: var(--tw-format-bold);
          font-weight: 600;
        }
        .markdown :where(h4 strong):not(:where([class~='not-markdown'] *)) {
          font-weight: 700;
        }
        .markdown-headings\:underline
          :is(:where(h1, h2, h3, h4, h5, h6, th):not(:where([class~='not-markdown'] *))) {
          text-decoration-line: underline;
        }
        .markdown-h1\:text-3xl :is(:where(h1):not(:where([class~='not-markdown'] *))) {
          font-size: 1.875rem;
          line-height: 2.25rem;
        }
        .markdown-h2\:text-2xl :is(:where(h2):not(:where([class~='not-markdown'] *))) {
          font-size: 1.5rem;
          line-height: 2rem;
        }
        .markdown-h3\:text-xl :is(:where(h3):not(:where([class~='not-markdown'] *))) {
          font-size: 1.25rem;
          line-height: 1.75rem;
        }
        .markdown-h4\:text-lg :is(:where(h4):not(:where([class~='not-markdown'] *))) {
          font-size: 1.125rem;
          line-height: 1.75rem;
        }
        .markdown-p\:text-gray-700 :is(:where(p):not(:where([class~='not-markdown'] *))) {
          --tw-text-opacity: 1;
          color: rgb(55 65 81 / var(--tw-text-opacity));
        }
        .markdown-a\:font-bold :is(:where(a):not(:where([class~='not-markdown'] *))) {
          font-weight: 700;
        }
        .markdown-blockquote\:italic
          :is(:where(blockquote):not(:where([class~='not-markdown'] *))) {
          font-style: italic;
        }
        .markdown-figure\:mx-auto :is(:where(figure):not(:where([class~='not-markdown'] *))) {
          margin-left: auto;
          margin-right: auto;
        }
        .markdown-figcaption\:opacity-75
          :is(:where(figcaption):not(:where([class~='not-markdown'] *))) {
          opacity: 0.75;
        }
        .markdown-strong\:font-medium :is(:where(strong):not(:where([class~='not-markdown'] *))) {
          font-weight: 500;
        }
        .markdown-em\:italic :is(:where(em):not(:where([class~='not-markdown'] *))) {
          font-style: italic;
        }
        .markdown-code\:font-mono :is(:where(code):not(:where([class~='not-markdown'] *))) {
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
            'Courier New', monospace;
        }
        .markdown-pre\:font-mono :is(:where(pre):not(:where([class~='not-markdown'] *))) {
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono',
            'Courier New', monospace;
        }
        .markdown-ol\:pl-6 :is(:where(ol):not(:where([class~='not-markdown'] *))) {
          padding-left: 1.5rem;
        }
        .markdown-ul\:pl-8 :is(:where(ul):not(:where([class~='not-markdown'] *))) {
          padding-left: 2rem;
        }
        .markdown-li\:my-4 :is(:where(li):not(:where([class~='not-markdown'] *))) {
          margin-top: 1rem;
          margin-bottom: 1rem;
        }
        .markdown-table\:my-8 :is(:where(table):not(:where([class~='not-markdown'] *))) {
          margin-top: 2rem;
          margin-bottom: 2rem;
        }
        .markdown-thead\:border-red-300 :is(:where(thead):not(:where([class~='not-markdown'] *))) {
          --tw-border-opacity: 1;
          border-color: rgb(252 165 165 / var(--tw-border-opacity));
        }
        .markdown-tr\:border-red-200 :is(:where(tr):not(:where([class~='not-markdown'] *))) {
          --tw-border-opacity: 1;
          border-color: rgb(254 202 202 / var(--tw-border-opacity));
        }
        .markdown-th\:text-left :is(:where(th):not(:where([class~='not-markdown'] *))) {
          text-align: left;
        }
        .markdown-img\:rounded-lg :is(:where(img):not(:where([class~='not-markdown'] *))) {
          border-radius: 0.5rem;
        }
        .markdown-video\:my-12 :is(:where(video):not(:where([class~='not-markdown'] *))) {
          margin-top: 3rem;
          margin-bottom: 3rem;
        }
        .markdown-hr\:border-t-2 :is(:where(hr):not(:where([class~='not-markdown'] *))) {
          border-top-width: 2px;
        }
        .markdown-lead\:italic :is(:where([class~="lead"]):not(:where([class~="not-markdown"] *))) {
          font-style: italic;
        }
      `
    )
  })
})

test('customizing defaults with multiple values does not result in invalid css', async () => {
  let config = {
    plugins: [typographyPlugin()],
    content: [
      {
        raw: html`<div class="format"></div>`,
      },
    ],
    theme: {
      typography: {
        DEFAULT: {
          css: {
            textAlign: ['-webkit-match-parent', 'match-parent'],
          },
        },
      },
    },
  }
  return run(config).then((result) => {
    expect(result.css).toMatchFormattedCss(
      css`
        ${defaults}

        .format {
          text-align: -webkit-match-parent;
          text-align: match-parent;
        }
      `
    )
  })
})

it('should be possible to use nested syntax (&) when extending the config', () => {
  let config = {
    plugins: [typographyPlugin()],
    content: [
      {
        raw: html`<div class="format"></div>`,
      },
    ],
    theme: {
      extend: {
        typography: {
          DEFAULT: {
            css: {
              color: '#000',
              a: {
                color: '#888',
                '&:hover': {
                  color: '#ff0000',
                },
              },
            },
          },
        },
      },
    },
  }

  return run(config).then((result) => {
    expect(result.css).toIncludeCss(css`
      .format {
        color: #000;
        max-width: 65ch;
      }
    `)

    expect(result.css).toIncludeCss(css`
      .format :where(a):not(:where([class~='not-format'] *)) {
        color: #888;
        text-decoration: underline;
        font-weight: 500;
      }
    `)

    expect(result.css).toIncludeCss(css`
      .format :where(a):not(:where([class~='not-format'] *)):hover {
        color: #ff0000;
      }
    `)
  })
})

it('should be possible to specify custom h5 and h6 styles', () => {
  let config = {
    plugins: [typographyPlugin()],
    content: [
      {
        raw: html`<div class="format format-h5:text-sm format-h6:text-xl"></div>`,
      },
    ],
  }

  return run(config).then((result) => {
    expect(result.css).toIncludeCss(css`
      .format-h5\:text-sm :is(:where(h5):not(:where([class~='not-format'] *))) {
        font-size: 0.875rem;
        line-height: 1.25rem;
      }
      .format-h6\:text-xl :is(:where(h6):not(:where([class~='not-format'] *))) {
        font-size: 1.25rem;
        line-height: 1.75rem;
      }
    `)
  })
})
