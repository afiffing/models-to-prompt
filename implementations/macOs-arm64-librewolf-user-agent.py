"""
Mangla Aarti Booking - Shri Kashi Vishwanath Temple
Selenium + LibreWolf

Flow:
  1. Open pooja page -> click Book Now -> login
  2. Re-open pooja page -> click Book Now (post-login)
  3. Fill adults/children count -> Check Availability
  4. Click first "Book Now" in availability list
  5. Fill devotee details (name, gender, age)
  6. Fill child details (name, gender, age)

pip3 install selenium webdriver-manager
"""

import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

LIBREWOLF_BIN = "/Applications/LibreWolf.app/Contents/MacOS/librewolf"
GECKODRIVER_PATH = "/Users/ashishsingh/.wdm/drivers/geckodriver/mac64/v0.36.0/geckodriver"

POOJA_PAGE = "https://shrikashivishwanath.org/frontend/home/poojadetail/c1M2MS9DUG1ydzZQVVFqT0w0SVNydz09/2026-03-27"

#POOJA_PAGE = "https://shrikashivishwanath.org/frontend/home/poojadetail/U3ViQWhsYms2WUoydkx5VkhvazgxUT09"


EMAIL = "xyz@gmail.com"
PASSWORD = "12345#"

NUM_ADULTS = 5
NUM_CHILDREN = 1

ADULTS = [
    ("Name1", "Male", "35", "AadharNumber1"),
    ("Name2", "Female", "32","AadharNumber2"),
    ("Name3", "Male", "35","AadharNumber3"),
    ("Name4", "Female", "33","AadharNumber4"),
    ("Name5", "Female", "65","AadharNumber5"),
]

CHILDREN = [
    ("Name6", "Female", "Below 1 Year"),
]

WAIT = 10


def driver_init():
    opts = Options()
    opts.binary_location = LIBREWOLF_BIN
    opts.set_preference("browser.display.use_document_fonts", 0)
    opts.set_preference("network.http.pipelining", True)
    opts.set_preference("network.http.proxy.pipelining", True)
    opts.page_load_strategy = "eager"
    svc = Service(GECKODRIVER_PATH)
    d = webdriver.Firefox(service=svc, options=opts)
    d.fullscreen_window()
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


def step1_login(d):
    print("[1] Opening pooja page & logging in...")
    d.get(POOJA_PAGE)
    WebDriverWait(d, WAIT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-style[data-target='#loginModal']"))
    ).click()

    WebDriverWait(d, WAIT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#passform"))
    )

    try:
        d.find_element(By.ID, "loginh4").click()
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

    d.find_element(By.CSS_SELECTOR, "#passform button[type='submit']").click()
    WebDriverWait(d, WAIT).until(EC.url_changes(POOJA_PAGE))
    print(f"    Logged in. URL: {d.current_url}")


def step2_book_now(d):
    print("[2] Re-opening pooja page & clicking Book Now...")
    d.get(POOJA_PAGE)
    WebDriverWait(d, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-style"))
    )

    for btn in d.find_elements(By.CSS_SELECTOR, "button.btn-style"):
        if "book now" in btn.text.strip().lower():
            btn.click()
            time.sleep(0.5)
            print("    Book Now clicked (post-login)")
            return
    print("    WARN: Book Now button not found")


