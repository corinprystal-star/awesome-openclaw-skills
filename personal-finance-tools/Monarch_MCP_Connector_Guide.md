# Setting Up Monarch Money as a Manus MCP Connector

This guide explains how to add the Monarch Money MCP server as a **Custom MCP** connector in Manus, so it can pull your financial data automatically in future sessions.

---

## Option 1: Custom MCP Connector (Recommended)

### Step 1: Get Your Monarch Session Token

You need a session token from Monarch Money. Two ways to get it:

**Method A — From the login script:**
```bash
cd ~/monarch-mcp-server
python login_setup.py
```
After login, the token is saved. You can find it at `~/.monarch_finance/token.txt`.

**Method B — From your browser:**
1. Log into [monarchmoney.com](https://www.monarchmoney.com)
2. Open Developer Tools (F12)
3. Go to Application → Local Storage → `https://app.monarchmoney.com`
4. Find the `token` key
5. Copy the value

### Step 2: Add as Custom MCP in Manus

1. Go to **Manus Settings → Connectors → Custom MCP**
2. Add a new Custom MCP server with:
   - **Name:** `Monarch Money`
   - **Command:** `python3`
   - **Args:** `["/path/to/monarch-mcp-server/src/monarch_mcp_server/server.py"]`
   - **Environment Variables:**
     - `MONARCH_TOKEN`: (your session token)

### Step 3: Verify

Ask Manus: "Check my Monarch Money accounts" — it should list your linked accounts.

---

## Option 2: Environment Variable Auth

If you don't want to run the login script, set these environment variables:

```
MONARCH_EMAIL=your@email.com
MONARCH_PASSWORD=your_password
```

The MCP server will auto-login on first use.

---

## Option 3: Use the Standalone Helper Script

If the MCP connector isn't available, use the standalone script:

```bash
python3 ~/monarch_finance_helper.py --login      # One-time setup
python3 ~/monarch_finance_helper.py --full-audit  # Full report
```

---

## What You Get Once Connected

| Tool | Description |
|------|-------------|
| `get_accounts` | All accounts with balances |
| `get_transactions` | Transaction history with filters |
| `get_budgets` | Budget vs. actual spending |
| `get_cashflow` | Income vs. expense analysis |
| `get_net_worth` | Net worth over time |
| `get_recurring_transactions` | All recurring bills |
| `search_transactions` | Search by merchant, amount, date |
| `get_spending_summary` | Spending by category |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Authentication needed" | Re-run login script |
| "Session expired" | Tokens last weeks/months but can expire. Re-login. |
| "Module not found" | Run `pip install monarchmoneycommunity` |
| SoFi not showing | Ensure SoFi is linked in Monarch Money app first |
