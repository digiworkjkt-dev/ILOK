import json, os, re
from collections import Counter

DATA_DIR = r"D:\AI_LAB\Office\AJWA\lombakurasi\data"
BATCH_DIR = os.path.join(DATA_DIR, "batches")

with open(os.path.join(DATA_DIR, "organizers_master.json"), encoding="utf-8") as f:
    orgs = json.load(f)

deep_results = {}
for fn in sorted(os.listdir(BATCH_DIR)):
    if fn.startswith("out_") and fn.endswith(".json"):
        with open(os.path.join(BATCH_DIR, fn), encoding="utf-8") as f:
            data = json.load(f)
        for r in data.get("results", []):
            deep_results[r["organizer"].strip()] = r

print(f"Organizers in master: {len(orgs)}")
print(f"Organizers in deep search outputs: {len(deep_results)}")

missing = [o["organizer"] for o in orgs if o["organizer"].strip() not in deep_results]
print(f"Missing from deep search: {len(missing)}")
if missing:
    for m in missing:
        print("  MISSING:", m)

# Compute sortable date key and days_from_now (relative to 2026-11-15)
from datetime import date
TODAY = date(2026, 11, 15)

def parse_sort_date(dstr):
    if not dstr or dstr == "-":
        return None, None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", dstr.strip())
    if m:
        y, mo, da = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            dt = date(y, mo, da)
            return dstr.strip(), (dt - TODAY).days
        except ValueError:
            pass
    m2 = re.match(r"^(\d{4})-(\d{2})$", dstr.strip())
    if m2:
        y, mo = int(m2.group(1)), int(m2.group(2))
        try:
            # use 15th of month as midpoint estimate for sorting
            dt = date(y, mo, 15)
            return f"{y:04d}-{mo:02d}-15", (dt - TODAY).days
        except ValueError:
            pass
    return None, None

def normalize_jenjang(txt):
    t = (txt or "").upper()
    tags = []
    for k, pat in [
        ("PAUD/TK", r"\b(PAUD|TK|PRA[\s-]?SEKOLAH)\b"),
        ("SD/MI", r"\b(SD|MI|SEKOLAH DASAR|ELEMENTARY)\b"),
        ("SMP/MTs", r"\b(SMP|MTS|SLTP|JUNIOR HIGH)\b"),
        ("SMA/SMK/MA", r"\b(SMA|SMK|MA|SLTA|SEDERAJAT|SENIOR HIGH|HIGH SCHOOL)\b"),
        ("Mahasiswa/DIKTI", r"\b(MAHASISWA|DIKTI|UNIVERSIT|PERGURUAN TINGGI|COLLEGE|UNDERGRADUATE|SARJANA|DIPLOMA)\b"),
        ("Guru/Tendik", r"\b(GURU|DOSEN|PENDIDIK|TENAGA KEPENDIDIKAN)\b"),
        ("Umum/Atlet", r"\b(UMUM|SENIOR|ATLET|TERBUKA|OPEN|PENELITI|YOUTH|JUNIOR|CADET|U-\d+)\b"),
    ]:
        if re.search(pat, t):
            tags.append(k)
    return tags if tags else ["Lainnya"]

def normalize_mode(txt):
    t = (txt or "").lower()
    if "hybrid" in t or ("daring" in t and "luring" in t) or ("online" in t and ("offline" in t or "tatap muka" in t)):
        return "Hybrid"
    if any(k in t for k in ["daring", "online", "virtual", "cbt", "zoom"]):
        return "Online / Daring"
    if any(k in t for k in ["luring", "offline", "tatap muka", "onsite", "gor ", "stadion", "kampus", "hotel", "gedung"]):
        return "Offline / Luring"
    return "Belum Ditentukan"

merged = []
for o in orgs:
    ds = deep_results.get(o["organizer"].strip(), {})
    s_date, days_away = parse_sort_date(ds.get("nearest_start_date", "-"))
    e_date, _ = parse_sort_date(ds.get("nearest_end_date", "-"))
    reg_date, reg_days = parse_sort_date(ds.get("registration_deadline", "-"))

    # Also keep SIMT competition list cleanly
    simt_comps = []
    for c in o["competitions"]:
        simt_comps.append({
            "name": c["competition"],
            "short": c["short"],
            "rating": c["rating"],
            "score": c["score"],
            "start": c["start"],
            "end": c["end"],
            "level": c["level"],
            "cluster": c["cluster"],
            "category": c["category"],
            "link": c["link"],
            "branches": c["branches"],
        })

    merged.append({
        "organizer": o["organizer"],
        "short_name": o["short_name"],
        "organizer_link": o["organizer_link"],
        "country": o["country"],
        "max_rating": o["max_rating"],
        "avg_score": o["avg_score"],
        "entries_count": o["entries_count"],
        "competitions_count": o["competitions_count"],
        "clusters": o["clusters"],
        "levels": o["levels"],
        "categories": o["categories"],
        "sectors": o["sectors"],
        "latest_simt_start": o["latest_simt_start"],
        "nearest_event_name": ds.get("nearest_event_name", "-"),
        "schedule_status": ds.get("schedule_status", "Belum Ada Info Terbaru"),
        "nearest_start_date": ds.get("nearest_start_date", "-"),
        "nearest_end_date": ds.get("nearest_end_date", "-"),
        "registration_deadline": ds.get("registration_deadline", "-"),
        "sort_date": s_date or "9999-12-31",
        "days_from_now": days_away,
        "reg_days_from_now": reg_days,
        "target_jenjang": ds.get("target_jenjang", "-"),
        "jenjang_tags": normalize_jenjang(ds.get("target_jenjang", "")),
        "mode_lokasi": ds.get("mode_lokasi", "-"),
        "mode_type": normalize_mode(ds.get("mode_lokasi", "")),
        "source_url": ds.get("source_url", o["organizer_link"]),
        "notes": ds.get("notes", ""),
        "simt_competitions": simt_comps,
    })

out_path = os.path.join(DATA_DIR, "merged_lomba_kurasi.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("\nSchedule Status counts:", Counter(x["schedule_status"] for x in merged))
print("Mode Type counts:", Counter(x["mode_type"] for x in merged))
print("With exact/month start date >= 2026-11-15:", sum(1 for x in merged if x["days_from_now"] is not None and x["days_from_now"] >= 0))
print("With start date in Nov-Dec 2026:", sum(1 for x in merged if x["nearest_start_date"].startswith(("2026-11", "2026-12"))))
print("With start date in 2027:", sum(1 for x in merged if x["nearest_start_date"].startswith("2027")))
print("With start date < 2026-11-15 (past/ongoing):", sum(1 for x in merged if x["days_from_now"] is not None and x["days_from_now"] < 0))
print("With start date '-' (unknown):", sum(1 for x in merged if x["nearest_start_date"] == "-"))

# Show sample of earliest upcoming events (>= 2026-11-15)
upcoming = sorted([x for x in merged if x["days_from_now"] is not None and x["days_from_now"] >= -5], key=lambda z: (z["sort_date"], -z["max_rating"]))
print(f"\nTop 20 earliest upcoming/current events:")
for x in upcoming[:20]:
    print(f"  [{x['max_rating']}★] {x['nearest_start_date']:10s} | {x['schedule_status']:25s} | {x['organizer'][:32]:32s} | {x['nearest_event_name'][:55]}")
