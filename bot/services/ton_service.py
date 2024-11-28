from aiohttp import ClientSession
from config.settings import TON_WALLET_ADDRESS, TON_TESTNET, TON_API_KEY
import logging
from datetime import datetime, timedelta
from decimal import Decimal

class TONService:
    def __init__(self):
        self.base_url = "https://testnet.toncenter.com/api/v2" if TON_TESTNET else "https://toncenter.com/api/v2"
        self.headers = {"X-API-Key": TON_API_KEY} if TON_API_KEY else {}
        
    async def verify_payment(self, payment_id: str, expected_amount: float) -> dict:
        """Verify payment with transaction details"""
        try:
            # Get transactions for the last 30 minutes
            time_window = datetime.now() - timedelta(minutes=30)
            timestamp = int(time_window.timestamp())
            
            async with ClientSession() as session:
                # Query transactions for our wallet
                async with session.get(
                    f"{self.base_url}/getTransactions",
                    params={
                        "address": TON_WALLET_ADDRESS,
                        "limit": 100,
                        "to_lt": 0,
                        "archival": False
                    },
                    headers=self.headers
                ) as response:
                    if response.status != 200:
                        logging.error(f"TON API error: {await response.text()}")
                        return {"verified": False}
                    
                    data = await response.json()
                    transactions = data.get("result", [])
                    
                    # Look for matching transaction
                    for tx in transactions:
                        # Skip outgoing transactions
                        if tx.get("out_msgs", []):
                            continue
                            
                        # Get transaction details
                        in_msg = tx.get("in_msg", {})
                        tx_amount = Decimal(str(in_msg.get("value", "0"))) / Decimal("1000000000")  # Convert from nanoTON
                        tx_comment = in_msg.get("message", "")
                        tx_timestamp = tx.get("utime", 0)
                        
                        # Verify transaction matches our criteria
                        amount_matches = abs(tx_amount - Decimal(str(expected_amount))) < Decimal("0.01")  # Allow 0.01 TON difference
                        comment_matches = str(payment_id) in tx_comment
                        time_valid = tx_timestamp >= timestamp
                        
                        if amount_matches and comment_matches and time_valid:
                            return {
                                "verified": True,
                                "transaction_hash": tx.get("transaction_id", {}).get("hash", ""),
                                "amount": float(tx_amount),
                                "timestamp": tx_timestamp
                            }
                            
            return {"verified": False}
            
        except Exception as e:
            logging.error(f"Error verifying TON payment: {e}")
            return {"verified": False} 