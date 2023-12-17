const colors = require('tailwindcss/colors')

const round = (num) =>
  num
    .toFixed(7)
    .replace(/(\.[0-9]+?)0+$/, '$1')
    .replace(/\.0$/, '')
const rem = (px) => `${round(px / 16)}rem`
const em = (px, base) => `${round(px / base)}em`

let defaultModifiers = {
  sm: {
    css: [
      {
        fontSize: rem(16),
        lineHeight: round(24 / 14),
        p: {
          marginTop: em(16, 16),
          marginBottom: em(16, 16),
        },
        '[class~="lead"]': {
          fontSize: em(18, 16),
          lineHeight: round(28 / 18),
          marginTop: em(16, 18),
          marginBottom: em(16, 18),
        },
        blockquote: {
          marginBottom: em(24, 18)
        },
        'blockquote::before': {
          marginTop: em(24, 18),
        },
        h1: {
          fontSize: em(30, 18),
          marginTop: '0',
          marginBottom: em(24, 30),
          lineHeight: round(36 / 30),
        },
        h2: {
          fontSize: em(24, 16),
          marginTop: '0',
          marginBottom: em(16, 20),
          lineHeight: round(28 / 20),
        },
        h3: {
          fontSize: em(20, 16),
          marginTop: '0',
          marginBottom: em(8, 18),
          lineHeight: round(28 / 18),
        },
        h4: {
          fontSize: em(18, 16),
          marginTop: '0',
          marginBottom: em(8, 16),
          lineHeight: round(20 / 16),
        },
        img: {
          marginTop: em(24, 16),
          marginBottom: em(24, 16),
        },
        video: {
          marginTop: em(24, 16),
          marginBottom: em(24, 16),
        },
        figure: {
          marginTop: em(24, 16),
          marginBottom: em(24, 16),
        },
        'figure > *': {
          marginTop: '0',
          marginBottom: '0',
        },
        figcaption: {
          fontSize: em(14, 16),
          lineHeight: round(16 / 12),
          marginTop: em(8, 12),
          textAlign: 'center'
        },
        code: {
          fontSize: em(14, 16),
        },
        'h2 code': {
          fontSize: em(18, 20),
        },
        'h3 code': {
          fontSize: em(16, 18),
        },
        pre: {
          fontSize: em(14, 16),
          lineHeight: round(20 / 12),
          marginTop: em(20, 12),
          marginBottom: em(20, 12),
          borderRadius: rem(4),
          paddingTop: em(8, 12),
          paddingRight: em(12, 12),
          paddingBottom: em(8, 12),
          paddingLeft: em(12, 12),
        },
        ol: {
          marginTop: em(16, 16),
          marginBottom: em(16, 16),
          paddingLeft: em(22, 16),
        },
        ul: {
          marginTop: em(16, 16),
          marginBottom: em(16, 16),
          paddingLeft: em(22, 16),
        },
        li: {
          marginTop: em(4, 16),
          marginBottom: em(4, 16),
        },
        'ol > li': {
          paddingLeft: em(6, 16),
        },
        'ul > li': {
          paddingLeft: em(6, 16),
        },
        '> ul > li p': {
          marginTop: em(8, 16),
          marginBottom: em(8, 16),
        },
        '> ul > li > *:first-child': {
          marginTop: em(16, 16),
        },
        '> ul > li > *:last-child': {
          marginBottom: em(16, 16),
        },
        '> ol > li > *:first-child': {
          marginTop: em(16, 16),
        },
        '> ol > li > *:last-child': {
          marginBottom: em(16, 16),
        },
        'ul ul, ul ol, ol ul, ol ol': {
          marginTop: em(8, 16),
          marginBottom: em(8, 16),
        },
        hr: {
          marginTop: em(40, 16),
          marginBottom: em(40, 16),
        },
        'hr + *': {
          marginTop: '0',
        },
        'h2 + *': {
          marginTop: '0',
        },
        'h3 + *': {
          marginTop: '0',
        },
        'h4 + *': {
          marginTop: '0',
        },
        table: {
          fontSize: em(14, 16),
          lineHeight: round(18 / 12),
        },
        'thead th': {
          paddingRight: em(12, 12),
          paddingBottom: em(8, 12),
          paddingLeft: em(12, 12),
        },
        'thead th:first-child': {
          paddingLeft: '0',
        },
        'thead th:last-child': {
          paddingRight: '0',
        },
        'tbody td, tfoot td': {
          paddingTop: em(8, 12),
          paddingRight: em(12, 12),
          paddingBottom: em(8, 12),
          paddingLeft: em(12, 12),
        },
        'tbody td:first-child, tfoot td:first-child': {
          paddingLeft: '0',
        },
        'tbody td:last-child, tfoot td:last-child': {
          paddingRight: '0',
        },
      },
      {
        '> :first-child': {
          marginTop: '0',
        },
        '> :last-child': {
          marginBottom: '0',
        },
      },
    ],
  },
  base: {
    css: [
      {
        fontSize: rem(16),
        lineHeight: round(28 / 16),
        p: {
          marginTop: em(20, 16),
          marginBottom: em(20, 16),
        },
        '[class~="lead"]': {
          fontSize: em(20, 16),
          lineHeight: round(32 / 20),
          marginTop: em(24, 20),
          marginBottom: em(24, 20),
        },
        blockquote: {
          marginBottom: em(32, 20)
        },
        'blockquote::before': {
          marginTop: em(32, 20),
        },
        'blockquote > p:first-child': {
          marginTop: '0'
        },
        h1: {
          fontSize: em(36, 16),
          marginTop: '0',
          marginBottom: em(32, 36),
          lineHeight: round(40 / 36),
        },
        h2: {
          fontSize: em(24, 16),
          marginTop: '0',
          marginBottom: em(24, 24),
          lineHeight: round(32 / 24),
        },
        h3: {
          fontSize: em(20, 16),
          marginTop: '0',
          marginBottom: em(12, 20),
          lineHeight: round(32 / 20),
        },
        h4: {
          marginTop: '0',
          marginBottom: em(8, 16),
          lineHeight: round(24 / 16),
        },
        img: {
          marginTop: em(32, 16),
          marginBottom: em(32, 16),
        },
        video: {
          marginTop: em(32, 16),
          marginBottom: em(32, 16),
        },
        figure: {
          marginTop: em(32, 16),
          marginBottom: em(32, 16),
        },
        'figure > *': {
          marginTop: '0',
          marginBottom: '0',
        },
        figcaption: {
          fontSize: em(14, 16),
          lineHeight: round(20 / 14),
          marginTop: em(12, 14),
        },
        code: {
          fontSize: em(14, 16),
        },
        'h2 code': {
          fontSize: em(21, 24),
        },
        'h3 code': {
          fontSize: em(18, 20),
        },
        pre: {
          fontSize: em(14, 16),
          lineHeight: round(24 / 14),
          marginTop: em(24, 14),
          marginBottom: em(24, 14),
          borderRadius: rem(6),
          paddingTop: em(12, 14),
          paddingRight: em(16, 14),
          paddingBottom: em(12, 14),
          paddingLeft: em(16, 14),
        },
        ol: {
          marginTop: em(20, 16),
          marginBottom: em(20, 16),
          paddingLeft: em(26, 16),
        },
        ul: {
          marginTop: em(20, 16),
          marginBottom: em(20, 16),
          paddingLeft: em(26, 16),
        },
        li: {
          marginTop: em(8, 16),
          marginBottom: em(8, 16),
        },
        'ol > li': {
          paddingLeft: em(6, 16),
        },
        'ul > li': {
          paddingLeft: em(6, 16),
        },
        '> ul > li p': {
          marginTop: em(12, 16),
          marginBottom: em(12, 16),
        },
        '> ul > li > *:first-child': {
          marginTop: em(20, 16),
        },
        '> ul > li > *:last-child': {
          marginBottom: em(20, 16),
        },
        '> ol > li > *:first-child': {
          marginTop: em(20, 16),
        },
        '> ol > li > *:last-child': {
          marginBottom: em(20, 16),
        },
        'ul ul, ul ol, ol ul, ol ol': {
          marginTop: em(12, 16),
          marginBottom: em(12, 16),
        },
        hr: {
          marginTop: em(48, 16),
          marginBottom: em(48, 16),
        },
        'hr + *': {
          marginTop: '0',
        },
        'h2 + *': {
          marginTop: '0',
        },
        'h3 + *': {
          marginTop: '0',
        },
        'h4 + *': {
          marginTop: '0',
        },
        table: {
          fontSize: em(14, 16),
          lineHeight: round(24 / 14),
        },
        'thead th': {
          paddingRight: em(8, 14),
          paddingBottom: em(8, 14),
          paddingLeft: em(8, 14),
        },
        'thead th:last-child': {
          paddingRight: '0',
        },
        'tbody td, tfoot td': {
          paddingTop: em(8, 14),
          paddingRight: em(8, 14),
          paddingBottom: em(8, 14),
          paddingLeft: em(8, 14),
        },
        'tbody td:last-child, tfoot td:last-child': {
          paddingRight: '0',
        },
      },
      {
        '> :first-child': {
          marginTop: '0',
        },
        '> :last-child': {
          marginBottom: '0',
        },
      },
    ],
  },
  lg: {
    css: [
      {
        fontSize: rem(18),
        lineHeight: round(32 / 18),
        p: {
          marginTop: em(24, 18),
          marginBottom: em(24, 18),
        },
        '[class~="lead"]': {
          fontSize: em(22, 18),
          lineHeight: round(32 / 22),
          marginTop: em(24, 22),
          marginBottom: em(24, 22),
        },
        'blockquote::before': {
          marginTop: em(40, 24),
        },
        'blockquote > p:first-child': {
          marginTop:  em(12, 24)
        },
        h1: {
          fontSize: em(48, 18),
          marginTop: '0',
          marginBottom: em(40, 48),
          lineHeight: round(48 / 48),
        },
        h2: {
          fontSize: em(36, 18),
          marginTop: '0',
          marginBottom: em(20, 30),
          lineHeight: round(40 / 30),
        },
        h3: {
          fontSize: em(24, 18),
          marginTop: '0',
          marginBottom: em(16, 24),
          lineHeight: round(36 / 24),
        },
        h4: {
          marginTop: '0',
          marginBottom: em(8, 18),
          lineHeight: round(28 / 18),
        },
        img: {
          marginTop: em(32, 18),
          marginBottom: em(32, 18),
        },
        video: {
          marginTop: em(32, 18),
          marginBottom: em(32, 18),
        },
        figure: {
          marginTop: em(32, 18),
          marginBottom: em(32, 18),
        },
        'figure > *': {
          marginTop: '0',
          marginBottom: '0',
        },
        figcaption: {
          fontSize: em(16, 18),
          lineHeight: round(24 / 16),
          marginTop: em(16, 16),
        },
        code: {
          fontSize: em(16, 18),
        },
        'h2 code': {
          fontSize: em(26, 30),
        },
        'h3 code': {
          fontSize: em(21, 24),
        },
        pre: {
          fontSize: em(16, 18),
          lineHeight: round(28 / 16),
          marginTop: em(32, 16),
          marginBottom: em(32, 16),
          borderRadius: rem(6),
          paddingTop: em(16, 16),
          paddingRight: em(24, 16),
          paddingBottom: em(16, 16),
          paddingLeft: em(24, 16),
        },
        ol: {
          marginTop: em(24, 18),
          marginBottom: em(24, 18),
          paddingLeft: em(28, 18),
        },
        ul: {
          marginTop: em(24, 18),
          marginBottom: em(24, 18),
          paddingLeft: em(28, 18),
        },
        li: {
          marginTop: em(12, 18),
          marginBottom: em(12, 18),
        },
        'ol > li': {
          paddingLeft: em(8, 18),
        },
        'ul > li': {
          paddingLeft: em(8, 18),
        },
        '> ul > li p': {
          marginTop: em(16, 18),
          marginBottom: em(16, 18),
        },
        '> ul > li > *:first-child': {
          marginTop: em(24, 18),
        },
        '> ul > li > *:last-child': {
          marginBottom: em(24, 18),
        },
        '> ol > li > *:first-child': {
          marginTop: em(24, 18),
        },
        '> ol > li > *:last-child': {
          marginBottom: em(24, 18),
        },
        'ul ul, ul ol, ol ul, ol ol': {
          marginTop: em(16, 18),
          marginBottom: em(16, 18),
        },
        hr: {
          marginTop: em(56, 18),
          marginBottom: em(56, 18),
        },
        'hr + *': {
          marginTop: '0',
        },
        'h2 + *': {
          marginTop: '0',
        },
        'h3 + *': {
          marginTop: '0',
        },
        'h4 + *': {
          marginTop: '0',
        },
        table: {
          fontSize: em(16, 18),
          lineHeight: round(24 / 16),
        },
        'thead th': {
          paddingRight: em(12, 16),
          paddingBottom: em(12, 16),
          paddingLeft: em(12, 16),
        },
        'thead th:last-child': {
          paddingRight: '0',
        },
        'tbody td, tfoot td': {
          paddingTop: em(12, 16),
          paddingRight: em(12, 16),
          paddingBottom: em(12, 16),
          paddingLeft: em(12, 16),
        },
        'tbody td:last-child, tfoot td:last-child': {
          paddingRight: '0',
        },
      },
      {
        '> :first-child': {
          marginTop: '0',
        },
        '> :last-child': {
          marginBottom: '0',
        },
      },
    ],
  },

  // Invert (for dark mode)
  invert: {
    css: {
      '--tw-format-body': 'var(--tw-format-invert-body)',
      '--tw-format-headings': 'var(--tw-format-invert-headings)',
      '--tw-format-lead': 'var(--tw-format-invert-lead)',
      '--tw-format-links': 'var(--tw-format-invert-links)',
      '--tw-format-bold': 'var(--tw-format-invert-bold)',
      '--tw-format-counters': 'var(--tw-format-invert-counters)',
      '--tw-format-bullets': 'var(--tw-format-invert-bullets)',
      '--tw-format-hr': 'var(--tw-format-invert-hr)',
      '--tw-format-quotes': 'var(--tw-format-invert-quotes)',
      '--tw-format-quote-borders': 'var(--tw-format-invert-quote-borders)',
      '--tw-format-captions': 'var(--tw-format-invert-captions)',
      '--tw-format-code': 'var(--tw-format-invert-code)',
      '--tw-format-code-bg': 'var(--tw-format-invert-code-bg)',
      '--tw-format-pre-code': 'var(--tw-format-invert-pre-code)',
      '--tw-format-pre-bg': 'var(--tw-format-invert-pre-bg)',
      '--tw-format-th-borders': 'var(--tw-format-invert-th-borders)',
      '--tw-format-td-borders': 'var(--tw-format-invert-td-borders)',
      '--tw-format-th-bg': 'var(--tw-format-invert-th-bg)'
    },
  },

  // Gray color themes
  gray: {
    css: {
      '--tw-format-body': colors.gray[500],
      '--tw-format-headings': colors.gray[900],
      '--tw-format-lead': colors.gray[500],
      '--tw-format-links': colors.gray[600],
      '--tw-format-bold': colors.gray[900],
      '--tw-format-counters': colors.gray[500],
      '--tw-format-bullets': colors.gray[500],
      '--tw-format-hr': colors.gray[200],
      '--tw-format-quotes': colors.gray[900],
      '--tw-format-quote-borders': colors.gray[200],
      '--tw-format-captions': colors.gray[500],
      '--tw-format-code': colors.gray[900],
      '--tw-format-code-bg': colors.gray[100],
      '--tw-format-pre-code': colors.gray[600],
      '--tw-format-pre-bg': colors.gray[100],
      '--tw-format-th-borders': colors.gray[200],
      '--tw-format-th-bg': colors.gray[50],
      '--tw-format-td-borders': colors.gray[200],
      '--tw-format-invert-body': colors.gray[400],
      '--tw-format-invert-headings': colors.white,
      '--tw-format-invert-lead': colors.gray[400],
      '--tw-format-invert-links': colors.white,
      '--tw-format-invert-bold': colors.white,
      '--tw-format-invert-counters': colors.gray[400],
      '--tw-format-invert-bullets': colors.gray[600],
      '--tw-format-invert-hr': colors.gray[700],
      '--tw-format-invert-quotes': colors.gray[100],
      '--tw-format-invert-quote-borders': colors.gray[700],
      '--tw-format-invert-captions': colors.gray[400],
      '--tw-format-invert-code': colors.white,
      '--tw-format-invert-code-bg': colors.gray[800],
      '--tw-format-invert-pre-code': colors.gray[300],
      '--tw-format-invert-pre-bg': colors.gray[700],
      '--tw-format-invert-th-borders': colors.gray[600],
      '--tw-format-invert-td-borders': colors.gray[700],
      '--tw-format-invert-th-bg': colors.gray[700],
    },
  },

  // Link-only themes (for backward compatibility)
  red: {
    css: {
      '--tw-format-links': colors.red[600],
      '--tw-format-invert-links': colors.red[500],
    },
  },

  orange: {
    css: {
      '--tw-format-links': colors.orange[600],
      '--tw-format-invert-links': colors.orange[500],
    },
  },

  amber: {
    css: {
      '--tw-format-links': colors.amber[600],
      '--tw-format-invert-links': colors.amber[500],
    },
  },

  yellow: {
    css: {
      '--tw-format-links': colors.yellow[600],
      '--tw-format-invert-links': colors.yellow[500],
    },
  },

  lime: {
    css: {
      '--tw-format-links': colors.lime[600],
      '--tw-format-invert-links': colors.lime[500],
    },
  },

  green: {
    css: {
      '--tw-format-links': colors.green[600],
      '--tw-format-invert-links': colors.green[500],
    },
  },

  emerald: {
    css: {
      '--tw-format-links': colors.emerald[600],
      '--tw-format-invert-links': colors.emerald[500],
    },
  },

  teal: {
    css: {
      '--tw-format-links': colors.teal[600],
      '--tw-format-invert-links': colors.teal[500],
    },
  },

  cyan: {
    css: {
      '--tw-format-links': colors.cyan[600],
      '--tw-format-invert-links': colors.cyan[500],
    },
  },

  sky: {
    css: {
      '--tw-format-links': colors.sky[600],
      '--tw-format-invert-links': colors.sky[500],
    },
  },

  blue: {
    css: {
      '--tw-format-links': colors.blue[600],
      '--tw-format-invert-links': colors.blue[500],
    },
  },

  indigo: {
    css: {
      '--tw-format-links': colors.indigo[600],
      '--tw-format-invert-links': colors.indigo[500],
    },
  },

  violet: {
    css: {
      '--tw-format-links': colors.violet[600],
      '--tw-format-invert-links': colors.violet[500],
    },
  },

  purple: {
    css: {
      '--tw-format-links': colors.purple[600],
      '--tw-format-invert-links': colors.purple[500],
    },
  },

  fuchsia: {
    css: {
      '--tw-format-links': colors.fuchsia[600],
      '--tw-format-invert-links': colors.fuchsia[500],
    },
  },

  pink: {
    css: {
      '--tw-format-links': colors.pink[600],
      '--tw-format-invert-links': colors.pink[500],
    },
  },

  rose: {
    css: {
      '--tw-format-links': colors.rose[600],
      '--tw-format-invert-links': colors.rose[500],
    },
  },
}

