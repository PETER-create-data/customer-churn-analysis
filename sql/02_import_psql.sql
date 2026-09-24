-- Run with psql from the repository root, not the pgAdmin Query Tool.
\set ON_ERROR_STOP on
BEGIN;
LOCK TABLE public.financial_data IN EXCLUSIVE MODE;
DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM public.financial_data) THEN
        RAISE EXCEPTION 'Table is not empty. Import cancelled to avoid duplicates.';
    END IF;
END $$;
\copy public.financial_data FROM 'data/cbs_dutch_financial_clean.csv' WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8')
COMMIT;
