from aiohttp import ClientSession
from config.settings import TON_WALLET_ADDRESS, TON_TESTNET, TON_API_KEY
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from utils.logger import setup_logger
from exchange_service import get_ton_price

logger = setup_logger()

class TONService:
    def __init__(self):
        self.base_url = "https://testnet.toncenter.com/api/v2" if TON_TESTNET else "https://toncenter.com/api/v2"
        self.headers = {"X-API-Key": TON_API_KEY} if TON_API_KEY else {}
        logger.info(f"Initialized TONService with base URL: {self.base_url}")
        
    async def verify_payment(self, payment_id: str, expected_amount: Decimal) -> dict:
        """Verify payment with transaction details"""
        try:
            logger.info(f"Verifying payment {payment_id} for {expected_amount} TON")
            
            # Get transactions for the last 30 minutes
            time_window = datetime.now() - timedelta(minutes=30)
            timestamp = int(time_window.timestamp())
            
            logger.info(f"Checking transactions since {time_window}")
            
            async with ClientSession() as session:
                # Query transactions for our wallet
                url = f"{self.base_url}/getTransactions"
                params = {
                    "address": TON_WALLET_ADDRESS,
                    "limit": 100,
                    "to_lt": 0,
                    "archival": False
                }
                
                logger.info(f"Requesting transactions from {url}")
                logger.info(f"Request params: {params}")
                
                async with session.get(
                    url,
                    params=params,
                    headers=self.headers
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"TON API error: {error_text}")
                        return {"verified": False}
                    
                    data = await response.json()
                    transactions = data.get("result", [])
                    logger.info(f"Found {len(transactions)} transactions")
                    
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
                        
                        logger.info(f"Checking transaction:")
                        logger.info(f"Amount: {tx_amount} TON")
                        logger.info(f"Comment: {tx_comment}")
                        logger.info(f"Timestamp: {datetime.fromtimestamp(tx_timestamp)}")
                        
                        # Verify transaction matches our criteria
                        amount_matches = abs(tx_amount - expected_amount) < Decimal("0.01")  # Allow 0.01 TON difference
                        comment_matches = str(payment_id) in tx_comment
                        time_valid = tx_timestamp >= timestamp
                        
                        logger.info(f"Verification checks:")
                        logger.info(f"Amount matches: {amount_matches}")
                        logger.info(f"Comment matches: {comment_matches}")
                        logger.info(f"Time valid: {time_valid}")
                        
                        if amount_matches and comment_matches and time_valid:
                            logger.info("Transaction verified successfully!")
                            return {
                                "verified": True,
                                "transaction_hash": tx.get("transaction_id", {}).get("hash", ""),
                                "amount": float(tx_amount),
                                "timestamp": tx_timestamp
                            }
            
            logger.info("No matching transaction found")
            return {"verified": False}
            
        except Exception as e:
            logger.error(f"Error verifying TON payment: {str(e)}", exc_info=True)
            return {"verified": False} 