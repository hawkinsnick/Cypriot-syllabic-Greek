#!/usr/bin/env python3
import argparse,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];F={"records":"data/records.json","lineage":"research/source-lineage-register.json","disagreements":"research/disagreement-register.json","rights":"research/rights-source-matrix.json"}
def rows(k):
 v=json.loads((R/F[k]).read_text())
 if isinstance(v,list):return v
 for z in ("records","lineages","items","sources"):
  if isinstance(v.get(z),list):return v[z]
 return [v]
p=argparse.ArgumentParser();p.add_argument("resource",choices=F);p.add_argument("--text",default="");p.add_argument("--limit",type=int,default=50);a=p.parse_args();q=a.text.casefold();x=[v for v in rows(a.resource) if not q or q in json.dumps(v,ensure_ascii=False).casefold()][:a.limit];print(json.dumps({"resource":a.resource,"records":x,"boundary":"Source-attributed IG evidence; digital entries are not physical-object counts or independent critical witnesses."},ensure_ascii=False,indent=2))
