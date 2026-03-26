"""
Mangla Aarti Booking - Shri Kashi Vishwanath Temple
Selenium + Safari

Flow:
  1. Open pooja page -> click Book Now -> login
  2. Re-open pooja page -> click Book Now (post-login)
  3. Fill adults count -> Check Availability
  4. Click first "Book Now" in availability list
  5. Fill devotee details (name, gender, age)

pip3 install selenium webdriver-manager
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

POOJA_PAGE = "https://shrikashivishwanath.org/frontend/home/poojadetail/c1M2MS9DUG1ydzZQVVFqT0w0SVNydz09/2026-04-25"

#POOJA_PAGE = "https://shrikashivishwanath.org/frontend/home/poojadetail/U3ViQWhsYms2WUoydkx5VkhvazgxUT09"


EMAIL = "xyz@gmail.com"
PASSWORD = "12345"

NUM_ADULTS = 1
NUM_CHILDREN = 0

ADULTS = [
    ("Name1", "Male", "60", "123456789012"),
]

WAIT = 10


def driver_init():
    d = webdriver.Safari()
    d.maximize_window()
    return d


def wait_click(d, css, timeout=WAIT):
    el = WebDriverWait(d, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    el.click()
    return el


def wait_el(d, css, timeout=WAIT):
    return WebDriverWait(d, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))


def type_into(d, css, text, timeout=WAIT):
    el = wait_el(d, css, timeout)
    el.clear()
    el.send_keys(text)
    return el


def select_dropdown(el, visible_text):
    Select(el).select_by_visible_text(visible_text)


def js_click(d, el):
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.3)
    el.click()


def dismiss_chat_popup(d):
    d.execute_script("""
        var selectors = [
            '[id*="nandi"]', '[class*="nandi"]',
            '[id*="chat"]', '[class*="chat-widget"]',
            '[id*="livechat"]', '[class*="livechat"]',
            'iframe[title*="chat"]', 'iframe[title*="Nandi"]'
        ];
        selectors.forEach(function(s) {
            document.querySelectorAll(s).forEach(function(el) {
                el.remove();
            });
        });
    """)


def step1_login(d):
    print("[1] Opening pooja page & logging in...")
    d.get(POOJA_PAGE)
    dismiss_chat_popup(d)
    login_btn = WebDriverWait(d, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-style[data-target='#loginModal']"))
    )
    js_click(d, login_btn)

    WebDriverWait(d, WAIT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#passform"))
    )

    try:
        js_click(d, d.find_element(By.ID, "loginh4"))
    except Exception:
        pass

    email_el = WebDriverWait(d, WAIT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#email"))
    )
    email_el.clear()
    email_el.send_keys(EMAIL)

    pwd_el = d.find_element(By.CSS_SELECTOR, "#password")
    pwd_el.clear()
    pwd_el.send_keys(PASSWORD)

    js_click(d, d.find_element(By.CSS_SELECTOR, "#passform button[type='submit']"))
    WebDriverWait(d, WAIT).until(EC.url_changes(POOJA_PAGE))
    print(f"    Logged in. URL: {d.current_url}")


def step2_book_now(d):
    print("[2] Re-opening pooja page & clicking Book Now...")
    d.get(POOJA_PAGE)
    time.sleep(2)
    dismiss_chat_popup(d)
    time.sleep(0.5)

    clicked = d.execute_script("""
        var btns = document.querySelectorAll('button.btn-style');
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].textContent.trim().toLowerCase().indexOf('book now') !== -1) {
                btns[i].scrollIntoView({block:'center'});
                btns[i].click();
                return true;
            }
        }
        return false;
    """)
    if clicked:
        time.sleep(1)
        print("    Book Now clicked (post-login)")
    else:
        print("    WARN: Book Now button not found")


def step3_check_availability(d):
    print("[3] Filling availability form...")
    dismiss_chat_popup(d)
    time.sleep(1)

    date_field = d.find_element(By.ID, "select_date")
    d.execute_script(
        "arguments[0].value='2026-04-25'; arguments[0].dispatchEvent(new Event('change'));",
        date_field
    )

    nop = d.find_element(By.ID, "nop")
    nop.clear()
    nop.send_keys(str(NUM_ADULTS))

    try:
        noc = d.find_element(By.ID, "noc")
        noc.clear()
        noc.send_keys(str(NUM_CHILDREN))
    except Exception:
        pass

    try:
        js_click(d, d.find_element(By.CSS_SELECTOR, "button[onclick*='validateavailabity']"))
    except Exception:
        try:
            d.find_element(By.ID, "available").submit()
        except Exception:
            pass

    WebDriverWait(d, WAIT).until(
        lambda dr: dr.execute_script("return document.readyState") == "complete"
    )
    time.sleep(0.5)
    print(f"    Availability checked. URL: {d.current_url}")


def step4_click_first_book(d):
    print("[4] Clicking first 'Book Now' in availability list...")
    dismiss_chat_popup(d)
    time.sleep(0.5)

    book_btns = d.find_elements(By.CSS_SELECTOR, "a.btn, button.btn, a.btn-style, button.btn-style")
    for btn in book_btns:
        txt = btn.text.strip()
        if "book now" in txt.lower() or "book" in txt.lower():
            if btn.is_displayed():
                js_click(d, btn)
                WebDriverWait(d, WAIT).until(
                    lambda dr: dr.execute_script("return document.readyState") == "complete"
                )
                print(f"    Clicked: {txt}")
                print(f"    URL: {d.current_url}")
                return True

    rows = d.find_elements(By.CSS_SELECTOR, "table tr td a, table tr td button")
    for r in rows:
        txt = r.text.strip()
        if "book" in txt.lower():
            js_click(d, r)
            WebDriverWait(d, WAIT).until(
                lambda dr: dr.execute_script("return document.readyState") == "complete"
            )
            print(f"    Clicked table action: {txt}")
            return True

    print("    WARN: No Book Now found in list. Page buttons:")
    for btn in d.find_elements(By.CSS_SELECTOR, "button, a.btn"):
        if btn.is_displayed():
            print(f"      [{btn.tag_name}] {btn.text.strip()[:50]}")
    return False


def _find_section(d, heading_text):
    """Find a form section by its heading text (e.g. 'Devotee Details')."""
    headings = d.find_elements(By.XPATH,
        f"//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        f"'{heading_text.lower()}')]"
    )
    for h in headings:
        parent = h
        for _ in range(5):
            parent = parent.find_element(By.XPATH, "..")
            inputs = parent.find_elements(By.CSS_SELECTOR, "input, select")
            if len(inputs) >= 3:
                return parent
    return None


def _fresh_fields(d, section_xpath, tag, attr_hint):
    """Re-query fields each time to avoid stale references."""
    if section_xpath:
        base = d.find_element(By.XPATH, section_xpath)
    else:
        base = d
    return base.find_elements(By.CSS_SELECTOR, f"{tag}[name*='{attr_hint}']")


def step5_fill_devotees(d):
    print(f"[5] Filling {len(ADULTS)} devotee details...")
    WebDriverWait(d, WAIT).until(
        lambda dr: any(
            "devotee" in el.text.lower()
            for el in dr.find_elements(By.CSS_SELECTOR, "h1,h2,h3,h4,h5,h6,label,legend,span,div,p,b,strong")
        )
    )
    time.sleep(1)
    dismiss_chat_popup(d)

    section = _find_section(d, "Devotee Details")
    if section:
        section_xpath = d.execute_script(
            "var e=arguments[0],p='';while(e&&e.nodeType===1){"
            "var idx=0,sib=e;while(sib){if(sib.nodeType===1)idx++;sib=sib.previousSibling;}"
            "p='/'+e.tagName.toLowerCase()+'['+idx+']'+p;e=e.parentNode;}return p;",
            section
        )
        print(f"    Found 'Devotee Details' section")
    else:
        section_xpath = None
        print("    WARN: Could not locate Devotee Details section, using whole page")

    page_html = d.page_source.lower()
    print(f"    Page has 'devotee' mention: {'devotee' in page_html}")

    for i, (name, gender, age, aadhar) in enumerate(ADULTS):
        time.sleep(0.3)
        name_fields = [
            el for el in d.find_elements(By.CSS_SELECTOR,
                "input[name*='name'], input[placeholder*='Name'], input[placeholder*='name']"
            ) if el.get_attribute("type") != "hidden" and el.is_displayed()
        ]
        gender_fields = d.find_elements(By.CSS_SELECTOR,
            "select[name*='gender'], select[name*='Gender']"
        )
        age_fields = [
            el for el in d.find_elements(By.CSS_SELECTOR,
                "input[name*='age'], input[placeholder*='Age'], input[placeholder*='age']"
            ) if el.get_attribute("type") != "hidden" and el.is_displayed()
        ]
        aadhar_fields = [
            el for el in d.find_elements(By.CSS_SELECTOR,
                "input[name*='aadhar'], input[name*='aadhaar'], input[name*='adhar'],"
                " input[placeholder*='Aadhar'], input[placeholder*='Aadhaar'], input[placeholder*='adhar']"
            ) if el.get_attribute("type") != "hidden" and el.is_displayed()
        ]
        if i == 0:
            print(f"    Found: {len(name_fields)} name, {len(gender_fields)} gender, {len(age_fields)} age, {len(aadhar_fields)} aadhar fields")

        if i < len(name_fields):
            try:
                name_fields[i].clear()
                name_fields[i].send_keys(name)
            except Exception:
                pass

        if i < len(gender_fields):
            try:
                select_dropdown(gender_fields[i], gender)
            except Exception:
                pass

        if i < len(age_fields):
            try:
                age_fields[i].clear()
                age_fields[i].send_keys(age)
            except Exception:
                pass

        if i < len(aadhar_fields):
            try:
                aadhar_fields[i].clear()
                aadhar_fields[i].send_keys(aadhar)
            except Exception:
                pass

        print(f"    [{i+1}] {name}, {gender}, {age}, Aadhar: {aadhar}")


def main():
    print("=" * 50)
    print("Mangla Aarti Booking - 25 April 2026")
    print(f"Adults: {NUM_ADULTS}, Children: {NUM_CHILDREN}, Children: {NUM_CHILDREN}")
    print("=" * 50)

    d = driver_init()

    try:
        step1_login(d)
        step2_book_now(d)
        step3_check_availability(d)
        step4_click_first_book(d)
        step5_fill_devotees(d)

        print("\n[DONE] All fields filled. Review in browser.")
        input("Press Enter to close browser (or Ctrl+C to keep it open)...")

    except KeyboardInterrupt:
        print("\nBrowser left open.")
        input("Press Enter when done...")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close browser...")
    finally:
        d.quit()


if __name__ == "__main__":
    main()
