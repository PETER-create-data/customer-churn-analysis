-- Expected: 390, 5, 6, 13.
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT institutional_sector) AS sectors,
       COUNT(DISTINCT transaction_type) AS transaction_types,
       COUNT(DISTINCT period) AS periods
FROM public.financial_data;

-- Expected: 156 and 78. Do not substitute zeros for missing values.
SELECT COUNT(*) FILTER (WHERE liabilities_currency_deposits IS NULL) AS missing_deposits,
       COUNT(*) FILTER (WHERE liabilities_equity_investment_funds IS NULL) AS missing_equity
FROM public.financial_data;

-- Expected: no duplicate groups.
SELECT institutional_sector, consolidation, transaction_type, period, COUNT(*)
FROM public.financial_data
GROUP BY institutional_sector, consolidation, transaction_type, period
HAVING COUNT(*) > 1;
