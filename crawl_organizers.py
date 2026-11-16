import asyncio, aiohttp, json, os, re, ssl
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

DATA_DIR = r"D:\AI_LAB\Office\AJWA\lombakurasi\data"
with open(os.path.join(DATA_DIR, "organizers_master.json"), encoding="utf-8") as f:
    orgs = json.load(f)

KEYWORDS = re.compile(r"(event|lomba|kompetisi|olimpiade|jadwal|agenda|competition|news|berita|program|daftar|register|timeline|kalender|calendar|2026|2027|ajang|kejuaraan|fest)", re.I)
YEAR_RE = re.compile(r"(.{0,100}\b(?:2026|2027)\b.{0,120})", re.I)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
}

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

async def fetch_text(session, url, timeout=12):
    if not url or not url.startswith(("http://", "https://")):
        return None, None, "invalid_url"
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=timeout), ssl=ssl_ctx, allow_redirects=True) as resp:
            ct = resp.headers.get("Content-Type", "")
            if "text/html" not in ct and "application/xhtml" not in ct and ct != "":
                return resp.status, str(resp.url), f"non_html:{ct[:40]}"
            raw = await resp.read()
            text = raw[:500_000].decode("utf-8", errors="replace")
            return resp.status, str(resp.url), text
    except Exception as e:
        return None, url, f"err:{type(e).__name__}:{str(e)[:80]}"

def extract_info(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    meta_desc = ""
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    if md and md.get("content"):
        meta_desc = md["content"].strip()

    # Candidate internal links
    base_host = urlparse(base_url).netloc.lower()
    cand_links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        full = urljoin(base_url, href)
        txt = a.get_text(" ", strip=True)
        combo = f"{txt} {href}"
        if KEYWORDS.search(combo) and full not in seen:
            # Prefer same host or linktree/instagram
            h = urlparse(full).netloc.lower()
            if h == base_host or h.endswith("." + base_host) or base_host.endswith("." + h):
                seen.add(full)
                cand_links.append((txt[:80], full))

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    clean_text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    snippets = []
    for m in YEAR_RE.finditer(clean_text):
        s = m.group(1).strip()
        if s not in snippets:
            snippets.append(s)
        if len(snippets) >= 12:
            break

    return {
        "title": title[:200],
        "meta_desc": meta_desc[:300],
        "cand_links": cand_links[:10],
        "year_snippets": snippets,
        "text_sample": clean_text[:800]
    }

async def process_org(sem, session, org):
    async with sem:
        url = org.get("organizer_link") or ""
        status, final_url, body = await fetch_text(session, url)
        res = {
            "organizer": org["organizer"],
            "url": url,
            "final_url": final_url,
            "status": status,
            "error": None,
            "home": None,
            "subpages": []
        }
        if not status or (isinstance(body, str) and (body.startswith("err:") or body.startswith("non_html:") or body == "invalid_url")):
            res["error"] = body
            return res

        info = extract_info(body, final_url or url)
        res["home"] = info

        # Fetch up to 2 relevant subpages if same host and not linktree/ig
        sub_candidates = [lnk for _, lnk in info["cand_links"] if any(k in lnk.lower() for k in ["event", "lomba", "kompetisi", "olimpiade", "jadwal", "agenda", "competition", "2026", "2027", "news", "berita", "program"])][:2]
        for sub_url in sub_candidates:
            st2, fu2, b2 = await fetch_text(session, sub_url, timeout=10)
            if st2 == 200 and b2 and not b2.startswith(("err:", "non_html:")):
                inf2 = extract_info(b2, fu2 or sub_url)
                res["subpages"].append({
                    "url": sub_url,
                    "title": inf2["title"],
                    "year_snippets": inf2["year_snippets"],
                    "text_sample": inf2["text_sample"][:500]
                })
        return res

async def main():
    sem = asyncio.Semaphore(25)
    connector = aiohttp.TCPConnector(limit=30, ssl=ssl_ctx)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [process_org(sem, session, o) for o in orgs]
        results = await asyncio.gather(*tasks)

    out_path = os.path.join(DATA_DIR, "crawl_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ok = sum(1 for r in results if r["status"] == 200)
    with_2026_2027 = sum(1 for r in results if r.get("home") and (r["home"]["year_snippets"] or any(sp["year_snippets"] for sp in r["subpages"])))
    print(f"Crawled {len(results)} organizers: HTTP 200={ok}, with 2026/2027 snippets={with_2026_2027}")

asyncio.run(main())
