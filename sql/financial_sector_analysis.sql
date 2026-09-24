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
