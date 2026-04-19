# EpiLab — Outbreak Lab (Free Preview)

A standalone interactive outbreak investigation simulator built with Streamlit.
Students become EIS officers and work through three complete outbreak investigations
from first report to control decision.

## Outbreaks included

| # | Scenario | Agent | Key skills |
|---|---|---|---|
| 1 | Norovirus at a University Dining Hall | Norovirus GII | Attack rates, vehicle ID, epidemic curves, secondary spread |
| 2 | Measles in an Under-Vaccinated School | Measles virus | R₀, herd immunity threshold, contact tracing, vaccination policy |
| 3 | Salmonellosis at a Community Church Potluck | Salmonella Enteritidis | Case definition, line list, incubation period, supply chain tracing |

Each investigation maps to the **CDC 10-step outbreak investigation framework** with
interactive decision points, immediate feedback, and built-in calculations.

---

## Deploy to Railway (recommended — always-on, no cold starts)

This repo uses a **Dockerfile** so Railway builds a container image instead of
reinstalling packages on every deploy. The container stays warm — no spin-up delay
when users open the link.

### Steps

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub repo
3. Select this repo — Railway detects `railway.json` and uses the Dockerfile automatically
4. Set **one environment variable** in Railway → Variables:
   ```
   PORT = 8501
   ```
5. Click Deploy. Your URL appears under Settings → Domains.

To keep the service **always-on** (no sleeping): Railway Hobby plan ($5/mo) runs
containers 24/7. The free tier sleeps after inactivity.

### Redeploy after code changes

Just push to GitHub — Railway rebuilds and redeploys automatically.
Because dependencies are baked into the Docker layer, only changed source files
trigger a fast rebuild (not a full pip install).

---

## Local development

```bash
pip install -r requirements.txt
streamlit run outbreak_lab_app.py
```

Or with Docker locally:
```bash
docker build -t outbreak-lab .
docker run -p 8501:8501 outbreak-lab
```
Then open http://localhost:8501

---

## File structure

```
.
├── outbreak_lab_app.py     # Main Streamlit app
├── Dockerfile              # Container definition
├── railway.json            # Tells Railway to use Dockerfile
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit server settings
└── README.md
```

---

## Part of EpiLab Interactive

This is a free preview module. The full EpiLab Interactive app includes:
- Module 1 — Study Design & Causation
- Module 2 — Foundations of Measurement
- Module 3 — Measures & Analysis
- Module 4 — Practice & Application (35+ randomized scenarios)
- Outbreak Lab (these three investigations)
- Four instructor manuals (.docx) aligned to CEPH competencies

**Available at:** https://marywmathis.gumroad.com

Developed by Mary W. Mathis, DrPH · 2026 Edition
