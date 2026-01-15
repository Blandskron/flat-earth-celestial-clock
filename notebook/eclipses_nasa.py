!pip install astropy jplephem numpy

import datetime as dt
import re
import requests
import pandas as pd

# --- Config ---
START_DATE = dt.date(2026, 1, 13)
END_DATE   = dt.date(2036, 1, 13)

# NASA/GSFC decade catalogs (tables)
SOLAR_DECADES = [
    "https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html",
    "https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2031.html",
]
LUNAR_DECADES = [
    "https://eclipse.gsfc.nasa.gov/LEdecade/LEdecade2021.html",
    "https://eclipse.gsfc.nasa.gov/LEdecade/LEdecade2031.html",
]

def fetch_tables(url: str) -> list[pd.DataFrame]:
    """Download an HTML page and return all tables."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    html = r.text
    # pandas will parse all <table> elements
    return pd.read_html(html)

def parse_date_cell(cell) -> dt.date | None:
    """
    NASA tables have 'Calendar Date' like '2026 Feb 17' or similar.
    We extract YYYY Mon DD robustly.
    """
    s = str(cell).strip()
    m = re.search(r"(\d{4})\s+([A-Za-z]{3})\s+(\d{1,2})", s)
    if not m:
        return None
    year = int(m.group(1))
    mon  = m.group(2).title()
    day  = int(m.group(3))
    try:
        return dt.datetime.strptime(f"{year} {mon} {day}", "%Y %b %d").date()
    except ValueError:
        return None

def normalize_eclipse_table(df: pd.DataFrame, eclipse_kind: str) -> pd.DataFrame:
    """
    Try to find the date column and type column; keep only what we need.
    Works for both Solar and Lunar decade summary tables.
    """
    # Best guess: first column is Calendar Date on both decade pages
    date_col = df.columns[0]

    out = pd.DataFrame()
    out["date"] = df[date_col].apply(parse_date_cell)

    # Eclipse type column: often includes words like Total/Partial/Annular/Penumbral/Hybrid
    # We'll just concatenate all row text and keep a 'type' guess from any column that looks like "Eclipse Type".
    type_col = None
    for c in df.columns:
        if isinstance(c, str) and "type" in c.lower():
            type_col = c
            break
    if type_col is None and len(df.columns) >= 3:
        # lunar pages often: Calendar Date | TD of Greatest Eclipse | Eclipse Type | ...
        # solar pages often: Calendar Date | Greatest Eclipse TD | Eclipse Type | ...
        # so third column is a good fallback
        type_col = df.columns[2]

    out["type"] = df[type_col].astype(str).str.strip()
    out["kind"] = eclipse_kind

    # Filter valid dates
    out = out.dropna(subset=["date"]).copy()
    return out

def load_eclipses(urls: list[str], kind: str) -> pd.DataFrame:
    rows = []
    for url in urls:
        tables = fetch_tables(url)
        # We want the main decade summary table; it is usually the first big table.
        # We'll scan for a table whose first column contains something date-like.
        chosen = None
        for t in tables:
            if t.shape[0] < 5 or t.shape[1] < 2:
                continue
            sample = t.iloc[0, 0]
            if parse_date_cell(sample) is not None:
                chosen = t
                break
        if chosen is None:
            # fallback: try first table
            chosen = tables[0]

        rows.append(normalize_eclipse_table(chosen, kind))

    return pd.concat(rows, ignore_index=True)

def main():
    solar = load_eclipses(SOLAR_DECADES, "solar")
    lunar = load_eclipses(LUNAR_DECADES, "lunar")

    all_e = pd.concat([solar, lunar], ignore_index=True)

    # Filter range
    all_e = all_e[(all_e["date"] >= START_DATE) & (all_e["date"] <= END_DATE)].copy()
    all_e = all_e.sort_values(["date", "kind"]).reset_index(drop=True)

    # Print
    print(f"Eclipses from {START_DATE} to {END_DATE} (NASA/GSFC decade catalogs):\n")
    for _, r in all_e.iterrows():
        print(f"{r['date'].isoformat()}  |  {r['kind'].upper():5s}  |  {r['type']}")

    print(f"\nTotal: {len(all_e)} eclipses")

if __name__ == "__main__":
    main()



"""
Eclipses from 2026-01-13 to 2036-01-13 (NASA/GSFC decade catalogs):

2026-02-17  |  SOLAR  |  Annular
2026-03-03  |  LUNAR  |  Total
2026-08-12  |  SOLAR  |  Total
2026-08-28  |  LUNAR  |  Partial
2027-02-06  |  SOLAR  |  Annular
2027-02-20  |  LUNAR  |  Penumbral
2027-07-18  |  LUNAR  |  Penumbral
2027-08-02  |  SOLAR  |  Total
2027-08-17  |  LUNAR  |  Penumbral
2028-01-12  |  LUNAR  |  Partial
2028-01-26  |  SOLAR  |  Annular
2028-07-06  |  LUNAR  |  Partial
2028-07-22  |  SOLAR  |  Total
2028-12-31  |  LUNAR  |  Total
2029-01-14  |  SOLAR  |  Partial
2029-06-12  |  SOLAR  |  Partial
2029-06-26  |  LUNAR  |  Total
2029-07-11  |  SOLAR  |  Partial
2029-12-05  |  SOLAR  |  Partial
2029-12-20  |  LUNAR  |  Total
2030-06-01  |  SOLAR  |  Annular
2030-06-15  |  LUNAR  |  Partial
2030-11-25  |  SOLAR  |  Total
2030-12-09  |  LUNAR  |  Penumbral
2031-05-07  |  LUNAR  |  Penumbral
2031-05-21  |  SOLAR  |  Annular
2031-06-05  |  LUNAR  |  Penumbral
2031-10-30  |  LUNAR  |  Penumbral
2031-11-14  |  SOLAR  |  Hybrid
2032-04-25  |  LUNAR  |  Total
2032-05-09  |  SOLAR  |  Annular
2032-10-18  |  LUNAR  |  Total
2032-11-03  |  SOLAR  |  Partial
2033-03-30  |  SOLAR  |  Total
2033-04-14  |  LUNAR  |  Total
2033-09-23  |  SOLAR  |  Partial
2033-10-08  |  LUNAR  |  Total
2034-03-20  |  SOLAR  |  Total
2034-04-03  |  LUNAR  |  Penumbral
2034-09-12  |  SOLAR  |  Annular
2034-09-28  |  LUNAR  |  Partial
2035-02-22  |  LUNAR  |  Penumbral
2035-03-09  |  SOLAR  |  Annular
2035-08-19  |  LUNAR  |  Partial
2035-09-02  |  SOLAR  |  Total

Total: 45 eclipses
"""
