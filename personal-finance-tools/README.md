# Personal Finance Tools

A collection of scripts and templates for managing personal finances via Monarch Money.

## What's Included

| File | Purpose |
|------|---------|
| `monarch_finance_helper.py` | CLI tool to pull data from Monarch Money (accounts, cashflow, budgets, debts) |
| `debt_payoff_calculator.py` | Interactive debt payoff planner (Snowball + Avalanche comparison) |
| `cashflow_forecast.py` | 30-day cash flow prediction with danger-day warnings |
| `Corin_Finance_Playbook.md` | Complete personal finance framework and strategy |
| `Monarch_MCP_Connector_Guide.md` | How to set up Monarch Money as a Manus MCP connector |
| `templates/` | Weekly Money Date checklist, Subscription Audit template |
| `goals/` | SMART goal template for financial freedom |

## Quick Start

```bash
# 1. Login to Monarch Money
python3 monarch_finance_helper.py --login

# 2. Run a full financial audit
python3 monarch_finance_helper.py --full-audit

# 3. Plan your debt payoff
python3 debt_payoff_calculator.py

# 4. Forecast your cash flow
python3 cashflow_forecast.py
```

## Requirements

```bash
pip install monarchmoneycommunity
```

## Integration with Manus

See `Monarch_MCP_Connector_Guide.md` for setting up the Monarch Money MCP server
as a Custom MCP connector in Manus for automated financial briefings.
