#!/usr/bin/env python3
import argparse,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument("output");a=p.parse_args();rows=json.loads((R/"data/records.json").read_text());out=pathlib.Path(a.output);out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n");out.with_suffix(out.suffix+".manifest.json").write_text(json.dumps({"records":len(rows),"source":"IG XV 1,1 digital","license":"CC BY 4.0","whole_corpus_complete":False,"physical_object_count":None,"independent_epigraphic_review":False},indent=2)+"\n")
