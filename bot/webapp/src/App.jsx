import React, { useEffect, useState } from 'react';
import { TonConnectButton, useTonWallet, useTonConnectUI } from '@tonconnect/ui-react';
import WebApp from '@twa-dev/sdk';

function App() {
  const wallet = useTonWallet();
  const [tonConnectUI] = useTonConnectUI();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
      // Convert TON amount to nanotons (1 TON = 1e9 nanotons)
      const amountInNanotons = BigInt(Math.round(parseFloat(product.priceInTon) * 1e9)).toString();

      // Create transaction with text comment instead of payload
      const transaction = {
        validUntil: Math.floor(Date.now() / 1000) + 600, // 10 minutes
        messages: [
          {
            address: import.meta.env.VITE_TON_WALLET_ADDRESS,
            amount: amountInNanotons,
            // Remove stateInit and use text comment instead
            payload: `text=${product.paymentId}`
          }
        ]
      };

      console.log('Sending transaction:', transaction);

      // Send transaction
      const result = await tonConnectUI.sendTransaction(transaction);
      
      if (result) {
        console.log('Transaction result:', result);
        // Notify the bot about successful transaction
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
      WebApp.showAlert('Transaction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>E-Pin Purchase</h1>
      </header>

      <main>
        {error ? (
          <div className="error-message">{error}</div>
        ) : product ? (
          <div className="product-details">
            <h2>{product.type}</h2>
            <p>Price: {product.priceInTon} TON</p>
            <p>Quantity: {product.quantity}</p>
          </div>
        ) : (
          <p>Loading product details...</p>
        )}

        <div className="wallet-section">
          <TonConnectButton />
          
          {wallet && product && (
            <button 
              onClick={handlePurchase}
              disabled={loading}
              className="purchase-button"
            >
              {loading ? 'Processing...' : 'Purchase E-Pin'}
            </button>
          )}
        </div>
      </main>
    </div>
  );
}

export default App; 