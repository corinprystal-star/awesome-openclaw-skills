#!/usr/bin/env python3
"""
Corin's Cash Flow Forecast
============================
Predicts your checking account balance for the next 30 days
based on known recurring bills and income.

Edit the INCOME and BILLS sections below with your actual numbers.
"""

from datetime import datetime, timedelta

# ============================================================
# YOUR INCOME (Edit these)
# ============================================================
INCOME = [
    # {"name": "Paycheck", "amount": 3500, "day_of_month": 1},
    # {"name": "Paycheck", "amount": 3500, "day_of_month": 15},
    # {"name": "Side Gig", "amount": 500, "day_of_month": 20},
]

# ============================================================
# YOUR RECURRING BILLS (Edit these)
# ============================================================
BILLS = [
    # {"name": "Rent", "amount": -1800, "day_of_month": 1},
    # {"name": "Car Payment", "amount": -350, "day_of_month": 5},
    # {"name": "Car Insurance", "amount": -180, "day_of_month": 7},
    # {"name": "Phone", "amount": -85, "day_of_month": 10},
    # {"name": "Internet", "amount": -75, "day_of_month": 12},
    # {"name": "Electricity", "amount": -120, "day_of_month": 15},
    # {"name": "Netflix", "amount": -15.49, "day_of_month": 16},
    # {"name": "Spotify", "amount": -10.99, "day_of_month": 18},
    # {"name": "Gym", "amount": -30, "day_of_month": 20},
    # {"name": "Credit Card Min", "amount": -150, "day_of_month": 25},
    # {"name": "Student Loan", "amount": -250, "day_of_month": 28},
]

# ============================================================
# STARTING BALANCE (Today's checking balance)
# ============================================================
STARTING_BALANCE = 0  # Set to your current checking balance

# Daily variable spending estimate (groceries, gas, food, etc.)
DAILY_VARIABLE_SPEND = 0  # Estimate your average daily spending


def forecast(starting_balance, income, bills, daily_spend, days=30):
    """Generate a 30-day cash flow forecast."""
    today = datetime.now()
    balance = starting_balance
    forecast_data = []
    
    # Combine income and bills
    all_events = []
    for item in income:
        all_events.append({**item, "type": "income"})
    for item in bills:
        all_events.append({**item, "type": "bill"})
    
    min_balance = balance
    min_balance_date = today
    danger_days = []
    
    for day_offset in range(days):
        date = today + timedelta(days=day_offset)
        day_of_month = date.day
        day_events = []
        
        # Check for events on this day
        for event in all_events:
            if event["day_of_month"] == day_of_month:
                balance += event["amount"]
                day_events.append(event)
        
        # Apply daily variable spending
        if day_offset > 0:  # Don't deduct for today (already spent or not)
            balance -= daily_spend
        
        # Track minimums
        if balance < min_balance:
            min_balance = balance
            min_balance_date = date
        
        # Track danger days
        if balance < 0:
            danger_days.append(date)
        
        forecast_data.append({
            "date": date,
            "balance": balance,
            "events": day_events
        })
    
    return forecast_data, min_balance, min_balance_date, danger_days


def print_forecast(forecast_data, min_balance, min_balance_date, danger_days):
    """Print the forecast in a scannable format."""
    
    print(f"\n{'═' * 65}")
    print(f"  📅 30-DAY CASH FLOW FORECAST")
    print(f"{'═' * 65}")
    
    if danger_days:
        print(f"\n  🚨 WARNING: NEGATIVE BALANCE ON {len(danger_days)} DAY(S)!")
        for d in danger_days[:5]:
            print(f"     ❌ {d.strftime('%a %b %d')}")
        print()
    
    print(f"  💰 Starting Balance: ${forecast_data[0]['balance']:,.2f}")
    print(f"  📉 Lowest Point:     ${min_balance:,.2f} on {min_balance_date.strftime('%a %b %d')}")
    print(f"  📊 Ending Balance:   ${forecast_data[-1]['balance']:,.2f}")
    
    print(f"\n{'─' * 65}")
    print(f"  {'Date':<12} {'Balance':>10}  {'Events'}")
    print(f"  {'─' * 60}")
    
    for day in forecast_data:
        date_str = day["date"].strftime("%a %b %d")
        balance = day["balance"]
        
        # Color coding via emoji
        if balance < 0:
            indicator = "🔴"
        elif balance < 200:
            indicator = "🟡"
        else:
            indicator = "🟢"
        
        events_str = ""
        for e in day["events"]:
            if e["type"] == "income":
                events_str += f" 💚 +${e['amount']:,.2f} ({e['name']})"
            else:
                events_str += f" 💸 ${e['amount']:,.2f} ({e['name']})"
        
        # Only print days with events or weekly markers
        if day["events"] or day["date"].weekday() == 0 or day == forecast_data[0]:
            print(f"  {indicator} {date_str:<12} ${balance:>9,.2f} {events_str}")
    
    print(f"\n{'═' * 65}")
    
    # Actionable insights
    print(f"\n  💡 INSIGHTS:")
    if danger_days:
        first_danger = danger_days[0]
        days_until = (first_danger - datetime.now()).days
        print(f"     ⚠️  You'll go negative in {days_until} days ({first_danger.strftime('%b %d')})")
        print(f"     → Move money, defer a bill, or find income before then.")
    
    if min_balance < 500 and min_balance > 0:
        print(f"     ⚠️  Your balance dips to ${min_balance:,.2f} — dangerously thin.")
        print(f"     → One unexpected expense could overdraft you.")
    
    total_income = sum(e["amount"] for e in forecast_data[0]["events"] if any(ev["type"] == "income" for ev in [e] if "type" in e))
    print(f"\n{'═' * 65}")


def main():
    if not INCOME and not BILLS:
        print("\n⚠️  No income or bills configured!")
        print("    Edit the INCOME and BILLS sections at the top of this file.")
        print("    Or connect to Monarch Money to auto-populate.")
        print("\n    Running with example data...\n")
        
        # Example data for demonstration
        example_income = [
            {"name": "Paycheck", "amount": 3500, "day_of_month": 1},
            {"name": "Paycheck", "amount": 3500, "day_of_month": 15},
        ]
        example_bills = [
            {"name": "Rent", "amount": -1800, "day_of_month": 1},
            {"name": "Car Payment", "amount": -350, "day_of_month": 5},
            {"name": "Car Insurance", "amount": -180, "day_of_month": 7},
            {"name": "Phone", "amount": -85, "day_of_month": 10},
            {"name": "Internet", "amount": -75, "day_of_month": 12},
            {"name": "Electricity", "amount": -120, "day_of_month": 15},
            {"name": "Netflix", "amount": -15.49, "day_of_month": 16},
            {"name": "Spotify", "amount": -10.99, "day_of_month": 18},
            {"name": "Credit Card Min", "amount": -150, "day_of_month": 25},
            {"name": "Student Loan", "amount": -250, "day_of_month": 28},
        ]
        
        data, min_bal, min_date, danger = forecast(
            starting_balance=2800,
            income=example_income,
            bills=example_bills,
            daily_spend=45,
            days=30
        )
        print_forecast(data, min_bal, min_date, danger)
        return
    
    data, min_bal, min_date, danger = forecast(
        starting_balance=STARTING_BALANCE,
        income=INCOME,
        bills=BILLS,
        daily_spend=DAILY_VARIABLE_SPEND,
        days=30
    )
    print_forecast(data, min_bal, min_date, danger)


if __name__ == "__main__":
    main()
