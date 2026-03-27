#!/usr/bin/env python3
"""
WhatsApp Web Group Creation - Safari + Selenium + JSON Config

Features:
- Login via phone number + OTP
- Create group with custom title
- Add multiple members

Requirements:
  pip3 install selenium

Usage:
  python3 whatsappWeb-create-group.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
import time
import json


def load_config():
    """Load configuration from config.json"""
    with open("config.json", "r") as f:
        return json.load(f)


def safe_click(driver, element, max_retries=3):
    """Safely click an element with retry logic and JavaScript fallback"""
    for attempt in range(max_retries):
        try:
            # Scroll element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)

            # Try Selenium click
            element.click()
            return
        except (StaleElementReferenceException, WebDriverException) as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            # Last attempt: use JavaScript click
            try:
                driver.execute_script("arguments[0].click();", element)
            except:
                raise e


def login_with_qr(driver, wait_timeout, qr_scan_timeout):
    """Step 1: Login via QR code scan"""
    print("[STEP 1] Login with QR Code")
    print("=" * 50)

    print("Opening WhatsApp Web...")
    driver.get("https://web.whatsapp.com")
    time.sleep(2)

    print("\n📱 QR Code displayed on screen")
    print(f"⏳ Waiting for QR scan ({qr_scan_timeout} seconds)...\n")
    print("Scan the QR code with your WhatsApp phone...\n")

    # Use qr_scan_timeout for QR code wait
    qr_wait = WebDriverWait(driver, qr_scan_timeout)
    qr_wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'New chat')] | //*[@aria-label='Chats']"))
    )
    print("✅ Scan successful! Logged in.\n")
    time.sleep(2)


def create_group(driver, group_title, wait_timeout, action_delay):
    """Step 2: Create group via menu dots"""
    print("[STEP 2] Create Group")
    print("=" * 50)

    wait = WebDriverWait(driver, wait_timeout)

    print("Clicking menu dots (⋯)...")
    menu_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Menu']"))
    )
    safe_click(driver, menu_button)
    time.sleep(action_delay)

    print("Clicking 'New group'...")
    new_group_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'New group')]"))
    )
    safe_click(driver, new_group_option)
    time.sleep(action_delay)

    print("✅ Group creation dialog opened\n")


def add_members_to_group(driver, members_list, wait_timeout, action_delay):
    """Step 3: Add members to group"""
    print("[STEP 3] Add Members to Group")
    print("=" * 50)

    wait = WebDriverWait(driver, wait_timeout)

    for idx, member_phone in enumerate(members_list, 1):
        print(f"Adding member {idx}/{len(members_list)}: {member_phone}...")

        search_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        search_input.clear()
        search_input.send_keys(member_phone)
        time.sleep(2)

        # Click the search result that matches the phone number
        print(f"  Clicking search result for {member_phone}...")
        time.sleep(2)  # Wait for results to render

        # Check if results exist before trying to select
        results_exist = driver.execute_script("""
            // Check if there are any contact results visible
            let results = document.querySelectorAll('[role="button"]');
            let contactResults = Array.from(results).filter(btn => {
                let rect = btn.getBoundingClientRect();
                return rect.height > 30 && rect.top > 100; // Rough filter
            });
            return contactResults.length > 0;
        """)

        if not results_exist:
            print(f"  ⚠️  No search results found for: {member_phone}")
            print(f"  ⚠️  Make sure '{member_phone}' is saved in WhatsApp contacts")
            search_input.clear()
            time.sleep(0.5)
            continue

        # Use keyboard navigation to select the first result
        # Press Arrow Down to highlight first result, then Enter to select
        search_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        search_input.send_keys(Keys.RETURN)

        time.sleep(action_delay)
        print(f"  ✅ Added: {member_phone}")

    print("\n✅ All members added\n")

    print("Clicking 'Next' (green arrow button)...")
    # Find div with role="button" and aria-label="Next" containing SVG with arrow icon
    next_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@role='button' and @aria-label='Next']"))
    )
    safe_click(driver, next_button)
    time.sleep(action_delay)


def set_group_title(driver, group_title, wait_timeout, action_delay):
    """Step 4: Set group title and create"""
    print("[STEP 4] Set Group Title & Create")
    print("=" * 50)

    wait = WebDriverWait(driver, wait_timeout)

    print(f"Entering group title: '{group_title}'...")
    # Find the contenteditable div for group title
    group_name_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@contenteditable='true' and @aria-label[contains(., 'Group subject')]]"))
    )

    # Click to focus
    safe_click(driver, group_name_input)
    time.sleep(0.5)

    # Select all and clear
    group_name_input.send_keys(Keys.COMMAND + "a")
    time.sleep(0.2)
    group_name_input.send_keys(Keys.DELETE)
    time.sleep(0.3)

    # Type the group title
    group_name_input.send_keys(group_title)
    time.sleep(action_delay)

    print("Creating group...")
    # Click the "Create group" button
    create_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@role='button' and @aria-label='Create group']"))
    )
    safe_click(driver, create_button)
    time.sleep(3)

    print(f"✅ Group '{group_title}' created successfully!\n")


def main():
    """Main automation workflow"""
    config = load_config()

    login_config = config["login"]
    groups_config = config["group"]
    members_config = config["members"]
    auto_config = config["automation"]

    driver = webdriver.Safari()
    driver.maximize_window()

    try:
        print("\n" + "=" * 50)
        print("WhatsApp Web Group Automation")
        print("=" * 50 + "\n")

        # Login once
        login_with_qr(
            driver,
            auto_config["wait_timeout"],
            login_config["qr_scan_timeout"]
        )

        # Create each group
        for idx, group_config in enumerate(groups_config, 1):
            print(f"\n{'='*50}")
            print(f"Creating Group {idx}/{len(groups_config)}")
            print(f"{'='*50}\n")

            create_group(
                driver,
                group_config["title"],
                auto_config["wait_timeout"],
                auto_config["action_delay"]
            )

            add_members_to_group(
                driver,
                members_config["to_add"],
                auto_config["wait_timeout"],
                auto_config["action_delay"]
            )

            set_group_title(
                driver,
                group_config["title"],
                auto_config["wait_timeout"],
                auto_config["action_delay"]
            )

            print(f"✅ Group '{group_config['title']}' created with {len(members_config['to_add'])} member(s)\n")

        print("=" * 50)
        print("✅ ALL GROUPS CREATED!")
        print("=" * 50)
        print(f"\nTotal groups created: {len(groups_config)}")
        print(f"Groups: {', '.join([g['title'] for g in groups_config])}\n")

        input("Press Enter to close browser...")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to close browser...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
