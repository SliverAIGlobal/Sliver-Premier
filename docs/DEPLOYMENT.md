# PRISM 9 API & Deployment Documentation

## Cloudflare Workers Deployment Checklist

Before deploying PRISM 9 to Cloudflare Workers, verify each item in this operational checklist:

1. [ ] **Environment Setup**: Set `CF_ACCOUNT_ID` and `CF_API_TOKEN` secrets in repository secrets / Cloudflare dashboard.
2. [ ] **KV Binding**: Create the `API_CACHE` namespace via `npx wrangler kv:namespace create API_CACHE` and update `wrangler.toml` with the generated KV ID.
3. [ ] **Domain & Route**: Configure production route in `wrangler.toml` (e.g. `pattern = "prism9.yourdomain.com/*"`).
4. [ ] **API Keys**: Configure `GEMINI_API_KEY` in Wrangler secrets (`npx wrangler secret put GEMINI_API_KEY`).
5. [ ] **WASM Build Verification**: Ensure `npm run build:all` executes cleanly and outputs `/dist` with `/public/pkg` static WASM assets.
6. [ ] **Rate Limiting**: Confirm `RATE_LIMIT_ENABLED = "true"` and `MAX_REQUESTS_PER_MINUTE = "60"`.
7. [ ] **Worker Health Check**: Perform GET request to `/api/proxy` to verify CORS headers and status response.
