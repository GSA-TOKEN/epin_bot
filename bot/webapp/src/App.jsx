import React, { useEffect, useState } from 'react';
import { TonConnectButton, useTonWallet, useTonConnectUI } from '@tonconnect/ui-react';
import WebApp from '@twa-dev/sdk';

function App() {
  const wallet = useTonWallet();
  const [tonConnectUI] = useTonConnectUI();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Get product details from Telegram WebApp init data
    const initData = WebApp.initData || '';
    if (initData) {
      try {
        const data = JSON.parse(decodeURIComponent(initData));
        setProduct(data.product);
      } catch (e) {
        console.error('Failed to parse init data:', e);
      }
    }

    WebApp.ready();
    WebApp.expand();
  }, []);

  const handlePurchase = async () => {
    if (!wallet || !product) return;

    setLoading(true);
    try {
      // Create transaction
      const transaction = {
        validUntil: Math.floor(Date.now() / 1000) + 600, // 10 minutes
        messages: [
          {
            address: import.meta.env.VITE_TON_WALLET_ADDRESS,
            amount: product.priceInTon.toString(),
            payload: product.paymentId.toString()
          }
        ]
      };

      // Send transaction
      const result = await tonConnectUI.sendTransaction(transaction);
      
      if (result) {
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
        {product ? (
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