import urllib.request, json, time, os

OUT_DIR = r"D:\AI_LAB\Office\AJWA\lombakurasi\data"

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

all_items = []
for rating in [5, 4, 3]:
    page = 1
    per_page = 100
    while True:
        url = f"https://simt.kemendikdasmen.go.id/api/v2/list-kurasi?page={page}&per_page={per_page}&rate_kurasi={rating}"
        d = get_json(url)
        res = d.get("result", {})
        lst = res.get("list", [])
        pag = res.get("pagination", {})
        all_items.extend(lst)
        print(f"rating={rating} page={page}/{pag.get('total_page')} fetched={len(lst)} total_expected={pag.get('total_data')}")
        if page >= pag.get("total_page", 0) or not lst:
            break
        page += 1
        time.sleep(0.15)

# Deduplicate by id just in case
by_id = {}
for item in all_items:
    by_id[item["id"]] = item
items = list(by_id.values())

with open(os.path.join(OUT_DIR, "simt_kurasi_star3plus.json"), "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(items)} unique rows.")
orgs = {}
comps = {}
for it in items:
    oid = it.get("organizer_id") or it.get("organizer")
    orgs.setdefault(oid, {"organizer": it.get("organizer"), "short": it.get("short_name_of_organizer"), "link": it.get("organizer_useful_link"), "country": it.get("country"), "count": 0, "competitions": set(), "max_rating": 0})
    orgs[oid]["count"] += 1
    orgs[oid]["competitions"].add(it.get("competition"))
    orgs[oid]["max_rating"] = max(orgs[oid]["max_rating"], it.get("rating") or 0)

    cid = it.get("competition_id") or it.get("competition")
    comps.setdefault(cid, {"competition": it.get("competition"), "organizer": it.get("organizer"), "rating": it.get("rating"), "start": it.get("competition_start"), "end": it.get("competition_end"), "level": it.get("level"), "country": it.get("country"), "branches": 0})
    comps[cid]["branches"] += 1

print(f"Unique organizers: {len(orgs)}")
print(f"Unique competitions: {len(comps)}")

from collections import Counter
print("Ratings breakdown (rows):", Counter(it.get("rating") for it in items))
print("Created_at years:", Counter((it.get("created_at") or "")[:4] for it in items))
print("Countries top 10:", Counter(it.get("country") for it in items).most_common(10))
print("Levels:", Counter(it.get("level") for it in items))
print("Categories:", Counter(it.get("category") for it in items))
print("Clusters:", Counter(it.get("cluster") for it in items))
