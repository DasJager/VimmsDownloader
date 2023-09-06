**Vimm's Lair Downloader Queue Server**
A Flask-based server application that interfaces with a Selenium WebDriver to automate downloading games from Vimm's Lair. The application maintains a queue of URLs and a record of completed downloads. I would appreciate if anyone who forks this project to keep the core values alive which include but are not limited to keep the ads viewable and ensue that vimms gets real views so they do not lose any profit from ad revenue. Please respect vimms 1 download session per person as I have develpoed this script to do, please do not use any proxy services. As this will most likely it would rob vimms of their ad revenue. 

**Features:**

**Web Interface:** Easily add URLs to a download queue.

**Real-time Updates:** Monitor the status of ongoing downloads in real-time.

**Record Keeping:** Keep track of completed downloads with associated filenames.

**Real-time Communication:** Utilizes Flask-SocketIO for real-time communication between the server and clients.

**Automation:** Uses Selenium WebDriver for browser automation.

**Installation:**

**Prerequisites:**

Apache web service - not needed if you just intend to use the server to send static files 

MySQL database - I recommend Xampp as it is the easiest to use and this is not a production environment https://www.apachefriends.org/

[Python 3.x](https://www.python.org/downloads/)


Chrome WebDriver - Chrome is already included as this is a some what stand alone package

**Steps:**

**1. Create the Database & Tables:
**


CREATE DATABASE queue;

USE queue;

CREATE TABLE queued_urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL
);

CREATE TABLE completed_urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL
);


**2. Clone the Repository:**
    
    
    git clone https://github.com/DasJager/VimmsDownloader.git
    cd VimmsDownloader

**3. Set up a Virtual Environment:**

python -m venv venv


venv\Scripts\Activate

**4.Install Required Packages:**
    
    
    pip install -r requirements.txt


**5.Set up the Database:**

Make sure you have MySQL installed and running. Then create the necessary tables using the provided SQL script provided in step 1.

**6.Run the Server:**

python app.py  # Or however you named your app server script

**Usage:**


Navigate to http://localhost:5000/ in your browser.
Add URLs (one per line, up to 40 URLs) to the queue.
Press the "Start Download" button to initiate the download process.
Monitor the progress on the web interface.


**Contributing:**


Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

**License:**


[MIT]([url](https://choosealicense.com/licenses/mit/)



![how to use](https://github.com/DasJager/VimmsDownloader/blob/46aca0b5e17513f976c033a950d6e4c4cca94016/how-to-use-VimmDownloader.gif)



**Donations**


    if you like my work or this tool has been helpful to you buy me a coffe/beer
**    my wallet address **


eth: 0x3535E89F33DA8892857eCB925434444B24141F2a
solana: 6d7Npf19vUrDWaMHWeHVEiXBcJXLHqgrUavtwEw4m3qt
Doge: D5H4ADNWcn1HaPpR5sizZuBX72HpMjvLeC


    

