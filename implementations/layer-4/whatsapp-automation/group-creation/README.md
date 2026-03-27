# 🤖 WhatsApp Web Automation - Group Creation

Automated group creation on WhatsApp Web using Selenium and Safari with QR code login.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip3 install selenium
```

### 2. Configure Settings

Edit `config.json` with:

```json
{
  "login": {
    "qr_scan_timeout": 60
  },
  "group": [
    {
      "title": "Test Group 2026"
    },
    {
      "title": "Test Group 2026-2"
    }
  ],
  "members": {
    "to_add": [
      "+91XXXXXXXX00"
    ]
  },
  "automation": {
    "wait_timeout": 30,
    "action_delay": 1
  }
}
```

### 3. Run

```bash
python3 whatsappWeb-create-group.py
```

---

## 📋 What It Does

### Step 1: Login (QR Code)
- Opens WhatsApp Web
- Displays QR code
- Waits for QR scan from your phone (configurable timeout)

### Step 2: Create Group
- Clicks menu dots (⋯)
- Selects "New group"

### Step 3: Add Members
- Searches each phone number in contacts
- Uses keyboard navigation to select results
- Adds member to group
- Skips if member not found in contacts

### Step 4: Set Group Title
- Enters group title in the "Group subject" field
- Clicks "Create group" button

### Multiple Groups
- Creates each group with the same members
- Supports unlimited groups via config array

---

## 🔧 Configuration (config.json)

### **Part 1: LOGIN CONFIGURATION**
```json
"login": {
  "qr_scan_timeout": 60
}
```
- `qr_scan_timeout`: Seconds to wait for QR code scan (default: 60)

### **Part 2: GROUP CONFIGURATION (Array)**
```json
"group": [
  {
    "title": "First Group",
    "description": "For testing purposes only"
  },
  {
    "title": "Second Group",
    "description": "For testing purposes only"
  }
]
```
- Create multiple groups by adding more objects to the array
- Each group gets the same members added

### **Part 3: GROUP MEMBERS**
```json
"members": {
  "to_add": [
    "+91XXXXXXXX99",
    "+91XXXXXXXX90"
  ]
}
```
- **Must be saved in WhatsApp contacts** before running
- Phone numbers not in contacts will be skipped with a warning

### **Part 4: Automation Settings**
```json
"automation": {
  "wait_timeout": 30,
  "action_delay": 1
}
```
- `wait_timeout`: Max seconds to wait for elements (default: 30)
- `action_delay`: Delay between actions in seconds (default: 1)

---

## 📱 Example Configurations

### Example 1: Single Group with Multiple Members
```json
{
  "login": {
    "qr_scan_timeout": 60
  },
  "group": [
    {
      "title": "Friends Group"
    }
  ],
  "members": {
    "to_add": [
      "+911XXXXXXX00",
      "+912XXXXXXX00"
    ]
  },
  "automation": {
    "wait_timeout": 30,
    "action_delay": 1
  }
}
```

### Example 2: Multiple Groups
```json
{
  "login": {
    "qr_scan_timeout": 60
  },
  "group": [
    { "title": "Work Team" },
    { "title": "Study Group" },
    { "title": "Sports Club" }
  ],
  "members": {
    "to_add": [
      "+9112345678"
    ]
  },
  "automation": {
    "wait_timeout": 30,
    "action_delay": 1
  }
}
```

---

## ⚠️ Important Notes

1. **Phone Numbers**: Must be saved in WhatsApp contacts on the phone
2. **QR Code**: Scan with your phone when prompted (60 seconds timeout)
3. **Internet**: Both phone and computer must be online
4. **WhatsApp App**: Must be active on your phone
5. **Rate Limiting**: WhatsApp may limit rapid group creation
6. **Multiple Groups**: Same members will be added to all groups

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| QR code scan timeout | Scan faster, or increase `qr_scan_timeout` in config |
| Member not found | Verify phone is saved in contacts on your phone |
| "No search results found" warning | Contact not in phone's WhatsApp contacts |
| Group creation fails | Try increasing `wait_timeout` in config.json |
| Safari WebDriver error | Update Safari and run `safaridriver --enable` |
| "Focus" ring not found | Check WhatsApp Web UI hasn't changed |

---

## 📝 How Member Selection Works

The script:
1. Types the phone number in search
2. Waits for search results (2 seconds)
3. Checks if results exist
4. **If found**: Presses Arrow Down + Enter to select
5. **If not found**: Skips with warning, continues with next member

**Key Point**: Members must be in your phone's WhatsApp contact list before running the script.

---

## 📝 File Structure

```
group-creation/
├── config.json                    ← Edit with your settings
├── whatsappWeb-create-group.py    ← Main automation script
└── README.md                      ← This file
```

---

## 🔐 Security Notes

- Never commit `config.json` with real phone numbers
- Keep phone numbers private
- Add to `.gitignore`:
  ```
  config.json
  ```

---

## 🎯 Recent Updates

- ✅ QR code login (no phone number needed)
- ✅ Menu dots approach (more reliable)
- ✅ Keyboard navigation for member selection
- ✅ Multiple group support
- ✅ Better error handling & warnings
- ✅ Contenteditable div for group title
