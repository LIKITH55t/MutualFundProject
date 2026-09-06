import requests
import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    "125497": "HDFC Top 100 Direct",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip"
}


def fetch_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nFetching: {scheme_name} ({scheme_code})")
    print(f"URL: {url}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = response.json()

    if result.get("status") != "SUCCESS":
        raise ValueError(f"API request failed for {scheme_code}")

    nav_data = result.get("data", [])

    if not nav_data:
        raise ValueError(f"No NAV data returned for {scheme_code}")

    df = pd.DataFrame(nav_data)

    # Convert values to appropriate types
    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    df["nav"] = pd.to_numeric(
        df["nav"],
        errors="coerce"
    )

    # Add scheme information
    df["scheme_code"] = scheme_code
    df["scheme_name"] = scheme_name

    # Save individual raw CSV
    output_file = RAW_DATA_DIR / f"nav_{scheme_code}.csv"
    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")
    print(f"Shape: {df.shape}")

    return df


all_nav_data = []

for scheme_code, scheme_name in SCHEMES.items():
    try:
        df = fetch_nav(scheme_code, scheme_name)
        all_nav_data.append(df)

    except Exception as e:
        print(f"ERROR for {scheme_code}: {e}")


# Combine all fetched NAV data
if all_nav_data:
    nav_history = pd.concat(all_nav_data, ignore_index=True)

    combined_file = RAW_DATA_DIR / "nav_history_live.csv"
    nav_history.to_csv(combined_file, index=False)

    print("\n" + "=" * 60)
    print("LIVE NAV FETCH COMPLETED")
    print("=" * 60)

    print(f"Combined shape: {nav_history.shape}")
    print(f"Saved to: {combined_file}")

    print("\nSchemes fetched:")
    print(nav_history["scheme_name"].unique())
else:
    print("\nNo NAV data was fetched.")