import { createGlobalStyle, ThemeProvider } from "styled-components"
import PropTypes from 'prop-types'

export const GlobalStyles = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Nunito Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #FDFBF7;
    color: #3D2C21;
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
  /* Animações para alertas de segurança */
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

  /* Estilos para componentes de segurança */
  .security-alert-critical {
    border-left: 4px solid #ef4444;
  }

  .security-alert-warning {
    border-left: 4px solid #f59e0b;
  }

  .security-alert-info {
    border-left: 4px solid #3b82f6;
  }

  /* Indicadores de status */
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
    background-color: #10b981;
  }

  .status-warning::before {
    background-color: #f59e0b;
  }

  .status-critical::before {
    background-color: #ef4444;
  }
`

export const theme = {
  colors: {
    // Cores principais da Padaria Santa Marcelina
    primary: "#B8860B", // Dourado da logo
    primaryDark: "#9A7209",
    primaryLight: "#D4A017",

    // Cores de fundo
    background: "#FDFBF7",
    white: "#FFFFFF",
    lightGray: "#F8F9FA",
    border: "#E9ECEF",

    // Cores de texto
    textPrimary: "#3D2C21",
    textSecondary: "#6C757D",
    textLight: "#ADB5BD",

    // Cores de status
    success: "#28A745",
    danger: "#DC3545",
    warning: "#FFC107",
    info: "#17A2B8",

    // Cores específicas da padaria
    wheat: "#F5DEB3",
    brown: "#8B4513",
    cream: "#FFFDD0",
  },

  breakpoints: {
    mobile: "768px",
    tablet: "1024px",
    desktop: "1200px",
  },

  shadows: {
    small: "0 2px 4px rgba(0,0,0,0.1)",
    medium: "0 4px 8px rgba(0,0,0,0.15)",
    large: "0 8px 16px rgba(0,0,0,0.2)",
  },

  borderRadius: {
    small: "4px",
    medium: "8px",
    large: "12px",
    round: "50%",
  },
}

export const ThemeWrapper = ({ children }) => (
  <ThemeProvider theme={theme}>
    <GlobalStyles />
    {children}
  </ThemeProvider>
)

ThemeWrapper.propTypes = {
  children: PropTypes.node
}