def step3_check_availability(d):
    print("[3] Filling availability form...")
    time.sleep(1)

    date_field = d.find_element(By.ID, "select_date")
    d.execute_script(
        "arguments[0].value='2026-03-27'; arguments[0].dispatchEvent(new Event('change'));",
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
        d.find_element(By.CSS_SELECTOR, "button[onclick*='validateavailabity']").click()
    except Exception:
        d.find_element(By.ID, "available").submit()

    WebDriverWait(d, WAIT).until(
        lambda dr: dr.execute_script("return document.readyState") == "complete"
    )
    time.sleep(0.5)
    print(f"    Availability checked. URL: {d.current_url}")


def step3b_fill_child_count(d):
    print("[3b] Looking for 'No. Of Child(s)' field after availability check...")
    time.sleep(0.5)

    noc = None

    labels = d.find_elements(By.XPATH,
        "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'no. of child')]"
    )
    for label in labels:
        field_id = label.get_attribute("for")
        if field_id:
            try:
                noc = d.find_element(By.ID, field_id)
                break
            except Exception:
                pass
        try:
            parent = label.find_element(By.XPATH, "..")
            noc = parent.find_element(By.CSS_SELECTOR, "input, select")
            break
        except Exception:
            pass

    if not noc:
        for sel in ["input[name*='noc'], input[name*='child']",
                     "input[placeholder*='Child'], input[placeholder*='child']",
                     "select[name*='noc'], select[name*='child']",
                     "#noc"]:
            fields = d.find_elements(By.CSS_SELECTOR, sel)
            for f in fields:
                if f.is_displayed():
                    noc = f
                    break
            if noc:
                break

    if noc:
        noc.clear()
        noc.send_keys(str(NUM_CHILDREN))
        print(f"    Set 'No. Of Child(s)' to {NUM_CHILDREN}")
    else:
        print("    WARN: Could not find 'No. Of Child(s)' field")

    submit_btn = None
    for btn in d.find_elements(By.CSS_SELECTOR, "button, input[type='submit']"):
        txt = btn.text.strip().lower() if btn.tag_name == "button" else (btn.get_attribute("value") or "").lower()
        if btn.is_displayed() and ("submit" in txt or "check" in txt or "search" in txt or "go" in txt):
            submit_btn = btn
            break

    if submit_btn:
        submit_btn.click()
        print(f"    Submitted: {submit_btn.text.strip() if submit_btn.tag_name == 'button' else submit_btn.get_attribute('value')}")
    elif noc:
        try:
            noc.find_element(By.XPATH, "ancestor::form").submit()
            print("    Submitted parent form")
        except Exception:
            print("    WARN: Could not find submit button, tried form submit")

    time.sleep(0.5)
    WebDriverWait(d, WAIT).until(
        lambda dr: dr.execute_script("return document.readyState") == "complete"
    )
    print(f"    Done. URL: {d.current_url}")


def step4_click_first_book(d):
    print("[4] Clicking first 'Book Now' in availability list...")
    time.sleep(0.5)

    book_btns = d.find_elements(By.CSS_SELECTOR, "a.btn, button.btn, a.btn-style, button.btn-style")
    for btn in book_btns:
        txt = btn.text.strip()
        if "book now" in txt.lower() or "book" in txt.lower():
            if btn.is_displayed():
                btn.click()
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
            r.click()
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


def step6_fill_children(d):
    print(f"[6] Filling {len(CHILDREN)} child details...")
    time.sleep(1)

    child_section = _find_section(d, "Child Detail")
    if child_section:
        print("    Found 'Child Details' section")
    else:
        print("    WARN: Could not locate Child Details section, searching whole page")

    for i, (name, gender, age_text) in enumerate(CHILDREN):
        time.sleep(0.3)

        child_name_fields = d.find_elements(By.CSS_SELECTOR,
            "input[name*='child_name'], input[name*='childname'], input[name*='cname']"
        )
        child_gender_fields = d.find_elements(By.CSS_SELECTOR,
            "select[name*='child_gender'], select[name*='childgender'], select[name*='cgender']"
        )
        child_age_fields = d.find_elements(By.CSS_SELECTOR,
            "select[name*='child_age'], select[name*='childage'], select[name*='cage'], "
            "input[name*='child_age'], input[name*='childage']"
        )

        if not child_name_fields:
            child_sections = d.find_elements(By.CSS_SELECTOR, "[id*='child'], [class*='child']")
            for sec in child_sections:
                child_name_fields = sec.find_elements(By.CSS_SELECTOR, "input[type='text']")
                child_gender_fields = sec.find_elements(By.CSS_SELECTOR, "select")
                if child_name_fields:
                    break

        if i == 0:
            print(f"    Found: {len(child_name_fields)} name, {len(child_gender_fields)} gender, {len(child_age_fields)} age fields")

        if i < len(child_name_fields):
            try:
                child_name_fields[i].clear()
                child_name_fields[i].send_keys(name)
            except Exception:
                try:
                    el = d.find_elements(By.CSS_SELECTOR, "input[name*='child_name'], input[name*='childname'], input[name*='cname']")[i]
                    el.clear()
                    el.send_keys(name)
                except Exception:
                    pass

        if i < len(child_gender_fields):
            try:
                select_dropdown(child_gender_fields[i], gender)
            except Exception:
                try:
                    fresh = d.find_elements(By.CSS_SELECTOR, "select[name*='child_gender'], select[name*='childgender'], select[name*='cgender']")[i]
                    select_dropdown(fresh, gender)
                except Exception:
                    pass

        if i < len(child_age_fields):
            try:
                sel = Select(child_age_fields[i])
                for opt in sel.options:
                    if "below" in opt.text.lower() and "1" in opt.text:
                        sel.select_by_visible_text(opt.text)
                        break
            except Exception:
                try:
                    fresh = d.find_elements(By.CSS_SELECTOR, "select[name*='child_age'], select[name*='childage'], select[name*='cage']")[i]
                    sel = Select(fresh)
                    for opt in sel.options:
                        if "below" in opt.text.lower() and "1" in opt.text:
                            sel.select_by_visible_text(opt.text)
                            break
                except Exception:
                    pass

        print(f"    [C{i+1}] {name}, {gender}, {age_text}")


def main():
    print("=" * 50)
    print("Mangla Aarti Booking - 25 April 2026")
    print(f"Adults: {NUM_ADULTS}, Children: {NUM_CHILDREN}")
    print("=" * 50)

    d = driver_init()

    try:
        step1_login(d)
        step2_book_now(d)
        step3_check_availability(d)
        step3b_fill_child_count(d)
        step4_click_first_book(d)
        step5_fill_devotees(d)
        step6_fill_children(d)

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
