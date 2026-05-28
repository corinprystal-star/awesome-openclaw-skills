#!/usr/bin/env python3
"""
Corin's Debt Payoff Calculator
================================
Generates a debt payoff plan using Snowball or Avalanche method.
Outputs a visual timeline and monthly payment schedule.

Usage:
    python3 debt_payoff_calculator.py

You'll be prompted to enter your debts. Or edit the DEBTS list below.
"""

import sys
from datetime import datetime, timedelta
from copy import deepcopy

# ============================================================
# EDIT YOUR DEBTS HERE (or enter interactively)
# ============================================================
# Format: {"name": str, "balance": float, "min_payment": float, "apr": float}
DEBTS = [
    # Example debts - REPLACE WITH YOUR ACTUAL NUMBERS
    # {"name": "Capital One CC", "balance": 3200, "min_payment": 85, "apr": 24.99},
    # {"name": "Chase Sapphire", "balance": 7500, "min_payment": 150, "apr": 21.49},
    # {"name": "Student Loan", "balance": 15000, "min_payment": 250, "apr": 5.5},
    # {"name": "Car Loan", "balance": 12000, "min_payment": 350, "apr": 6.9},
]

# How much EXTRA can you throw at debt each month (beyond all minimums)?
EXTRA_MONTHLY = 0  # Set this to your extra payment amount


def calculate_payoff(debts, extra_monthly, method="snowball"):
    """
    Calculate debt payoff schedule.
    
    method: "snowball" (smallest balance first) or "avalanche" (highest APR first)
    """
    debts = deepcopy(debts)
    
    if method == "snowball":
        debts.sort(key=lambda d: d["balance"])
    else:  # avalanche
        debts.sort(key=lambda d: d["apr"], reverse=True)
    
    total_paid = 0
    total_interest = 0
    months = 0
    schedule = []
    
    while any(d["balance"] > 0 for d in debts):
        months += 1
        month_data = {"month": months, "payments": [], "total_balance": 0}
        
        # Calculate interest for all debts
        for d in debts:
            if d["balance"] > 0:
                monthly_interest = d["balance"] * (d["apr"] / 100 / 12)
                d["balance"] += monthly_interest
                total_interest += monthly_interest
        
        # Pay minimums on all debts
        extra_available = extra_monthly
        for d in debts:
            if d["balance"] > 0:
                payment = min(d["min_payment"], d["balance"])
                d["balance"] -= payment
                total_paid += payment
                month_data["payments"].append({
                    "name": d["name"],
                    "payment": payment,
                    "remaining": d["balance"]
                })
        
        # Apply extra to target debt (first in sorted order with balance > 0)
        for d in debts:
            if d["balance"] > 0 and extra_available > 0:
                extra_payment = min(extra_available, d["balance"])
                d["balance"] -= extra_payment
                extra_available -= extra_payment
                total_paid += extra_payment
                # Update the payment record
                for p in month_data["payments"]:
                    if p["name"] == d["name"]:
                        p["payment"] += extra_payment
                        p["remaining"] = d["balance"]
                break  # Only apply extra to the target debt
        
        month_data["total_balance"] = sum(d["balance"] for d in debts if d["balance"] > 0)
        schedule.append(month_data)
        
        # Safety valve
        if months > 600:  # 50 years max
            break
    
    return {
        "months": months,
        "total_paid": total_paid,
        "total_interest": total_interest,
        "schedule": schedule,
        "method": method
    }


