# 🏛️ Mangla Aarti Booking Automation

Automated booking system for Mangla Aarti pooja at Shri Kashi Vishwanath Temple using Selenium.

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip3 install selenium webdriver-manager
```

### 2. Choose Your Script

#### Option A: Safari (macOS)
```bash
python macOs-arm64-safari-user-agent.py
```

#### Option B: LibreWolf (macOS ARM64)
```bash
python macOs-arm64-librewolf-user-agent.py
```

### 3. Configure Before Running

Edit the script and update these variables with your details:

```python
EMAIL = "your-email@gmail.com"
PASSWORD = "your-password"
POOJA_PAGE = "https://shrikashivishwanath.org/frontend/home/poojadetail/..."

NUM_ADULTS = 5
NUM_CHILDREN = 1

ADULTS = [
    ("Your Name", "Male", "35", "Aadhar1"),
    ("Family Member", "Female", "32", "Aadhar2"),
    # Add more...
]

CHILDREN = [
    ("Child Name", "Female", "Below 1 Year"),
]
```

### 4. Run

```bash
python macOs-arm64-safari-user-agent.py    # or LibreWolf version
```

The script will:
- ✅ Login to your account
- ✅ Navigate to the pooja page
- ✅ Check availability
- ✅ Book first available slot
- ✅ Fill devotee details automatically

---

## 📋 Requirements

- Python 3.8+
- macOS (ARM64 architecture)
- Safari or LibreWolf browser installed
- Internet connection

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser not found | Install Safari (built-in) or LibreWolf |
| GeckoDriver fails | `webdriver-manager` handles auto-download |
| Selectors don't match | Website may have changed; update CSS selectors in the script |
| Login fails | Check EMAIL and PASSWORD in script |

---

## ⚠️ Notes

- Update email/password/devotee details **before running**
- Test on non-production URLs first
- Keep personal data (Aadhar) masked if sharing the script
