import React from 'react';
import ReactDOM from 'react-dom/client';
import { TonConnectUIProvider } from '@tonconnect/ui-react';
import App from './App';
import './index.css';

// Use environment variable for manifest URL
const manifestUrl = `${import.meta.env.VITE_WEBAPP_URL}/tonconnect-manifest.json`;

// TON Connect configuration
const tonConnectOptions = {
  manifestUrl,
  walletsUiPreset: 'all',
  actionsConfiguration: {
    twaReturnUrl: import.meta.env.VITE_WEBAPP_URL,
  }
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <TonConnectUIProvider {...tonConnectOptions}>
      <App />
    </TonConnectUIProvider>
  </React.StrictMode>
); 