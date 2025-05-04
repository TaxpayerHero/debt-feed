# NZ Debt Feed 🧾🇳🇿

This repository contains a Python script that generates an RSS feed showing New Zealand's current national debt and the debt per person. The data is fetched and calculated based on parameters from [DebtClock.nz](https://www.debtclock.nz).

## 🔗 Live Feed

You can view the live RSS feed here:  
👉 [https://taxpayerhero.github.io/debt-feed/debt_feed.xml](https://taxpayerhero.github.io/debt-feed/debt_feed.xml)

This feed updates **hourly** using GitHub Actions.

---

## 🧠 How It Works

- The script fetches:
  - `initialDebt`, `targetDebt`
  - `startTime`, `endTime`
  - `populationSize`  
  ...from the live JavaScript in [DebtClock.nz](https://www.debtclock.nz)

- It interpolates the current debt based on the time elapsed in the forecast window.

- It generates an RSS feed item like:

  ```
  $190,456,893,141
  ($93,284.25 per person)
  ```

- The RSS file is committed back to the repository and published via GitHub Pages.

---

## 🛠 Tech Stack

- **Python 3**
- **Requests** (for HTML fetching)
- **ElementTree** (for generating XML)
- **GitHub Actions** (to automate updates hourly)
- **GitHub Pages** (to host the RSS feed)

---

## 🕒 GitHub Actions Schedule

The feed is updated every hour via `.github/workflows/generate_rss.yml`.

You can also trigger it manually from the **Actions** tab.

---

## 🚀 How to Use / Modify

1. Clone the repo:
   ```bash
   git clone https://github.com/taxpayerhero/debt-feed.git
   cd debt-feed
   ```

2. Run the script locally:
   ```bash
   pip install requests
   python generate_rss.py
   ```

3. View the generated file:
   ```bash
   cat debt_feed.xml
   ```

To deploy your own version, fork this repo and enable GitHub Pages.

---

## 🧾 Maintained By

This tool is maintained by the team behind [DebtClock.nz](https://www.debtclock.nz) and the [Taxpayers' Union](https://www.taxpayers.org.nz).

---

## 📄 License

MIT License — feel free to copy, fork, and adapt for your country or cause.
