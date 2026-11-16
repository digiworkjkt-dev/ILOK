import subprocess, time, urllib.request, os, re
from playwright.sync_api import sync_playwright

DIST = r"D:\AI_LAB\Office\AJWA\lombakurasi\portal\dist"
PORT = 4329

proc = subprocess.Popen(
    ["python", "-m", "http.server", str(PORT), "--directory", DIST],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(1.5)

try:
    base = f"http://127.0.0.1:{PORT}"
    # 1. Check static files & sitemap
    for path in ["/sitemap-index.xml", "/sitemap-0.xml", "/robots.txt", "/ads.txt", "/tentang/", "/disclaimer/", "/privasi/", "/kontak/"]:
        with urllib.request.urlopen(base + path, timeout=5) as r:
            body = r.read().decode("utf-8", errors="replace")
            print(f"GET {path} -> {r.status} (len={len(body)})")
            if path == "/sitemap-0.xml":
                urls = re.findall(r"<loc>(.*?)</loc>", body)
                print(f"  Sitemap URLs count: {len(urls)}")

    # 2. Playwright E2E check
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda err: errors.append(f"PAGEERROR: {err}"))
        page.on("console", lambda msg: errors.append(f"CONSOLE_{msg.type}: {msg.text}") if msg.type == "error" else None)

        # Home
        page.goto(base + "/", wait_until="networkidle")
        home_cards = page.locator("#staticDirectory .lomba-card").count()
        home_ads = page.locator(".ad-slot").count()
        digest_rows = page.locator(".digest-row").count()
        branch_previews = page.locator("#staticDirectory .lomba-branches-preview").count()
        overlaps = page.evaluate("""() => {
            const bad = [];
            document.querySelectorAll('.digest-row').forEach((row, i) => {
                const d = row.querySelector('.digest-date').getBoundingClientRect();
                const t = row.children[1].getBoundingClientRect();
                if (d.right > t.left + 1 && d.bottom > t.top + 1) bad.push({i, dRight: d.right, tLeft: t.left});
            });
            return bad;
        }""")
        assert not overlaps, f"Digest date overlap detected: {overlaps}"
        print(f"Digest overlap check: 0 overlaps across {digest_rows} rows")
        body_font = page.evaluate("getComputedStyle(document.body).fontFamily")
        mono_font = page.evaluate("getComputedStyle(document.querySelector('.mono')).fontFamily")
        print(f"Home cards: {home_cards}, AdSlots: {home_ads}, DigestRows: {digest_rows}, BranchPreviews: {branch_previews}")
        print(f"Fonts -> body: {body_font} | mono: {mono_font}")

        # Test quick chip + collapsible advanced filter drawer
        page.locator('.chip-btn[data-chip="STAR45"]').click()
        print("Quick chip STAR45 meta:", page.locator("#directoryMeta").inner_text())
        page.locator('.chip-btn[data-chip="ALL"]').click()
        page.click("#btnToggleAdvFilters")
        page.select_option("#fRating", "5")
        dyn_cards = page.locator("#dynamicDirectory .lomba-card").count()
        pill_txt = page.locator("#filterCountPill").inner_text()
        print(f"Dynamic 5★ filter cards: {dyn_cards} | Filter count pill: {pill_txt}")

        # Reset & bookmark first card
        page.click("#btnResetFilters")
        page.locator("#staticDirectory .btn-save").first.click()
        saved_cnt = page.locator("#navSavedCount").inner_text()
        print(f"Saved pill after click: {saved_cnt}")

        # Visit /tersimpan/
        page.goto(base + "/tersimpan/", wait_until="networkidle")
        saved_cards = page.locator("#savedList .lomba-card").count()
        print(f"/tersimpan/ cards: {saved_cards}")

        # Visit organizer detail page
        page.goto(base + "/penyelenggara/indonesian-young-scientist-association/", wait_until="networkidle")
        h1 = page.locator("h1").inner_text()
        ld_cnt = page.locator('script[type="application/ld+json"]').count()
        print(f"Detail H1: {h1} | JSON-LD blocks: {ld_cnt}")

        # Visit category hub
        page.goto(base + "/kategori/pendaftaran-dibuka/", wait_until="networkidle")
        cat_h1 = page.locator("h1").inner_text()
        print(f"Category H1: {cat_h1}")

        # Visit guide page
        page.goto(base + "/panduan/arti-bintang-kurasi-lomba-untuk-jalur-prestasi/", wait_until="networkidle")
        guide_ld = page.locator('script[type="application/ld+json"]').count()
        print(f"Guide JSON-LD blocks: {guide_ld}")

        # Mobile viewport check (anchor ad visible)
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(base + "/", wait_until="networkidle")
        anchor_visible = page.locator("#mobileAnchorBar").is_visible()
        print(f"Mobile anchor bar visible: {anchor_visible}")

        browser.close()

    print("E2E Errors:", errors)
    assert not errors, f"Found errors: {errors}"
finally:
    proc.terminate()
    proc.wait()
