# Mutual Fund Analytics Platform — Data Dictionary

## 1. investor_transactions

| Column | Data Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor identifier |
| transaction_date | DATE | Date of transaction |
| amfi_code | INTEGER | AMFI scheme code |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption |
| amount_inr | REAL | Transaction amount in INR |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| city_tier | TEXT | City classification |
| age_group | TEXT | Investor age group |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income in lakh INR |
| payment_mode | TEXT | Mode used for payment |
| kyc_status | TEXT | KYC verification status |

## 2. portfolio_holdings

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | AMFI scheme code |
| stock_symbol | TEXT | Stock ticker symbol |
| stock_name | TEXT | Name of stock held |
| sector | TEXT | Stock sector |
| weight_pct | REAL | Portfolio weight percentage |
| market_value_cr | REAL | Market value in crore INR |
| current_price_inr | REAL | Current stock price in INR |
| portfolio_date | DATE | Portfolio holding date |

## 3. benchmark_indices

| Column | Data Type | Description |
|---|---|---|
| date | DATE | Index observation date |
| index_name | TEXT | Benchmark index name |
| close_value | REAL | Closing index value |

## 4. fund_master

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | Unique AMFI scheme code |
| fund_house | TEXT | Mutual fund house |
| scheme_name | TEXT | Mutual fund scheme name |
| category | TEXT | Fund category |
| sub_category | TEXT | Fund sub-category |
| plan | TEXT | Fund plan type |
| launch_date | DATE | Scheme launch date |
| benchmark | TEXT | Benchmark used by the scheme |
| expense_ratio_pct | REAL | Expense ratio percentage |
| exit_load_pct | REAL | Exit load percentage |
| min_sip_amount | REAL | Minimum SIP investment |
| min_lumpsum_amount | REAL | Minimum lumpsum investment |
| fund_manager | TEXT | Fund manager |
| risk_category | TEXT | Risk classification |
| sebi_category_code | TEXT | SEBI category code |

## 5. nav_history

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | AMFI scheme code |
| date | DATE | NAV date |
| nav | REAL | Net Asset Value |

## 6. aum_by_fund_house

| Column | Data Type | Description |
|---|---|---|
| date | DATE | AUM reporting date |
| fund_house | TEXT | Mutual fund house |
| aum_lakh_crore | REAL | AUM in lakh crore INR |
| aum_crore | REAL | AUM in crore INR |
| num_schemes | INTEGER | Number of schemes |

## 7. monthly_sip_inflows

| Column | Data Type | Description |
|---|---|---|
| month | DATE | Reporting month |
| sip_inflow_crore | REAL | SIP inflow in crore INR |
| active_sip_accounts_crore | REAL | Active SIP accounts in crore |
| new_sip_accounts_lakh | REAL | New SIP accounts in lakh |
| sip_aum_lakh_crore | REAL | SIP AUM in lakh crore INR |
| yoy_growth_pct | REAL | Year-over-year SIP growth percentage |

## 8. category_inflows

| Column | Data Type | Description |
|---|---|---|
| month | DATE | Reporting month |
| category | TEXT | Mutual fund category |
| net_inflow_crore | REAL | Net inflow in crore INR |

## 9. industry_folio_count

| Column | Data Type | Description |
|---|---|---|
| month | DATE | Reporting month |
| total_folios_crore | REAL | Total folios in crore |
| equity_folios_crore | REAL | Equity folios in crore |
| debt_folios_crore | REAL | Debt folios in crore |
| hybrid_folios_crore | REAL | Hybrid folios in crore |
| others_folios_crore | REAL | Other folios in crore |

## 10. scheme_performance

| Column | Data Type | Description |
|---|---|---|
| amfi_code | INTEGER | AMFI scheme code |
| scheme_name | TEXT | Mutual fund scheme name |
| fund_house | TEXT | Mutual fund house |
| category | TEXT | Fund category |
| plan | TEXT | Fund plan |
| return_1yr_pct | REAL | 1-year return percentage |
| return_3yr_pct | REAL | 3-year return percentage |
| return_5yr_pct | REAL | 5-year return percentage |
| benchmark_3yr_pct | REAL | 3-year benchmark return |
| alpha | REAL | Alpha relative to benchmark |
| beta | REAL | Beta relative to benchmark |
| sharpe_ratio | REAL | Risk-adjusted return using Sharpe ratio |
| sortino_ratio | REAL | Downside-risk-adjusted return |
| std_dev_ann_pct | REAL | Annualized standard deviation |
| max_drawdown_pct | REAL | Maximum portfolio decline |
| aum_crore | REAL | Assets under management in crore INR |
| expense_ratio_pct | REAL | Expense ratio percentage |
| morningstar_rating | REAL | Fund rating |
| risk_grade | TEXT | Risk grade |

---

# Database Schema

The SQLite database `bluestock_mf.db` contains:

- `dim_fund` — fund master dimension
- `dim_date` — date dimension
- `fact_nav` — historical NAV data
- `fact_transactions` — investor transactions
- `fact_performance` — scheme performance metrics
- `fact_aum` — fund-house AUM
- `portfolio_holdings` — portfolio holdings
- `benchmark_indices` — benchmark index data
- `monthly_sip_inflows` — monthly SIP data
- `category_inflows` — category-level inflows
- `industry_folio_count` — industry folio statistics

## Data Sources

The datasets used in this project are based on the provided mutual fund datasets and publicly available mutual fund market data.

## Data Cleaning

The datasets were cleaned by:

- Parsing date fields into standard date format
- Converting numeric columns to appropriate numeric types
- Removing duplicate records
- Validating positive NAV values
- Standardizing transaction types
- Validating transaction amounts
- Checking expense-ratio ranges
- Handling missing NAV values using forward filling
- Identifying potential data anomalies