module.exports = {
  DEFAULT: {
    css: [
      {
        color: 'var(--tw-format-body)',
        maxWidth: '65ch',
        '[class~="lead"]': {
          color: 'var(--tw-format-lead)',
        },
        a: {
          color: 'var(--tw-format-links)',
          textDecoration: 'underline',
          fontWeight: '500',
          '&:hover': {
            textDecoration: 'none'
          }
        },
        strong: {
          color: 'var(--tw-format-bold)',
          fontWeight: '700',
        },
        'a strong': {
          color: 'inherit',
        },
        'blockquote strong': {
          color: 'inherit',
        },
        'thead th strong': {
          color: 'inherit',
        },
        ol: {
          listStyleType: 'decimal',
        },
        'ol[type="A"]': {
          listStyleType: 'upper-alpha',
        },
        'ol[type="a"]': {
          listStyleType: 'lower-alpha',
        },
        'ol[type="A" s]': {
          listStyleType: 'upper-alpha',
        },
        'ol[type="a" s]': {
          listStyleType: 'lower-alpha',
        },
        'ol[type="I"]': {
          listStyleType: 'upper-roman',
        },
        'ol[type="i"]': {
          listStyleType: 'lower-roman',
        },
        'ol[type="I" s]': {
          listStyleType: 'upper-roman',
        },
        'ol[type="i" s]': {
          listStyleType: 'lower-roman',
        },
        'ol[type="1"]': {
          listStyleType: 'decimal',
        },
        ul: {
          listStyleType: 'disc',
        },
        'ol > li::marker': {
          fontWeight: '400',
          color: 'var(--tw-format-counters)',
        },
        'ul > li::marker': {
          color: 'var(--tw-format-bullets)',
        },
        hr: {
          borderColor: 'var(--tw-format-hr)',
          borderTopWidth: 1,
        },
        blockquote: {
          fontSize: em(20, 18),
          fontWeight: '700',
          fontStyle: 'italic',
          color: 'var(--tw-format-quotes)',
          quotes: '"\\201C""\\201D""\\2018""\\2019"',
        },
        'blockquote::before': {
          content: '""',
          backgroundImage: `url("data:image/svg+xml,%0A%3Csvg width='32' height='24' viewBox='0 0 32 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M18.6893 24V14.1453C18.6893 6.54 23.664 1.38533 30.6667 -7.15256e-07L31.9933 2.868C28.7507 4.09066 26.6667 7.71867 26.6667 10.6667H32V24H18.6893ZM-9.53674e-07 24V14.1453C-9.53674e-07 6.54 4.99733 1.384 12 -7.15256e-07L13.328 2.868C10.084 4.09066 8 7.71867 8 10.6667L13.3107 10.6667V24H-9.53674e-07Z' fill='%239CA3AF'/%3E%3C/svg%3E%0A")`,
          backgroundRepeat: 'no-repeat',
          color: 'var(--tw-format-quotes)',
          width: em(32, 18),
          height: em(24, 18),
          display: 'block',
        },
        'blockquote p:first-of-type::before': {
          content: 'open-quote',
        },
        'blockquote p:last-of-type::after': {
          content: 'close-quote',
        },
        h1: {
          color: 'var(--tw-format-headings)',
          fontWeight: '800',
        },
        'h1 strong': {
          fontWeight: '900',
          color: 'inherit',
        },
        h2: {
          color: 'var(--tw-format-headings)',
          fontWeight: '700',
        },
        'h2 strong': {
          fontWeight: '800',
          color: 'inherit',
        },
        h3: {
          color: 'var(--tw-format-headings)',
          fontWeight: '700',
        },
        'h3 strong': {
          fontWeight: '800',
          color: 'inherit',
        },
        h4: {
          color: 'var(--tw-format-headings)',
          fontWeight: '600',
        },
        'h4 strong': {
          fontWeight: '700',
          color: 'inherit',
        },
        // TODO: Figure out how to not need these, it's a merging issue
        img: {},
        'figure > *': {},
        figcaption: {
          color: 'var(--tw-format-captions)',
        },
        code: {
          color: 'var(--tw-format-code)',
          fontWeight: '600',
          backgroundColor: 'var(--tw-format-code-bg)',
          paddingTop: em(6, 18),
          paddingBottom: em(6, 18),
          paddingLeft: em(10, 18),
          paddingRight: em(10, 18),
          borderRadius: em(4, 18)
        },
        'a code': {
          color: 'inherit',
        },
        'h1 code': {
          color: 'inherit',
        },
        'h2 code': {
          color: 'inherit',
        },
        'h3 code': {
          color: 'inherit',
        },
        'h4 code': {
          color: 'inherit',
        },
        'blockquote code': {
          color: 'inherit',
        },
        'thead th code': {
          color: 'inherit',
        },
        pre: {
          color: 'var(--tw-format-pre-code)',
          backgroundColor: 'var(--tw-format-pre-bg)',
          overflowX: 'auto',
          fontWeight: '400',
        },
        'pre code': {
          backgroundColor: 'transparent',
          borderWidth: '0',
          borderRadius: '0',
          padding: '0',
          fontWeight: 'inherit',
          color: 'inherit',
          fontSize: 'inherit',
          fontFamily: 'inherit',
          lineHeight: 'inherit',
        },
        'pre code::before': {
          content: 'none',
        },
        'pre code::after': {
          content: 'none',
        },
        table: {
          width: '100%',
          tableLayout: 'auto',
          textAlign: 'left',
          marginTop: em(32, 16),
          marginBottom: em(32, 16),
        },
        thead: {
          backgroundColor: 'var(--tw-format-th-bg)',
          borderRadius: em(5, 18),
        },
        'thead th': {
          color: 'var(--tw-format-headings)',
          fontWeight: '600',
          verticalAlign: 'bottom',
          padding: em(10, 18)
        },
        'tbody tr': {
          borderBottomWidth: '1px',
          borderBottomColor: 'var(--tw-format-td-borders)',
        },
        'tbody tr:last-child': {
          borderBottomWidth: '0',
        },
        'tbody td': {
          verticalAlign: 'baseline',
        },
        tfoot: {
          borderTopWidth: '1px',
          borderTopColor: 'var(--tw-format-th-borders)',
        },
        'tfoot td': {
          verticalAlign: 'top',
        },
      },
      defaultModifiers.gray.css,
      ...defaultModifiers.base.css,
    ],
  },
  ...defaultModifiers,
}
