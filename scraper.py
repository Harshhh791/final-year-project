from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials, firestore
import schedule
import time

# ===================== 🔥 Initialize Firebase =====================
print("Initializing Firebase...")
cred = credentials.Certificate(r"H:\Last year\Scholarship_Prediction\Scholarship_Prediction\firebase_config.json")

try:
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully!")
except Exception as e:
    print("❌ Firebase initialization failed:", str(e))
    exit(1)

# ===================== 🌐 Selenium WebDriver Setup =====================
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
service = Service(r"H:\Last year\Scholarship_Prediction\Scholarship_Prediction\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# ===================== 📌 Web Scraping Function =====================
def scrape_scholarships():
    print("\n🚀 Starting web scraping...")

    url = "https://buddy4study.com/scholarships"
    driver.get(url)

    # Wait until scholarships load
    wait = WebDriverWait(driver, 10)

    try:
        # Extract scholarship names and links
        scholarship_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a h4.Listing_scholarshipName__VLFMj"))
        )
        scholarships = []

        for scholarship in scholarship_elements:
            title = scholarship.text
            link = scholarship.find_element(By.XPATH, "./ancestor::a").get_attribute("href")

            # Store in Firestore
            data = {
                "title": title,
                "link": link
            }
            scholarships.append(data)

        # Save data to Firebase Firestore
        if scholarships:
            for scholarship in scholarships:
                db.collection("scholarship").add(scholarship)
            print(f"✅ {len(scholarships)} Scholarships added successfully!")
        else:
            print("⚠️ No scholarships found.")

    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")

# ===================== ⏳ Scheduler Setup =====================
schedule.every(1).minute.do(scrape_scholarships)  # Runs every minute

# Print scheduled jobs
print("🕒 Scheduled Jobs:", schedule.get_jobs())

# Run the scheduler continuously
while True:
    schedule.run_pending()
    time.sleep(60)