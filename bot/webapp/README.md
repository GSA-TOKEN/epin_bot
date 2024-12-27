# E-Pin Bot WebApp

This is the Telegram WebApp component of the E-Pin Bot, providing TON Connect wallet integration for e-pin purchases.

## Setup

1. Install dependencies:

```bash
npm install
```

2. Configure environment:

   - Copy `.env.example` to `.env`
   - Update the following variables:
     - `VITE_TON_WALLET_ADDRESS`: Your TON wallet address
     - `VITE_WEBAPP_URL`: Your WebApp domain

3. Update manifest:

   - Edit `public/tonconnect-manifest.json`
   - Replace all instances of `your-domain.com` with your actual domain

4. Build for production:

```bash
npm run build
```

5. Deploy:
   - Deploy the built files (in `dist/`) to your web server
   - Ensure your domain has HTTPS enabled
   - Configure CORS to allow Telegram domains

## Development

1. Start development server:

```bash
npm run dev
```

2. Test in Telegram:
   - Use [ngrok](https://ngrok.com/) for local testing
   - Update `WEBAPP_URL` in bot's `.env` with ngrok URL
   - Configure allowed domains in BotFather:
     ```
     /mybots > [YourBot] > Bot Settings > Menu Button > Edit Menu Button URL
     ```

## Integration with Bot

1. The WebApp receives product details and payment ID via URL parameters
2. After successful payment:
   - Transaction details are sent back to the bot
   - Bot verifies the transaction and delivers e-pin codes
   - User's wallet address is stored for future reference

## Security Notes

- Always verify transactions server-side
- Never trust client-side data without verification
- Keep your TON wallet private key secure
- Monitor transaction confirmations

## Troubleshooting

1. WebApp not loading:

   - Check CORS configuration
   - Verify HTTPS setup
   - Confirm domain is allowed in BotFather

2. Payment issues:

   - Check TON Connect manifest configuration
   - Verify wallet address format
   - Ensure sufficient TON balance

3. Transaction verification:
   - Check TON API key validity
   - Verify network configuration (mainnet/testnet)
   - Monitor logs for detailed errors
