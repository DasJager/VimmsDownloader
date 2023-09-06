from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import mysql.connector
from mysql.connector import errorcode
import logging
import sys
import traceback
import random

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="queue"
    )

# Global variables for Selenium driver
driver = None


# Global variable to keep track of completed downloads
downloads_completed = 0

def retrieve_queued_urls():
    db_connection = get_db_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT url FROM queued_urls")
        urls = [row[0] for row in cursor.fetchall()]
        return urls
    except mysql.connector.Error as err:
        logging.error("Error retrieving queued URLs: %s", err)
    except Exception as e:
        raise Exception("An error occurred while retrieving queued URLs: " + str(e))
    finally:
        if cursor:
            cursor.close()
        db_connection.close()

    return []

def retrieve_completed_urls():
    db_connection = get_db_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT url, filename FROM completed_urls")
        urls = [{"url": row[0], "filename": row[1]} for row in cursor.fetchall()]
        return urls
    except mysql.connector.Error as err:
        logging.error("Error retrieving completed URLs: %s", err)
    except Exception as e:
        raise Exception("An error occurred while retrieving completed URLs: " + str(e))
    finally:
        if cursor:
            cursor.close()
        db_connection.close()

    return []

def save_url_to_database(url):
    db_connection = get_db_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO queued_urls (url) VALUES (%s)", (url,))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        raise Exception("Error saving URL to database: " + str(e))
    finally:
        db_connection.close()

def remove_url_from_queue(url):
    db_connection = get_db_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM queued_urls WHERE url = %s", (url,))
        db_connection.commit()
        time.sleep(1)  # Add a delay of 1 second
    except mysql.connector.Error as err:
        logging.error("Error removing URL from queue: %s", err)
        raise Exception("An error occurred while removing URL from the queue.")
    finally:
        if cursor:
            cursor.close()
        db_connection.close()

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Add a route to serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route('/initialdata')
def get_initial_data():
    queued_urls = retrieve_queued_urls()
    completed_urls = retrieve_completed_urls()
    return jsonify({'queued_urls': queued_urls, 'completed_urls': completed_urls})

@app.route('/addurl', methods=['POST'])
def add_url():
    urls = request.get_json()['urls'][:40]
    for url in urls:
        try:
            print(f"Saving URL to database: {url}")
            save_url_to_database(url)
            print(f"URL saved to database: {url}")
        except Exception as e:
            print(f"Error saving URL to database: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    queued_urls = retrieve_queued_urls()
    return jsonify({'message': 'URLs added to the queue.', 'queued_urls': queued_urls})
    
    
    # Function to check if a download is complete
def is_download_complete(download_path, filename):
    while not os.path.exists(os.path.join(download_path, filename)):
        time.sleep(1)
    
    while os.path.exists(os.path.join(download_path, filename + ".crdownload")):
        time.sleep(1)

    # Function to get the filename from the webpage
def get_filename_from_webpage(driver):
    title_element = driver.find_element(By.CSS_SELECTOR, '#data-good-title')
    filename = title_element.text
    return filename.replace('.iso', '.7z')

@socketio.on('start_download')
def start_download(message):
    global driver
    global downloads_completed

    urls = message['urls']
    total_urls = len(urls)
    downloads_completed = 0
    print("Starting download for URLs: ", urls)

    if driver is None:
     # Create Chrome options and set the binary location to your custom path
        chrome_binary_path = "./chrome-win/chrome.exe"
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_binary_path
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--start-maximized")  # Put WebDriver in full-screen mode
        options.add_argument("--disable-infobars")  # Disable infobars
        options.add_argument("--force-device-scale-factor=0.7") # zoom the page 70% and prevent add clicking id="footerAd"
          # Path to your chrome profile
        #options.add_argument("user-data-dir=C:\\Users\\roger\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
        #options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')  # Set a realistic user-agent
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Create a new Chrome driver instance using the custom binary
        driver = webdriver.Chrome(options=options)


    try:
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

            
            filename = get_filename_from_webpage(driver)  # Get the filename

            # Check if the download is complete
            is_download_complete('C:\\Users\\roger\\Downloads', filename)


        
            # Time to wait before looping
            sleep_time = random.randint(5, 30)  # Random time between 5 and 30 seconds
            print(f"Waiting for {sleep_time} seconds before next download...")
            time.sleep(sleep_time)

            # Remove completed URL from the queue
            try:
                remove_url_from_queue(url)
                db_connection = get_db_connection()
                cursor = db_connection.cursor()
                cursor.execute("INSERT INTO completed_urls (url, filename) VALUES (%s, %s)", (url, filename))
                db_connection.commit()
                # Emit an event with the updated list of completed URLs
                completed_urls = retrieve_completed_urls()
                print("URL download completed, moving URL from queue to completed list: ", url)
                print("Emitting 'update_completed' with data: ", {'completed_urls': completed_urls})
                emit('update_completed', {'completed_urls': completed_urls})
                downloads_completed += 1
            except Exception as e:
                emit('download_error', str(e))


        
            if downloads_completed == total_urls:
                # Close the WebDriver
                driver.quit()
                driver = None

    except Exception as e:
        logging.error("Error during download process: %s", e)
        traceback.print_exc(file=sys.stdout)  # Print the traceback
        emit('download_error', 'An error occurred during the download process.')

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('ready')
def handle_ready():
    print("Client is ready")
    queued_urls = retrieve_queued_urls()
    completed_urls = retrieve_completed_urls()
    print("Emitting 'initial_data' with data: ", {'queued_urls': queued_urls, 'completed_urls': completed_urls})
    emit('initial_data', {'queued_urls': queued_urls, 'completed_urls': completed_urls})


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(filename='app.log', level=logging.ERROR)

    try:
        socketio.run(app, debug=False, port=5000)
    except Exception as e:
        logging.error("Flask application error: %s", e)