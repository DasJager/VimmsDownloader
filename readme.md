Vimm's Lair Downloader Queue Server
A Flask-based server application that interfaces with a Selenium WebDriver to automate downloading tasks from Vimm's Lair. The application maintains a queue of URLs and a record of completed downloads.

Features:
Web Interface: Easily add URLs to a download queue.
Real-time Updates: Monitor the status of ongoing downloads in real-time.
Record Keeping: Keep track of completed downloads with associated filenames.
Real-time Communication: Utilizes Flask-SocketIO for real-time communication between the server and clients.
Automation: Uses Selenium WebDriver for browser automation.
Installation:
Prerequisites:
Apache web service
MySQL database
Python 3.x
Chrome WebDriver

Steps:

1. Create the Database & Tables:

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


2. Clone the Repository:
    git clone https://github.com/DasJager/VimmsDownloader.git
    cd VimmsDownloader

3. Set up a Virtual Environment:


4.Install Required Packages:
    pip install -r requirements.txt


5.Set up the Database: Make sure you have MySQL installed and running. Then create the necessary tables using the provided SQL script provided in step 1.

6.Run the Server:
python app.py  # Or however you named your app server script


