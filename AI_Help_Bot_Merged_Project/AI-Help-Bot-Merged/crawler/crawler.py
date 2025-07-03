import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def crawl_faq():
    options = Options()
    options.add_argument('--headless')  # for background mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.mosdac.gov.in/help")
    wait = WebDriverWait(driver, 10)

    faqs = []
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.field-item.even")))

        content_div = driver.find_element(By.CSS_SELECTOR, "div.field-item.even")
        all_elements = content_div.find_elements(By.XPATH, "./*")  # All direct children

        question = None
        answer_parts = []

        for elem in all_elements:
            tag_name = elem.tag_name.lower()
            text = elem.text.strip()

            if tag_name == "h3":
                if question and answer_parts:
                    answer = " ".join(answer_parts).strip()
                    faqs.append({"question": question, "answer": answer})
                question = text
                answer_parts = []
            elif question:
                if text:
                    answer_parts.append(text)

        if question and answer_parts:
            answer = " ".join(answer_parts).strip()
            faqs.append({"question": question, "answer": answer})

    except Exception as e:
        print("⚠️ Error locating FAQ section:", e)
    finally:
        driver.save_screenshot("faq_page_debug.png")
        driver.quit()
        print(f"✅ FAQs found: {len(faqs)}")
        return faqs
