from flask import Flask, request, jsonify, send_from_directory
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

app = Flask(__name__, static_url_path='/static')

# Initialize the URL queue
url_queue = []

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route('/addurl', methods=['POST'])
def add_url():
    url = request.json['url']
    url_queue.append(url)
    return jsonify({'message': 'URL added to the queue.'})

@app.route('/startdownload', methods=['POST'])
def start_download():
    urls = request.json['urls']

    # Create Chrome options and set the binary location to your custom path
    chrome_binary_path = "./chrome-win/chrome.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary_path
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--force-device-scale-factor=0.7")

    # Create a new Chrome driver instance using the custom binary
    driver = webdriver.Chrome(options=options)

    def every_downloads_chrome(driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """)

    for url in urls:
        driver.get(url)  # Open the URL

        # Click on the "More..." link
        try:
            more_link = driver.find_element(By.CSS_SELECTOR, 'a[onclick="showHashData(this); return false"]')
            driver.execute_script("arguments[0].scrollIntoView();", more_link)
            more_link.click()
        except NoSuchElementException:
            pass  # Handle the case if the "More..." link is not present

        # Wait for a short duration to ensure the page settles
        time.sleep(2)

        # Locate the download button again and click it
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"][style="width:100%"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()

        # Wait for the download to start before navigating to chrome://downloads/
        time.sleep(5)  # Sleep for 5 seconds

        # Wait for the download to complete with a timeout of 8 hours
        WebDriverWait(driver, 28800, 10).until(every_downloads_chrome)

        # Time to wait before looping
        time.sleep(5)  # Sleep for 5 seconds

    # Quit the driver when done
    driver.quit()

    return jsonify({'message': 'URL queue processed successfully.'})

if __name__ == '__main__':
    app.run(debug=False)
