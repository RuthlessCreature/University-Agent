from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
r=Path(__file__).resolve().parent;p=r/'figure-packet';df=pd.read_csv(p/'penguins.csv');v=df.loc[df.species.eq('Adelie')].dropna(subset=['sex','flipper_length_mm']);rng=np.random.default_rng(20261018);groups=[]
for sex in ['female','male']:
 x=v.loc[v.sex.eq(sex),'flipper_length_mm'].to_numpy();means=rng.choice(x,(10000,len(x)),replace=True).mean(axis=1);groups.append({'sex':sex,'n':len(x),'mean':float(x.mean()),'sd':float(x.std(ddof=1)),'se_iid':float(x.std(ddof=1)/np.sqrt(len(x))),'mean_bootstrap_95':np.quantile(means,[.025,.975]).tolist()})
edges=np.arange(170,216,5);hist={'edges':edges.tolist(),'series':[{'name':sex,'values':np.histogram(v.loc[v.sex.eq(sex),'flipper_length_mm'],edges)[0].tolist()} for sex in ['female','male']]}
scatter=[]
for sex in ['female','male']:
 q=v.loc[v.sex.eq(sex)].dropna(subset=['bill_length_mm']);scatter.append({'name':sex,'x':q.bill_length_mm.tolist(),'y':q.flipper_length_mm.tolist()})
years=[]
for year,q in v.groupby('year'):years.append({'year':int(year),**{sex:float(q.loc[q.sex.eq(sex),'flipper_length_mm'].mean()) for sex in ['female','male']}})
q={'source_sha256':hashlib.sha256((p/'penguins.csv').read_bytes()).hexdigest(),'groups':groups,'histogram':hist,'scatter':scatter,'years':years,'bootstrap_seed':20261018,'bootstrap_per_group':10000,'bootstrap_quantile_method':'linear','claim_limit':'row iid conditional teaching calculation; no verified nest/individual independence; no causal inference','runtime':{'numpy':np.__version__,'pandas':pd.__version__}}
(r/'figure-data.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(groups,indent=2))
