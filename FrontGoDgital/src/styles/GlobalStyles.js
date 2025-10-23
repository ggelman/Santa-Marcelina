import { createGlobalStyle, ThemeProvider } from "styled-components"
import PropTypes from "prop-types"

import { synviaTheme } from "./theme"

export const GlobalStyles = createGlobalStyle`
  :root {
    --synvia-space-cadet: ${synviaTheme.colors.spaceCadet};
    --synvia-snow: ${synviaTheme.colors.snow};
    --synvia-steel-blue: ${synviaTheme.colors.steelBlue};
    --synvia-asparagus: ${synviaTheme.colors.asparagus};
    --synvia-smoky-black: ${synviaTheme.colors.smokyBlack};
    --synvia-graphite: ${synviaTheme.colors.graphiteGray};
    --synvia-background: ${synviaTheme.colors.background};
    --synvia-surface: ${synviaTheme.colors.surface};
    --synvia-surface-alt: ${synviaTheme.colors.surfaceAlt};
    --synvia-text-primary: ${synviaTheme.colors.textPrimary};
    --synvia-text-secondary: ${synviaTheme.colors.textSecondary};
    --synvia-text-muted: ${synviaTheme.colors.textMuted};
    --synvia-accent-primary: ${synviaTheme.colors.accentPrimary};
    --synvia-accent-secondary: ${synviaTheme.colors.accentSecondary};
    --synvia-border: ${synviaTheme.colors.border};
    --synvia-shadow-soft: ${synviaTheme.colors.shadowSoft};
    --synvia-focus-ring: ${synviaTheme.colors.focusRing};
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: ${synviaTheme.typography.primary};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: var(--synvia-background);
    color: var(--synvia-text-primary);
    line-height: 1.6;
    overflow-y: scroll;
  }

  button {
    border: none;
    cursor: pointer;
    font-family: inherit;
  }

  input, textarea, select {
    font-family: inherit;
  }

  a {
    color: inherit;
    text-decoration: none;
  }

  ul, ol {
    list-style: none;
  }

  img {
    max-width: 100%;
    height: auto;
  }

  @keyframes slide-in {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slide-out {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }

  .animate-slide-in {
    animation: slide-in 0.3s ease-out;
  }

  .animate-slide-out {
    animation: slide-out 0.3s ease-in;
  }

  .security-alert-critical {
    border-left: 4px solid #ef4444;
  }

  .security-alert-warning {
    border-left: 4px solid #f59e0b;
  }

  .security-alert-info {
    border-left: 4px solid var(--synvia-accent-primary);
  }

  .status-indicator {
    position: relative;
  }

  .status-indicator::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: currentColor;
  }

  .status-healthy::before {
    background-color: var(--synvia-accent-secondary);
  }

  .status-warning::before {
    background-color: #f59e0b;
  }

  .status-critical::before {
    background-color: #ef4444;
  }
`

export const ThemeWrapper = ({ children }) => (
  <ThemeProvider theme={synviaTheme}>
    <GlobalStyles />
    {children}
  </ThemeProvider>
)

ThemeWrapper.propTypes = {
  children: PropTypes.node,
}
