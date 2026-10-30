# JOYCE — Job-Oriented Yield & Code Examiner

> **Ship confidently. Or don't ship at all.**
> JOYCE scans your repo for the mistakes that kill vibe-coded apps before they ever reach users.

## Why JOYCE exists

AI made building apps easy. It didn't make *shipping them safely* easy.
Every day, indie developers push code to production with:

- 🔑 API keys hardcoded in source
- 📄 `.env` files committed to Git
- 🔓 Supabase / Firebase rules set to `public`
- 🐛 Debug flags left on in production builds

JOYCE finds these in seconds and gives you a **Production Readiness Score** (0–100) with a prioritized fix list.

## Quick start

```bash
git clone https://github.com/YOURNAME/joyce.git
cd joyce
pip install -r requirements.txt
python joyce.py scan /path/to/your/project