#!/usr/bin/env python3
"""
Corin's Monarch Money Finance Helper
=====================================
A standalone script to interact with Monarch Money for:
- Cash flow analysis
- Debt tracking
- Budget monitoring
- Subscription auditing

Usage:
    python3 monarch_finance_helper.py --login       # First-time login
    python3 monarch_finance_helper.py --accounts    # List all accounts
    python3 monarch_finance_helper.py --cashflow    # Cash flow summary
    python3 monarch_finance_helper.py --recurring   # Recurring bills
    python3 monarch_finance_helper.py --budgets     # Budget status
    python3 monarch_finance_helper.py --debts       # Debt summary
    python3 monarch_finance_helper.py --full-audit  # Full financial audit
"""

import sys
import os
import json
import asyncio
import getpass
from datetime import datetime, timedelta
from pathlib import Path

# Fix path for installed packages
sys.path.insert(0, '/usr/local/lib/python3.11/dist-packages')

from monarchmoney import MonarchMoney

# Token storage
TOKEN_DIR = Path.home() / ".monarch_finance"
TOKEN_FILE = TOKEN_DIR / "token.txt"


def save_token(token: str):
    """Save auth token to file."""
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token)
    TOKEN_FILE.chmod(0o600)
    print(f"✅ Token saved to {TOKEN_FILE}")


def load_token() -> str | None:
    """Load auth token from file."""
    if TOKEN_FILE.is_file():
        token = TOKEN_FILE.read_text().strip()
        if token:
            return token
    return None


async def login():
    """Interactive login to Monarch Money."""
    print("\n🔐 Monarch Money Login")
    print("=" * 40)
    
    choice = input("\nLogin method:\n  1. Email/Password\n  2. Session Token (from browser)\n\nChoice (1 or 2): ").strip()
    
    if choice == "2":
        token = input("Paste your session token: ").strip()
        if not token:
            print("❌ No token provided.")
            return
        mm = MonarchMoney(token=token)
        save_token(token)
        print("✅ Token saved! Testing connection...")
        try:
            accounts = await mm.get_accounts()
            count = len(accounts.get("accounts", []))
            print(f"✅ Connected! Found {count} accounts.")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
        return
    
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    
    mm = MonarchMoney()
    try:
        await mm.login(email, password, use_saved_session=False, save_session=False)
        print("✅ Login successful!")
    except Exception as e:
        if "MFA" in str(type(e).__name__) or "mfa" in str(e).lower():
            mfa_code = input("🔐 Enter 2FA code: ").strip()
            await mm.multi_factor_authenticate(email, password, mfa_code)
            print("✅ MFA authentication successful!")
        else:
            print(f"❌ Login failed: {e}")
            return
    
    if mm.token:
        save_token(mm.token)
    
    # Test
    try:
        accounts = await mm.get_accounts()
        count = len(accounts.get("accounts", []))
        print(f"✅ Connected! Found {count} accounts.")
    except Exception as e:
        print(f"⚠️ Login saved but test failed: {e}")


async def get_client() -> MonarchMoney:
    """Get authenticated client."""
    token = load_token()
    if not token:
        print("❌ Not logged in. Run: python3 monarch_finance_helper.py --login")
        sys.exit(1)
    return MonarchMoney(token=token)


