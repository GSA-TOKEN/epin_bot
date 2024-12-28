import React, { useEffect, useState } from 'react';
import { TonConnectButton, useTonWallet, useTonConnectUI } from '@tonconnect/ui-react';
import WebApp from '@twa-dev/sdk';

function App() {
  const wallet = useTonWallet();
  const [tonConnectUI] = useTonConnectUI();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showManualInstructions, setShowManualInstructions] = useState(false);

  useEffect(() => {
    // Get product details from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const initData = urlParams.get('initData');
    
    if (initData) {
      try {
        const decodedData = decodeURIComponent(initData);
        const data = JSON.parse(decodedData);
        console.log('Parsed product data:', data.product);
        setProduct(data.product);
        setError(null);
      } catch (e) {
        console.error('Failed to parse init data:', e);
        setError('Failed to load product details. Please try again.');
      }
    } else {
      setError('No product data found. Please start from the bot.');
    }

    WebApp.ready();
    WebApp.expand();
  }, []);

  const handlePurchase = async () => {
    if (!wallet || !product) return;

    setLoading(true);
    try {
      const amountInNanotons = BigInt(Math.round(parseFloat(product.priceInTon) * 1e9)).toString();

      const transaction = {
        validUntil: Math.floor(Date.now() / 1000) + 600,
        messages: [
          {
            address: import.meta.env.VITE_TON_WALLET_ADDRESS,
            amount: amountInNanotons,
            stateInit: null,
            payload: product.paymentId.toString(),
          }
        ]
      };

      console.log('Debug - Transaction Details:', {
        address: import.meta.env.VITE_TON_WALLET_ADDRESS,
        amount: Number(amountInNanotons) / 1e9,
        paymentId: product.paymentId
      });

      const result = await tonConnectUI.sendTransaction(transaction);
      
      if (result) {
        console.log('Transaction result:', result);
        WebApp.sendData(JSON.stringify({
          type: 'payment_success',
          transactionHash: result.boc,
          walletAddress: wallet.account.address,
          paymentId: product.paymentId
        }));
        
        WebApp.close();
      }
    } catch (e) {
      console.error('Transaction failed:', e);
      WebApp.showAlert('Transaction failed: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    WebApp.showAlert('Copied to clipboard!');
  };

  return (
    <div className="App">
      <header>
        <h1>💎 E-Pin Purchase</h1>
      </header>

      <main>
        {error ? (
          <div className="error-message">{error}</div>
        ) : product ? (
          <>
            <div className="product-details">
              <div className="product-header">
                <h2>{product.type}</h2>
                <span className="product-badge">Testnet</span>
              </div>
              <div className="price-tag">
                <span className="amount">{product.priceInTon}</span>
                <span className="currency">TON</span>
              </div>
              <div className="quantity">Quantity: {product.quantity}</div>
            </div>

            <div className="payment-section">
              <h3>Payment Methods</h3>
              
              <div className="connect-wallet-section">
                <p className="section-description">
                  Option 1: Connect your wallet directly (recommended)
                </p>
                <TonConnectButton />
                
                {wallet && (
                  <button 
                    onClick={handlePurchase}
                    disabled={loading}
                    className="purchase-button"
                  >
                    {loading ? '⏳ Processing...' : '💎 Purchase E-Pin'}
                  </button>
                )}
              </div>

              <div className="manual-section">
                <p className="section-description">
                  Option 2: Manual Payment
                  <button 
                    onClick={() => setShowManualInstructions(!showManualInstructions)}
                    className="toggle-button"
                  >
                    {showManualInstructions ? 'Hide Instructions' : 'Show Instructions'}
                  </button>
                </p>

                {showManualInstructions && (
                  <div className="manual-instructions">
                    <div className="instruction-step">
                      <h4>1. Copy Wallet Address</h4>
                      <div className="copy-field" onClick={() => copyToClipboard(import.meta.env.VITE_TON_WALLET_ADDRESS)}>
                        <code>{import.meta.env.VITE_TON_WALLET_ADDRESS}</code>
                        <button className="copy-button">📋 Copy</button>
                      </div>
                    </div>

                    <div className="instruction-step">
                      <h4>2. Amount to Send</h4>
                      <div className="copy-field" onClick={() => copyToClipboard(product.priceInTon)}>
                        <code>{product.priceInTon} TON</code>
                        <button className="copy-button">📋 Copy</button>
                      </div>
                    </div>

                    <div className="instruction-step">
                      <h4>3. Add Comment (Required)</h4>
                      <div className="copy-field" onClick={() => copyToClipboard(product.paymentId)}>
                        <code>{product.paymentId}</code>
                        <button className="copy-button">📋 Copy</button>
                      </div>
                    </div>

                    <div className="warning-box">
                      ⚠️ Important:
                      <ul>
                        <li>Send <strong>exactly</strong> {product.priceInTon} TON</li>
                        <li>Include the payment ID in the comment</li>
                        <li>Double-check the wallet address</li>
                        <li>Transaction may take 1-2 minutes to confirm</li>
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Loading product details...</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 