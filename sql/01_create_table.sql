-- For a NEW database. Existing tables are left unchanged.
-- Amounts are in million euros; missing numeric cells are NULL.
CREATE TABLE IF NOT EXISTS public.financial_data (
    institutional_sector VARCHAR(100) NOT NULL,
    consolidation VARCHAR(50) NOT NULL,
    transaction_type VARCHAR(100) NOT NULL,
    period VARCHAR(50) NOT NULL,
    assets_total BIGINT,
    assets_currency_deposits BIGINT,
    assets_debt_securities BIGINT,
    assets_loans_total BIGINT,
    assets_short_term_loans BIGINT,
    assets_long_term_loans BIGINT,
    assets_equity_investment_funds BIGINT,
    liabilities_total BIGINT,
    liabilities_currency_deposits BIGINT,
    liabilities_debt_securities BIGINT,
    liabilities_loans_total BIGINT,
    liabilities_short_term_loans BIGINT,
    liabilities_long_term_loans BIGINT,
    liabilities_equity_investment_funds BIGINT,
    net_worth BIGINT,
    UNIQUE (institutional_sector, consolidation, transaction_type, period)
);