async def show_accounts():
    """Display all accounts with balances."""
    mm = await get_client()
    data = await mm.get_accounts()
    accounts = data.get("accounts", [])
    
    print("\n📊 YOUR ACCOUNTS")
    print("=" * 60)
    
    # Group by type
    by_type = {}
    for acct in accounts:
        atype = acct.get("type", {}).get("display", "Other")
        if atype not in by_type:
            by_type[atype] = []
        by_type[atype].append(acct)
    
    total_assets = 0
    total_liabilities = 0
    
    for atype, accts in sorted(by_type.items()):
        print(f"\n  {'─' * 50}")
        print(f"  📁 {atype.upper()}")
        print(f"  {'─' * 50}")
        for acct in accts:
            name = acct.get("displayName", "Unknown")
            balance = acct.get("currentBalance", 0)
            institution = acct.get("credential", {}).get("institution", {}).get("name", "")
            
            # Determine if asset or liability
            is_liability = atype.lower() in ["credit cards", "loans", "credit card"]
            if is_liability:
                total_liabilities += abs(balance)
                print(f"    💳 {name:<30} ${balance:>12,.2f}  ({institution})")
            else:
                total_assets += balance
                print(f"    🏦 {name:<30} ${balance:>12,.2f}  ({institution})")
    
    print(f"\n  {'═' * 50}")
    print(f"  💰 Total Assets:       ${total_assets:>12,.2f}")
    print(f"  💳 Total Liabilities:  ${total_liabilities:>12,.2f}")
    print(f"  📈 Net Worth:          ${total_assets - total_liabilities:>12,.2f}")
    print(f"  {'═' * 50}")


async def show_cashflow():
    """Display cash flow for current and previous month."""
    mm = await get_client()
    
    today = datetime.now()
    start_of_month = today.replace(day=1)
    start_of_last_month = (start_of_month - timedelta(days=1)).replace(day=1)
    
    print("\n💸 CASH FLOW ANALYSIS")
    print("=" * 60)
    
    # Current month
    try:
        cf = await mm.get_cashflow(
            start_date=start_of_month.strftime("%Y-%m-%d"),
            end_date=today.strftime("%Y-%m-%d")
        )
        if cf:
            print(f"\n  📅 This Month ({start_of_month.strftime('%B %Y')})")
            print(f"  {'─' * 50}")
            # Parse cashflow data
            summary = cf.get("summary", [])
            for item in summary:
                category = item.get("groupBy", {}).get("category", {}).get("name", "Unknown")
                total = item.get("summary", {}).get("sum", 0)
                print(f"    {category:<30} ${total:>10,.2f}")
    except Exception as e:
        print(f"  ⚠️ Could not fetch current month cashflow: {e}")
    
    # Previous month
    try:
        cf_prev = await mm.get_cashflow(
            start_date=start_of_last_month.strftime("%Y-%m-%d"),
            end_date=(start_of_month - timedelta(days=1)).strftime("%Y-%m-%d")
        )
        if cf_prev:
            print(f"\n  📅 Last Month ({start_of_last_month.strftime('%B %Y')})")
            print(f"  {'─' * 50}")
            summary = cf_prev.get("summary", [])
            for item in summary:
                category = item.get("groupBy", {}).get("category", {}).get("name", "Unknown")
                total = item.get("summary", {}).get("sum", 0)
                print(f"    {category:<30} ${total:>10,.2f}")
    except Exception as e:
        print(f"  ⚠️ Could not fetch last month cashflow: {e}")


async def show_recurring():
    """Display recurring transactions (bills and subscriptions)."""
    mm = await get_client()
    
    print("\n🔄 RECURRING TRANSACTIONS")
    print("=" * 60)
    
    try:
        recurring = await mm.get_recurring_transactions()
        items = recurring if isinstance(recurring, list) else recurring.get("recurringTransactions", [])
        
        total_monthly = 0
        
        for item in items:
            name = item.get("title", item.get("merchant", {}).get("name", "Unknown"))
            amount = item.get("amount", 0)
            frequency = item.get("frequency", "monthly")
            next_date = item.get("nextExpectedDate", "Unknown")
            
            total_monthly += abs(amount)
            print(f"    {'📌' if abs(amount) > 100 else '  '} {name:<35} ${abs(amount):>8,.2f}  ({frequency}) Next: {next_date}")
        
        print(f"\n  {'═' * 50}")
        print(f"  📊 Total Monthly Recurring: ${total_monthly:>10,.2f}")
        print(f"  {'═' * 50}")
    except Exception as e:
        print(f"  ⚠️ Could not fetch recurring transactions: {e}")


