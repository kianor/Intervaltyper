from flask import Flask, render_template, request
import pyautogui
import threading
import time

app = Flask(__name__)

# Global variables
is_running = False

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Function to start sending messages periodically
def start_sending(interval, message_content):
    global is_running
    while is_running:
        pyautogui.typewrite(message_content)
        pyautogui.press('enter')
        time.sleep(interval)

# Start route
@app.route('/start', methods=['POST'])
def start():
    global is_running
    if is_running:
        return 'Error: The script is already running!'
    else:
        interval = int(request.form['interval'])
        if interval <= 0:
            return 'Error: Invalid timer interval! Please enter a positive integer.'
        message_content = request.form['message']
        is_running = True
        threading.Thread(target=start_sending, args=(interval, message_content)).start()
        return 'Success: The script has started.'

# Stop route
@app.route('/stop', methods=['POST'])
def stop():
    global is_running
    is_running = False
    return 'Success: The script has stopped.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)