Vimm's Lair Downloader Queue Server
A Flask-based server application that interfaces with a Selenium WebDriver to automate downloading tasks from Vimm's Lair, while maintaining a queue of URLs and a record of completed downloads.

Features:
Web-based interface to add URLs to a download queue.
Real-time updates on the status of downloads.
Records completed downloads with associated filenames.
Uses Flask-SocketIO for real-time communication between the server and clients.
Uses Selenium WebDriver for browser automation.



Installation:



Prerequisites:
Apache web service 
mysql database 
Python 3.x
Chrome WebDriver
Steps:
Create the database & tables 


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

Clone the Repository



git clone https://github.com/DasJager/VimmsDownloader.git
cd VimmsDownloader
Set up a Virtual Environment:


pip install virtualenv
virtualenv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
Install Required Packages:


pip install -r requirements.txt
Set up the Database:
Make sure you have MySQL installed and running. Then create the necessary tables using the provided SQL script.

Run the Server:


python main.py  # Or however you named your main server script

Usage:
Navigate to http://localhost:5000/ in your browser.
Add URLs (one per line, up to 40 URLs) to the queue.
Press the "Start Download" button to initiate the download process.
Monitor the progress on the web interface.
Contributing:
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License:
MIT






