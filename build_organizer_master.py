import json, os

DATA_DIR = r"D:\AI_LAB\Office\AJWA\lombakurasi\data"
with open(os.path.join(DATA_DIR, "simt_kurasi_star3plus.json"), encoding="utf-8") as f:
    items = json.load(f)

orgs = {}
for x in items:
    o = (x.get("organizer") or "").strip()
    if o not in orgs:
        orgs[o] = {
            "organizer_id": x.get("organizer_id"),
            "organizer": o,
            "short_name": x.get("short_name_of_organizer"),
            "organizer_link": x.get("organizer_useful_link"),
            "country": x.get("country"),
            "max_rating": 0,
            "scores": [],
            "clusters": set(),
            "levels": set(),
            "categories": set(),
            "sectors": set(),
            "competitions": {},
            "entries_count": 0,
        }
    rec = orgs[o]
    rec["entries_count"] += 1
    rec["max_rating"] = max(rec["max_rating"], x.get("rating") or 0)
    if x.get("score") is not None:
        rec["scores"].append(x["score"])
    for k, s in [("cluster", "clusters"), ("level", "levels"), ("category", "categories"), ("sector", "sectors")]:
        if x.get(k):
            rec[s].add(x[k])

    cname = (x.get("competition") or "").strip()
    if cname not in rec["competitions"]:
        rec["competitions"][cname] = {
            "competition": cname,
            "short": x.get("short_name_of_competition"),
            "rating": x.get("rating"),
            "score": x.get("score"),
            "start": x.get("competition_start"),
            "end": x.get("competition_end"),
            "link": x.get("competition_useful_link"),
            "level": x.get("level"),
            "cluster": x.get("cluster"),
            "category": x.get("category"),
            "sector": x.get("sector"),
            "type": x.get("type"),
            "batch": x.get("batch"),
            "branches": []
        }
    b = (x.get("branch") or "").strip()
    if b and b not in rec["competitions"][cname]["branches"]:
        rec["competitions"][cname]["branches"].append(b)

out_list = []
for o in sorted(orgs.values(), key=lambda z: (-z["max_rating"], -z["entries_count"], z["organizer"])):
    comps = sorted(o["competitions"].values(), key=lambda c: (c["start"] or ""), reverse=True)
    out_list.append({
        "organizer": o["organizer"],
        "short_name": o["short_name"],
        "organizer_link": o["organizer_link"],
        "country": o["country"],
        "max_rating": o["max_rating"],
        "avg_score": round(sum(o["scores"]) / len(o["scores"]), 2) if o["scores"] else None,
        "entries_count": o["entries_count"],
        "competitions_count": len(comps),
        "clusters": sorted(o["clusters"]),
        "levels": sorted(o["levels"]),
        "categories": sorted(o["categories"]),
        "sectors": sorted(o["sectors"]),
        "latest_simt_start": max((c["start"] or "" for c in comps), default=""),
        "latest_simt_end": max((c["end"] or "" for c in comps), default=""),
        "competitions": comps,
    })

with open(os.path.join(DATA_DIR, "organizers_master.json"), "w", encoding="utf-8") as f:
    json.dump(out_list, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(out_list)} organizers to organizers_master.json")
