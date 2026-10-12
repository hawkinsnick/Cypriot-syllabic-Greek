# Source-bound geographic expansion

The 2026-10-12 BBAW [IG XV Cyprus squeeze catalogue](https://ig.bbaw.de/de/abklatsche/ig-xv-cyprus) snapshot adds 210 legacy syllabic source-identifier rows outside the frozen digital-edition view. It includes 138 Rantidi labels, four Paphus vetus labels, 37 Golgi labels and routes for Idalium, Chytri, Soli, Cyrenia and other sites. Two rows have only the source heading `Cyprus alibi`; their site remains unknown. These are catalogue rows, not 210 new inscriptions. Marium and other labels may overlap IG XV 1 records; every IG/object join remains unresolved.

`research/bbaw-squeeze-identifier-snapshot.json` contains factual bibliographic identifiers and geographic headings only, with the exact retrieved HTML SHA-256, source URL and observation time. Full HTML is held locally for this acquisition and is not redistributed. `scripts/build_expansion_layer.py` replays `research/geographic-expansion-register.json` deterministically. The original legacy identifiers and qualifiers are retained: AB, A-C, fragment ranges, uncertain sites, and plaster-cast labels are never silently split or merged. The HTML parser selects the legacy `Tituli syllabici` section and stops before alphabetic material; it does not capture the entire Cyprus catalogue.

Run:

```sh
python scripts/build_expansion_layer.py
python scripts/research_api.py expansion --text Rantidi --limit 5
python -m unittest discover -s tests -v
```

The browser, combined corpus, collection work ledger and individual AI skill include this separate discovery layer. The existing IG XV 1 records, 170 admitted source-interpreted Greek records, token statistics and XML quarantine remain unchanged. A catalogue heading identifying syllabic material does not independently establish Greek-language membership. No readings, images, squeeze scans or unpublished IG XV 1,2 material are imported. The project-authored factual register uses the project's metadata terms; BBAW has not granted a blanket image/text redistribution license through this work.

The older Paphos museum seeds remain separate. ICS 17 AB is not automatically one physical object, and an ICS label is not a verified modern IG number. The squeeze label `Drimu / ICS n. 84` does not establish a join with the museum seed `Dhrymou / ICS 87`. Independent source disagreement must be investigated rather than normalized away.

Next work: check source editions against these exact identifiers, resolve museum inventory and fragment/cast concordances, and acquire licensed readings. BBAW's published digital-edition page still lists the syllabic IG XV 1,1 fascicle; the current research page and their separately archived receipt must be checked before claiming publication of another fascicle. This snapshot is an expanded discovery map, not exhaustive corpus coverage or scholarly approval.
