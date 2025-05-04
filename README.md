# NZ Debt Feed (RSS)

This repository generates a public RSS feed that tracks New Zealand's national debt and per-household share, based on live and forecast data from [DebtClock.nz](https://www.debtclock.nz).

🕰 **Feed updates every hour at 30 minutes past the hour (NZT)**, projecting debt values for the top of the next hour.

📡 **Live RSS feed URL**:  
https://taxpayerhero.github.io/debt-feed/debt_feed.xml

---

## 📌 What This Project Does

- Pulls forecast data from [DebtClock.nz](https://www.debtclock.nz)
- Calculates projected national debt for **30 minutes in the future**
- Outputs an RSS feed with:
  - Total debt (to the dollar)
  - Per-household debt (to the cent)
  - Updated `pubDate` formatted for the next top of the hour

---

## 🔁 Update Frequency

- GitHub Actions runs every hour at `HH:30`
- The RSS `<pubDate>` is set for the **top of the next hour**
- Zapier or Buffer can use the `pubDate` to post tweets **exactly on the hour**

---

## 🔧 How to Update Forecast Values (every 6 months)

The script uses hardcoded fallback values in case the live site is unavailable.  
**When [DebtClock.nz](https://www.debtclock.nz) is updated (usually each July and January), do the following:**

1. Open `generate_rss.py`
2. Find the section:

```python
FALLBACK_PARAMS = {
    "initial_debt": 175_464_000_000,
    "target_debt": 192_810_000_000,
    "start_time": int(datetime(2024, 7, 1, 0, 1, tzinfo=...)).timestamp(),
    "end_time": int(datetime(2025, 6, 30, 23, 59, tzinfo=...)).timestamp(),
    "population_size": 2_034_000
}
```

3. Update:
   - `initial_debt`: New starting national debt figure
   - `target_debt`: Forecast debt for the end of the new forecast period
   - `start_time`: Start of the forecast period (NZ time)
   - `end_time`: End of the forecast period (NZ time)
   - `population_size`: Should match the value used by DebtClock.nz (which represents households)

4. Commit your changes and push to GitHub
5. GitHub Actions will pick up the change at the next `:30` update

---

## 🔧 Manual Trigger

You can run the workflow manually from the **Actions** tab in GitHub.

---

## 📦 Dependencies

Ensure the following are listed in `requirements.txt`:

```
requests
pytz
```

---

## 🐦 Integration Example (Zapier + Buffer)

- Use Zapier to watch the RSS feed
- Add a **“Delay Until `pubDate`”** step
- Post the feed title to Buffer/Twitter exactly on the hour

---

## 🔗 Maintained by

[TaxpayerHero](https://github.com/TaxpayerHero)

