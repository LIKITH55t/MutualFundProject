-- 1. Top 5 funds by AUM
SELECT 
    fund_house,
    SUM(aum_crore) AS total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC
LIMIT 5;


-- 2. Average NAV per month
SELECT 
    strftime('%Y-%m', date) AS month,
    AVG(nav) AS average_nav
FROM fact_nav
GROUP BY month
ORDER BY month;


-- 3. SIP YoY growth
SELECT 
    strftime('%Y', month) AS year,
    AVG(yoy_growth_pct) AS average_yoy_growth_pct
FROM monthly_sip_inflows
GROUP BY year
ORDER BY year;


-- 4. Transactions by state
SELECT 
    state,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;


-- 5. Funds with expense ratio below 1%
SELECT 
    amfi_code,
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;


-- 6. Top 5 funds by 3-year return
SELECT 
    amfi_code,
    scheme_name,
    return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;


-- 7. Top 5 funds by Sharpe Ratio
SELECT 
    amfi_code,
    scheme_name,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;


-- 8. Funds with worst maximum drawdown
SELECT 
    amfi_code,
    scheme_name,
    max_drawdown_pct
FROM fact_performance
ORDER BY max_drawdown_pct ASC
LIMIT 5;


-- 9. Transaction type analysis
SELECT 
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount_inr,
    AVG(amount_inr) AS average_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;


-- 10. Fund performance comparison
SELECT 
    f.amfi_code,
    f.scheme_name,
    f.category,
    p.return_1yr_pct,
    p.return_3yr_pct,
    p.sharpe_ratio,
    p.sortino_ratio,
    p.alpha,
    p.beta,
    p.max_drawdown_pct
FROM dim_fund f
JOIN fact_performance p
    ON f.amfi_code = p.amfi_code
ORDER BY p.return_3yr_pct DESC;