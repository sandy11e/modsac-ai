from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")  # Comment this out if you want to see the browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ Correct usage with Service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the MOSDAC Help page
driver.get("https://www.mosdac.gov.in/help")

# Dump the page HTML
with open("mosdac_help_dump.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("✅ Dumped page source to mosdac_help_dump.html")
