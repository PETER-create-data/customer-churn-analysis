import csv, hashlib, io, json, re
from pathlib import Path

# Paths are relative to this repository, not the terminal working directory.
ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'data/cbs_dutch_financial_raw.csv'
out = ROOT / 'data/cbs_dutch_financial_clean.csv'
if not __debug__:
    raise RuntimeError('Run without -O: validation assertions must remain enabled.')
if source.resolve() == out.resolve():
    raise ValueError('Source and output paths must differ.')
raw = source.read_bytes()
digest = hashlib.sha256(raw).hexdigest()
rows = list(csv.reader(io.StringIO(raw.decode('utf-8-sig')), delimiter=';'))
headers = rows[0]
mapping = [
 ('institutional_sector', 'Institutional sectors'),
 ('consolidation', 'Not Consolidated or Consolidated'),
 ('transaction_type', 'Balance sheets and transactions'),
 ('period', 'Periods'),
]
for side in ['Assets', 'Liabilities']:
    for target, topic in [
        ('total', 'Totaal' if side == 'Liabilities' else 'Total'),
        ('currency_deposits', 'Currency and deposits/Total'),
        ('debt_securities', 'Debt securities/Total'),
        ('loans_total', 'Loans/Total'),
        ('short_term_loans', 'Loans/Short-term loans'),
        ('long_term_loans', 'Loans/Long-term loans'),
        ('equity_investment_funds', 'Equity and investment fund shares/Total'),
    ]:
        mapping.append((side.lower()+'_'+target, side+'/'+topic+' (million euros)'))
mapping.append(('net_worth', 'Net worth (million euros)'))
assert len(headers) == 87 and len(mapping) == 19
assert all(headers.count(h) == 1 for _, h in mapping)
indices = [headers.index(h) for _, h in mapping]
clean, excluded = [], []
for line, row in enumerate(rows[1:], 2):
    if not row or not any(c.strip() for c in row) or (row[0].strip() == 'Source: CBS.' and not any(c.strip() for c in row[1:])):
        excluded.append({'line': line, 'row': row})
        continue
    assert len(row) == 87, (line, len(row))
    values = [row[i].strip() for i in indices]
    assert all(values[:4]), line
    for v in values[4:]:
        assert v == '' or re.fullmatch(r'-?\d+', v), (line, v)
        assert v == '' or -(2**63) <= int(v) < 2**63, (line, v)
    assert all(len(v) <= lim for v, lim in zip(values[:4], [100,50,100,50]))
    clean.append(values)
assert len(clean) == 390
assert len(set(tuple(r[:4]) for r in clean)) == len(clean)
out.parent.mkdir(parents=True, exist_ok=True)
with out.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow([k for k, _ in mapping])
    writer.writerows(clean)
with out.open(newline='', encoding='utf-8') as f:
    saved = list(csv.reader(f))
assert saved == [[k for k, _ in mapping]] + clean
assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
report = {
 'source_sha256': digest, 'raw_unchanged': True,
 'source_columns': len(headers), 'output_rows': len(clean), 'output_columns': len(mapping),
 'excluded_rows': excluded, 'mapping': dict(mapping),
 'missing_counts': {k: sum(r[i] == '' for r in clean) for i, (k, _) in enumerate(mapping)},
 'dimensions': {k: sorted(set(r[i] for r in clean)) for i, (k, _) in enumerate(mapping[:4])},
 'numeric_type': '15 integer columns, compatible with PostgreSQL BIGINT; million euros',
 'samples': [dict(zip([k for k, _ in mapping], clean[i])) for i in [0, 195, 389]],
}
(ROOT / 'reports').mkdir(exist_ok=True)
(ROOT / 'reports/cbs_validation.json').write_text(json.dumps(report, indent=2)+'\n')
print(f'Validated {len(clean)} rows and {len(mapping)} columns. Raw SHA-256 unchanged.\nSaved: {out}')
