"""Reproduce teaching calculations locally; no LLM calls or causal claims."""
from pathlib import Path
import json,math,hashlib,platform
import pandas as pd
import numpy as np
r=Path(__file__).resolve().parent;p=r/'analysis-packet';raw=p/'penguins.csv';df=pd.read_csv(raw)
assert list(df.columns)==['species','island','bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g','sex','year']
a=df.loc[df.species.eq('Adelie')].copy();a['source_csv_row']=a.index+2
clean=a.dropna(subset=['sex','flipper_length_mm']).copy();clean.to_csv(p/'adelie-analysis.csv',index=False)
f=clean.loc[clean.sex.eq('female'),'flipper_length_mm'].to_numpy();m=clean.loc[clean.sex.eq('male'),'flipper_length_mm'].to_numpy()
def describe(x):return {'n':len(x),'mean':float(np.mean(x)),'sd':float(np.std(x,ddof=1)),'se_iid':float(np.std(x,ddof=1)/math.sqrt(len(x))),'median':float(np.median(x))}
B=10000;seed=20261018;rng=np.random.default_rng(seed)
boot=rng.choice(m,(B,len(m)),replace=True).mean(axis=1)-rng.choice(f,(B,len(f)),replace=True).mean(axis=1)
np.savetxt(p/'bootstrap-differences.csv',boot,delimiter=',',header='male_minus_female_mm',comments='',fmt='%.12f')
bins=np.arange(170,216,5);mh,_=np.histogram(m,bins);fh,_=np.histogram(f,bins)
be=np.arange(0,10.5,.5);bh,_=np.histogram(boot,be)
q1,q3=np.quantile(clean.flipper_length_mm,[.25,.75],method='linear');lo=q1-1.5*(q3-q1);hi=q3+1.5*(q3-q1);flag=clean.loc[(clean.flipper_length_mm<lo)|(clean.flipper_length_mm>hi),'source_csv_row'].astype(int).tolist()
# Independent normal samples with KNOWN population SD=10, n=25, true mean=100.
simrng=np.random.default_rng(seed+1);means=simrng.normal(100,10,(1000,25)).mean(axis=1);half=1.959963984540054*10/5;lower=means-half;upper=means+half;covered=(lower<=100)&(upper>=100)
sim=pd.DataFrame({'mean':means,'lower':lower,'upper':upper,'covers_true_100':covered});sim.to_csv(p/'normal-ci-simulation.csv',index=False)
# Exact two-sided symmetric binomial tail for teaching scenario 15/20 heads.
prob=[math.comb(20,k)/2**20 for k in range(21)];pv=sum(prob[:6])+sum(prob[15:])
scatter=[]
for sp in ['Adelie','Chinstrap','Gentoo']:
 v=df.loc[df.species.eq(sp)].dropna(subset=['bill_length_mm','flipper_length_mm']);scatter.append({'name':sp,'x':[float(x) for x in v.bill_length_mm],'y':[float(x) for x in v.flipper_length_mm]})
cor=df.dropna(subset=['bill_length_mm','flipper_length_mm']);corr={'pooled':float(cor.bill_length_mm.corr(cor.flipper_length_mm))}
for sp in ['Adelie','Chinstrap','Gentoo']:
 v=cor.loc[cor.species.eq(sp)];corr[sp]=float(v.bill_length_mm.corr(v.flipper_length_mm))
yearly=[]
for year,v in clean.groupby('year'):
 yearly.append({'year':int(year),'female_n':int(v.sex.eq('female').sum()),'male_n':int(v.sex.eq('male').sum()),'female_mean':float(v.loc[v.sex.eq('female'),'flipper_length_mm'].mean()),'male_mean':float(v.loc[v.sex.eq('male'),'flipper_length_mm'].mean())})
out={'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'runtime':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__},'raw_rows':len(df),'columns':len(df.columns),'species_counts':{k:int(v) for k,v in df.species.value_counts().items()},'missing':{k:int(v) for k,v in df.isna().sum().items()},'adelie_rows':len(a),'analysis_rows':len(clean),'excluded_rows':a.loc[~a.index.isin(clean.index),'source_csv_row'].astype(int).tolist(),'female':describe(f),'male':describe(m),'mean_difference_mm':float(m.mean()-f.mean()),'histogram':{'edges':bins.tolist(),'male':mh.tolist(),'female':fh.tolist()},'iqr_screen':{'q1':float(q1),'q3':float(q3),'lower':float(lo),'upper':float(hi),'flagged_csv_rows':flag,'removed':0},'bootstrap':{'seed':seed,'replicates':B,'sampling_unit':'row; groups separately; iid assumption, not a verified nest/year model','quantile_method':'linear','percentile_95':np.quantile(boot,[.025,.975],method='linear').tolist(),'se':float(np.std(boot,ddof=1)),'histogram_edges':be.tolist(),'histogram_counts':bh.tolist(),'outside_histogram':int(((boot<be[0])|(boot>be[-1])).sum())},'ci_simulation':{'seed':seed+1,'repetitions':1000,'known_mean':100,'known_sd':10,'n':25,'covered':int(covered.sum()),'first_ten':sim.head(10).to_dict(orient='records')},'coin_teaching':{'n':20,'heads':15,'null_p':.5,'probabilities':prob,'two_sided_p':pv},'scatter':scatter,'correlations':corr,'yearly':yearly,'claim_limits':['observational secondary teaching analysis','row independence assumed, not established','sex and flipper complete cases only; no imputation','no population causal conclusion','bootstrap CI does not include selection, missingness, nest dependence or model bias']}
(r/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),'utf-8');print(json.dumps({k:out[k] for k in ['raw_rows','analysis_rows','excluded_rows','female','male','mean_difference_mm','yearly','correlations']},ensure_ascii=False,indent=2));print('bootstrap percentile',out['bootstrap']['percentile_95'],'coin p',pv)