async def show_budgets():
    """Display budget status."""
    mm = await get_client()
    
    today = datetime.now()
    start_of_month = today.replace(day=1)
    
    print("\n📋 BUDGET STATUS")
    print("=" * 60)
    
    try:
        budgets = await mm.get_budgets(
            start_date=start_of_month.strftime("%Y-%m-%d"),
            end_date=today.strftime("%Y-%m-%d")
        )
        
        if budgets:
            items = budgets if isinstance(budgets, list) else budgets.get("budgetData", [])
            
            days_in_month = 30
            day_of_month = today.day
            pct_elapsed = (day_of_month / days_in_month) * 100
            
            print(f"  📅 Month Progress: {pct_elapsed:.0f}% elapsed")
            print(f"  {'─' * 50}")
            
            for item in items:
                category = item.get("category", {}).get("name", "Unknown")
                budgeted = item.get("budgetAmount", 0)
                spent = abs(item.get("actualAmount", item.get("spent", 0)))
                
                if budgeted > 0:
                    pct_spent = (spent / budgeted) * 100
                    status = "🟢" if pct_spent <= pct_elapsed else "🟡" if pct_spent <= 100 else "🔴"
                    print(f"    {status} {category:<25} ${spent:>8,.2f} / ${budgeted:>8,.2f}  ({pct_spent:.0f}%)")
            
            print(f"\n  Legend: 🟢 On track | 🟡 Pacing fast | 🔴 Over budget")
    except Exception as e:
        print(f"  ⚠️ Could not fetch budgets: {e}")


async def show_debts():
    """Display debt summary with payoff projections."""
    mm = await get_client()
    data = await mm.get_accounts()
    accounts = data.get("accounts", [])
    
    print("\n⚔️ DEBT SUMMARY")
    print("=" * 60)
    
    debts = []
    for acct in accounts:
        atype = acct.get("type", {}).get("display", "").lower()
        if any(x in atype for x in ["credit", "loan", "debt"]):
            debts.append({
                "name": acct.get("displayName", "Unknown"),
                "balance": abs(acct.get("currentBalance", 0)),
                "type": acct.get("type", {}).get("display", "Unknown"),
                "institution": acct.get("credential", {}).get("institution", {}).get("name", ""),
            })
    
    if not debts:
        print("  🎉 No debt accounts found!")
        return
    
    # Sort by balance (snowball) 
    debts_snowball = sorted(debts, key=lambda x: x["balance"])
    # Sort by type for display
    
    total_debt = sum(d["balance"] for d in debts)
    
    print(f"\n  📊 Total Debt: ${total_debt:,.2f}")
    print(f"  {'─' * 50}")
    print(f"\n  🎯 SNOWBALL ORDER (smallest balance first):")
    print(f"  {'─' * 50}")
    
    for i, d in enumerate(debts_snowball, 1):
        marker = "👊" if i == 1 else "  "
        print(f"    {marker} #{i} {d['name']:<30} ${d['balance']:>10,.2f}  ({d['institution']})")
    
    print(f"\n  {'─' * 50}")
    print(f"  👊 = Attack this one first (Snowball Method)")
    print(f"  {'═' * 50}")


async def full_audit():
    """Run all reports."""
    await show_accounts()
    await show_debts()
    await show_recurring()
    await show_budgets()
    await show_cashflow()
    
    print("\n" + "=" * 60)
    print("  🏁 FULL AUDIT COMPLETE")
    print("=" * 60)


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "--login":
        await login()
    elif cmd == "--accounts":
        await show_accounts()
    elif cmd == "--cashflow":
        await show_cashflow()
    elif cmd == "--recurring":
        await show_recurring()
    elif cmd == "--budgets":
        await show_budgets()
    elif cmd == "--debts":
        await show_debts()
    elif cmd == "--full-audit":
        await full_audit()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    asyncio.run(main())
