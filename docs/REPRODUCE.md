REPRODUCE
Reproduce the Dutch Financial Sector Analysis
This workflow reproduces the supplied CBS export (390 observations, 87 source columns). It is snapshot-specific, not an automatic downloader. No database passwords belong in the repository.
1. Prepare Python
Use Python 3.12 or later. In Terminal, change into the downloaded/cloned repository folder. On macOS or Linux:
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python python/clean_cbs.py
python python/build_charts.py
​
On Windows, activate with .venv\Scripts\activate instead. Cleaning uses only Python's standard library; plotting requires the listed packages. Do not run scripts with -O, because that disables assertions.
The scripts locate files from their own repository location. Cleaning reads data/cbs_dutch_financial_raw.csv, writes data/cbs_dutch_financial_clean.csv and records header mappings, missing values, sample rows and a source checksum in reports/cbs_validation.json. Charts are written to charts/ as PNG and SVG. Reruns replace generated outputs, never the raw CSV.
2. Create a database and table
In pgAdmin, create a new database named dutch_financial_analysis if needed. Open its Query Tool and run sql/01_create_table.sql.
If you already imported the 390 rows, SKIP the import step. The setup script does not change an existing table or retrofit its constraints. New tables include a uniqueness constraint on the four observation dimensions.
3. Import once
pgAdmin
Right-click Schemas > public > Tables > financial_data, then choose Import/Export Data. Select Import and the cleaned CSV. Use CSV format, UTF8 encoding, Header enabled, comma delimiter, double quote for Quote and Escape, and an empty NULL String. Select all 19 columns in CSV order. Leave NOT NULL columns unselected. Confirm completion before continuing.
Alternative: psql
With PostgreSQL's psql command available, run from the repository root:
psql -h localhost -U postgres -d dutch_financial_analysis -v ON_ERROR_STOP=1 -f sql/01_create_table.sql
psql -h localhost -U postgres -d dutch_financial_analysis -f sql/02_import_psql.sql
psql -h localhost -U postgres -d dutch_financial_analysis -v ON_ERROR_STOP=1 -f sql/03_validate.sql
​
Enter your password when prompted. The import file contains a psql-only \copy command and cannot run in the pgAdmin Query Tool. It imports in a transaction and refuses to append to a nonempty table.
4. Validate and analyse
Run sql/03_validate.sql: expect 390 rows, 5 sectors, 6 transaction types and 13 periods. Expect 156 NULL deposit-liability values and 78 NULL equity-liability values, and zero duplicate groups. Then run the queries in the existing sql/financial_sector_analysis.sql, selecting one complete statement at a time in pgAdmin.
Definitions and limitations
Amounts are million euros; charts divide by 1,000 to display billion euros.
Preserve original sector names and period asterisks; verify asterisk definitions in CBS metadata before describing revision status.
Annual 2015–2025 observations and Q1/Q2 2026 observations have different frequencies. Do not combine them into an annual growth series.
Charts use closing balances. Do not sum opening/closing balances and flows together.
Other changes includes its revaluation and volume-change subcategories; do not add those subcategories again.
Data are not consolidated. Financial corporations are broader than banks, and financial assets do not include non-financial assets.
Missing numeric cells remain NULL. The source is preserved and its SHA-256 is checked before/after cleaning.
Add to the main README
Link to this guide using [Reproduce the analysis](docs/REPRODUCE.md). Keep the existing analysis, results and dashboard sections. The current dashboard is a static Python chart; an interactive dashboard remains future work.
