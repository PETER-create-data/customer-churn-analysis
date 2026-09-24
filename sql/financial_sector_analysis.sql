-- Dutch Financial Sector Analysis
-- Source: CBS
-- Original amounts are in millions of euros.


-- ANALYSIS 1: Compare sectors at year-end 2025
-- Results are expressed in billions of euros.
-- Exclude the aggregate to avoid mixing it with individual sectors.

SELECT
    institutional_sector,
    ROUND(assets_total / 1000.0, 2) AS assets_billion_eur,
    ROUND(liabilities_total / 1000.0, 2) AS liabilities_billion_eur,
    ROUND(net_worth / 1000.0, 2) AS net_worth_billion_eur
FROM public.financial_data
WHERE transaction_type = 'Closing balance sheet'
  AND period = '2025*'
  AND institutional_sector <> 'Total domestic sectors'
ORDER BY assets_total DESC;


-- ANALYSIS 2: Annual financial-corporation asset growth
-- Annual observations only, covering 2015–2025.
-- The first year's growth is NULL because 2014 is unavailable.

WITH annual_assets AS (
    SELECT
        REPLACE(period, '*', '')::integer AS year,
        assets_total
    FROM public.financial_data
    WHERE institutional_sector = 'Financial corporations'
      AND transaction_type = 'Closing balance sheet'
      AND period NOT LIKE '%quarter%'
),
previous_year AS (
    SELECT
        year,
        assets_total,
        LAG(assets_total) OVER (ORDER BY year) AS previous_assets
    FROM annual_assets
)
SELECT
    year,
    ROUND(assets_total / 1000.0, 2) AS assets_billion_eur,
    ROUND(
        100.0 * (assets_total - previous_assets)
        / NULLIF(previous_assets, 0),
        2
    ) AS annual_growth_percent
FROM previous_year
ORDER BY year;  


-- CHECK 1: Find duplicate observations.
-- Expected result: zero rows.

SELECT
    institutional_sector,
    consolidation,
    transaction_type,
    period,
    COUNT(*) AS occurrences
FROM public.financial_data
GROUP BY
    institutional_sector,
    consolidation,
    transaction_type,
    period
HAVING COUNT(*) > 1;


-- CHECK 2: Confirm missing values were preserved.
-- Expected: 390 rows, 156 missing deposits, 78 missing equity values.

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (
        WHERE liabilities_currency_deposits IS NULL
    ) AS missing_liabilities_deposits,
    COUNT(*) FILTER (
        WHERE liabilities_equity_investment_funds IS NULL
    ) AS missing_liabilities_equity
FROM public.financial_data;

-- ANALYSIS 3: Selected assets as a percentage of total assets.
-- Year-end 2025, individual sectors only.
-- These categories do not cover every asset in the CBS dataset.

SELECT
    institutional_sector,
    ROUND(
        100.0 * assets_currency_deposits
        / NULLIF(assets_total, 0), 2
    ) AS deposits_pct,
    ROUND(
        100.0 * assets_debt_securities
        / NULLIF(assets_total, 0), 2
    ) AS debt_securities_pct,
    ROUND(
        100.0 * assets_loans_total
        / NULLIF(assets_total, 0), 2
    ) AS loans_pct,
    ROUND(
        100.0 * assets_equity_investment_funds
        / NULLIF(assets_total, 0), 2
    ) AS equity_and_funds_pct
FROM public.financial_data
WHERE transaction_type = 'Closing balance sheet'
  AND period = '2025*'
  AND institutional_sector <> 'Total domestic sectors'
ORDER BY institutional_sector;

-- ANALYSIS 4: Reconcile financial-corporation assets in 2025.
-- Amounts remain in millions of euros.
-- Other changes already includes revaluations and volume changes:
-- do not add those subcategories again.

WITH balances AS (
    SELECT
        MAX(assets_total) FILTER (
            WHERE transaction_type = 'Opening balance sheet'
        ) AS opening_assets,
        MAX(assets_total) FILTER (
            WHERE transaction_type = 'Financial transactions'
        ) AS transactions,
        MAX(assets_total) FILTER (
            WHERE transaction_type = 'Other changes'
        ) AS other_changes,
        MAX(assets_total) FILTER (
            WHERE transaction_type = 'Closing balance sheet'
        ) AS closing_assets
    FROM public.financial_data
    WHERE institutional_sector = 'Financial corporations'
      AND period = '2025*'
)
SELECT
    opening_assets,
    transactions,
    other_changes,
    closing_assets,
    closing_assets - opening_assets AS total_change,
    closing_assets
        - opening_assets
        - transactions
        - other_changes AS reconciliation_difference
FROM balances;        year,
        assets_total,
        LAG(assets_total) OVER (ORDER BY year) AS previous_assets
    FROM annual_assets
)
SELECT
    year,
    ROUND(assets_total / 1000.0, 2) AS assets_billion_eur,
    ROUND(
        100.0 * (assets_total - previous_assets)
        / NULLIF(previous_assets, 0),
        2
    ) AS annual_growth_percent
FROM previous_year
ORDER BY year;
