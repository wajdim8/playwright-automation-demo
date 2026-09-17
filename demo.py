from playwright.sync_api import sync_playwright
from datetime import datetime
import json

FORM_URL = "https://www.selenium.dev/selenium/web/web-form.html"


def log(message):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {message}")


def main():
    result = {
        "status": "FAILED",
        "submitted_value": None,
        "page_message": None
    }

    with sync_playwright() as p:
        log("Starting browser...")
        browser = p.chromium.launch(
            headless=False,
            slow_mo=400
        )

        page = browser.new_page(
            viewport={"width": 1280, "height": 800}
        )

        try:
            log("Opening test web portal...")
            page.goto(
                FORM_URL,
                wait_until="domcontentloaded",
                timeout=30000
            )

            log("Waiting for form...")
            text_box = page.locator('input[name="my-text"]')
            text_box.wait_for(state="visible", timeout=10000)

            submitted_value = "Wajdi Python Automation Demo"

            log("Entering data...")
            text_box.fill(submitted_value)

            log("Selecting an option...")
            page.locator('select[name="my-select"]').select_option(
                label="Two"
            )

            log("Checking form option...")
            page.locator("#my-check-1").check()

            # Screenshot before submission
            page.screenshot(
                path="01_form_filled.png",
                full_page=True
            )

            log("Submitting form...")
            page.get_by_role("button", name="Submit").click()

            log("Waiting for response...")
            message = page.locator("#message")
            message.wait_for(state="visible", timeout=10000)

            page_message = message.inner_text()

            log(f"Response received: {page_message}")

            # Screenshot after submission
            page.screenshot(
                path="02_submission_result.png",
                full_page=True
            )

            result["status"] = "SUCCESS"
            result["submitted_value"] = submitted_value
            result["page_message"] = page_message

        except Exception as exc:
            log(f"ERROR: {exc}")
            result["error"] = str(exc)

            try:
                page.screenshot(
                    path="error.png",
                    full_page=True
                )
            except Exception:
                pass

        finally:
            with open(
                "automation_result.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    result,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            log("Result saved to automation_result.json")
            log("Demo completed.")

            page.wait_for_timeout(3000)
            browser.close()


if __name__ == "__main__":
    main()