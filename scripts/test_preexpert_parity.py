#!/usr/bin/env python3
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];req=["research/source-lineage-register.json","research/disagreement-register.json","research/rights-source-matrix.json","research/residual-blocker-ledger.json","research/ig-xv1-authority.json"];assert all((R/p).exists() for p in req);rows=json.loads((R/"data/records.json").read_text());idx=json.loads((R/"data/source-index.json").read_text());assert len(idx)==593 and len(rows)==592;print(json.dumps({"status":"PASS","source_responses":593,"parsed_records":592,"quarantined":1,"whole_corpus_complete":False}))
