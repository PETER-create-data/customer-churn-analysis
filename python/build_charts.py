import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if not __debug__:
    raise RuntimeError('Run without -O to retain validation.')
out = ROOT / 'charts'; out.mkdir(exist_ok=True)
rows = list(csv.DictReader(open(ROOT / 'data/cbs_dutch_financial_clean.csv', encoding='utf-8')))
latest = sorted([r for r in rows if r['period']=='2025*' and r['transaction_type']=='Closing balance sheet' and r['institutional_sector']!='Total domestic sectors'], key=lambda r:-int(r['assets_total']))
annual = sorted([r for r in rows if r['institutional_sector']=='Financial corporations' and r['transaction_type']=='Closing balance sheet' and 'quarter' not in r['period']], key=lambda r:r['period'])
assert len(latest)==4 and len(annual)==11
names = {'The non-financial corporations sector':'Non-financial corporations','Households including NPISHs':'Households incl. NPISHs'}
labels = [names.get(r['institutional_sector'],r['institutional_sector']) for r in latest]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#334155','text.color':'#142d40'})
fig, axes = plt.subplots(3,1,figsize=(12,15),gridspec_kw={'height_ratios':[1,1.15,1.15]})
fig.subplots_adjust(top=.89,bottom=.18,left=.24,right=.94,hspace=.65)
fig.text(.065,.96,'Dutch financial sector analysis',fontsize=25,weight='bold')
fig.text(.065,.927,'CBS financial accounts | Annual closing balances | Not consolidated',fontsize=12)
ax=axes[0]; values=[int(r['assets_total'])/1000 for r in latest]
ax.barh(labels,values,color='#147d92',height=.55); ax.invert_yaxis()
ax.set_title('1. Financial assets by sector · 2025*',loc='left',pad=18)
ax.set_xlabel('€ billion'); ax.set_xlim(0,max(values)*1.2); ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
for i,v in enumerate(values): ax.text(v+max(values)*.015,i,f'{v:,.2f}',va='center')
ax=axes[1]; years=[int(r['period'].replace('*','')) for r in annual]; vals=[int(r['assets_total'])/1000 for r in annual]
ax.plot(years,vals,color='#147d92',marker='o',lw=2.5)
ax.set_title('2. Financial-corporation assets · 2015–2025*',loc='left',pad=18)
ax.set_ylabel('€ billion'); ax.set_xlabel('Year'); ax.set_xticks(years[::2]); ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')); ax.grid(axis='y',alpha=.2)
ax.margins(x=.08,y=.25)
for i in [0,len(vals)-1]: ax.annotate(f'{vals[i]:,.2f}',(years[i],vals[i]),xytext=(0,12),textcoords='offset points',ha='center')
ax=axes[2]
keys=['assets_currency_deposits','assets_debt_securities','assets_loans_total','assets_equity_investment_funds']
legend=['Currency & deposits','Debt securities','Loans','Equity & funds','Other assets (residual)']
colors=['#147d92','#e9aa45','#5576b9','#966aa7','#aeb9c2']
shares=np.array([[int(r[k])/int(r['assets_total'])*100 for k in keys] for r in latest]); residual=100-shares.sum(axis=1)
assert (residual>=0).all()
shares=np.column_stack([shares,residual]); left=np.zeros(4)
for j in range(5):
    ax.barh(labels,shares[:,j],left=left,color=colors[j],label=legend[j],height=.55)
    for i,v in enumerate(shares[:,j]):
        if v>=9: ax.text(left[i]+v/2,i,f'{v:.1f}%',va='center',ha='center',fontsize=10,color='white' if j in [0,2,3] else '#142d40')
    left+=shares[:,j]
ax.invert_yaxis(); ax.set_xlim(0,100); ax.set_xlabel('Share of total financial assets (%)'); ax.set_title('3. Asset composition · 2025*',loc='left',pad=18)
ax.legend(loc='upper center',bbox_to_anchor=(.4,-.26),ncol=3,frameon=False,fontsize=10)
fig.text(.065,.035,'Source: supplied CBS table 85883ENG export. * retained from source period labels.\nIndividual sectors only in comparisons. Other assets = total less the four displayed categories.\nFinancial assets exclude non-financial assets; non-consolidated figures include intra-sector positions.',fontsize=10,color='#52616b')
fig.savefig(out/'dutch_financial_dashboard.png',dpi=170)
fig.savefig(out/'dutch_financial_dashboard.svg')
plt.close(fig)
print(f'Saved charts in {out}')