def print_summary(result, debts):
    """Print a clean summary of the payoff plan."""
    total_debt = sum(d["balance"] for d in debts)
    years = result["months"] // 12
    remaining_months = result["months"] % 12
    
    method_name = "SNOWBALL" if result["method"] == "snowball" else "AVALANCHE"
    
    print(f"\n{'═' * 60}")
    print(f"  ⚔️  DEBT PAYOFF PLAN — {method_name} METHOD")
    print(f"{'═' * 60}")
    print(f"\n  📊 Starting Total Debt:    ${total_debt:>12,.2f}")
    print(f"  💰 Total You'll Pay:       ${result['total_paid']:>12,.2f}")
    print(f"  🔥 Total Interest Paid:    ${result['total_interest']:>12,.2f}")
    print(f"  📅 Debt-Free In:           {years} years, {remaining_months} months")
    print(f"  🗓️  Debt-Free Date:         {(datetime.now() + timedelta(days=result['months']*30)).strftime('%B %Y')}")
    print(f"\n{'─' * 60}")
    
    # Show order of attack
    if result["method"] == "snowball":
        sorted_debts = sorted(debts, key=lambda d: d["balance"])
    else:
        sorted_debts = sorted(debts, key=lambda d: d["apr"], reverse=True)
    
    print(f"\n  🎯 ORDER OF ATTACK:")
    for i, d in enumerate(sorted_debts, 1):
        print(f"    #{i} {d['name']:<25} ${d['balance']:>10,.2f}  ({d['apr']}% APR)")
    
    # Show first 6 months
    print(f"\n{'─' * 60}")
    print(f"  📅 FIRST 6 MONTHS PREVIEW:")
    print(f"{'─' * 60}")
    for month in result["schedule"][:6]:
        print(f"\n    Month {month['month']}  (Remaining: ${month['total_balance']:,.2f})")
        for p in month["payments"]:
            if p["payment"] > 0:
                status = "✅ PAID OFF!" if p["remaining"] <= 0.01 else f"${p['remaining']:,.2f} left"
                print(f"      → {p['name']:<25} Pay: ${p['payment']:>8,.2f}  ({status})")


def interactive_input():
    """Get debt info interactively."""
    print("\n📝 ENTER YOUR DEBTS")
    print("=" * 40)
    print("(Type 'done' when finished)\n")
    
    debts = []
    i = 1
    while True:
        print(f"\n  Debt #{i}:")
        name = input("    Name (e.g., Chase CC): ").strip()
        if name.lower() == "done":
            break
        
        try:
            balance = float(input("    Current Balance: $").strip().replace(",", ""))
            min_payment = float(input("    Minimum Payment: $").strip().replace(",", ""))
            apr = float(input("    APR (%): ").strip().replace("%", ""))
        except ValueError:
            print("    ❌ Invalid number. Try again.")
            continue
        
        debts.append({
            "name": name,
            "balance": balance,
            "min_payment": min_payment,
            "apr": apr
        })
        i += 1
    
    if not debts:
        print("No debts entered.")
        return None, 0
    
    try:
        extra = float(input("\n  💪 Extra monthly payment (beyond all minimums): $").strip().replace(",", ""))
    except ValueError:
        extra = 0
    
    return debts, extra


def main():
    global DEBTS, EXTRA_MONTHLY
    
    if not DEBTS:
        debts, extra = interactive_input()
        if not debts:
            return
    else:
        debts = DEBTS
        extra = EXTRA_MONTHLY
    
    # Calculate both methods
    snowball = calculate_payoff(debts, extra, "snowball")
    avalanche = calculate_payoff(debts, extra, "avalanche")
    
    # Print both
    print_summary(snowball, debts)
    print_summary(avalanche, debts)
    
    # Comparison
    interest_diff = snowball["total_interest"] - avalanche["total_interest"]
    month_diff = snowball["months"] - avalanche["months"]
    
    print(f"\n{'═' * 60}")
    print(f"  🆚 COMPARISON")
    print(f"{'═' * 60}")
    print(f"\n  Avalanche saves you: ${abs(interest_diff):,.2f} in interest")
    print(f"  Avalanche is faster by: {abs(month_diff)} months")
    print(f"\n  💡 RECOMMENDATION FOR ADHD BRAIN:")
    if interest_diff < 200:
        print(f"     Go SNOWBALL. The interest difference is tiny (${interest_diff:,.2f}),")
        print(f"     and the dopamine hit of closing accounts will keep you going.")
    else:
        print(f"     Avalanche saves ${interest_diff:,.2f} — that's real money.")
        print(f"     BUT if you struggle with motivation, Snowball's quick wins matter more.")
        print(f"     Pick the one you'll actually stick with.")
    print(f"\n{'═' * 60}")


if __name__ == "__main__":
    main()
