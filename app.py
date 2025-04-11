from flask import Flask, render_template, Response, jsonify, request
import subprocess
import cv2
from detect import detect_objects
from database import get_item_location
import pyttsx3
from datetime import datetime

app = Flask(__name__)

# Global state
camera = None
detection_running = False

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    global camera, detection_running
    camera = cv2.VideoCapture(0)

    while detection_running:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = detect_objects(frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start-detection', methods=['GET'])
def start_detection():
    global detection_running
    detection_running = True
    return jsonify({"message": "Detection started"})

@app.route('/stop-detection', methods=['GET'])
def stop_detection():
    global detection_running
    detection_running = False
    return jsonify({"message": "Detection stopped"})

@app.route('/view-items', methods=['GET'])
def view_items():
    result = subprocess.run(['python', 'view_items.py'], stdout=subprocess.PIPE)
    return jsonify({"items": result.stdout.decode().splitlines()})

@app.route('/clear-items', methods=['GET'])
def clear_items():
    subprocess.run(['python', 'clear_items.py'])
    return jsonify({"message": "Items cleared"})

# Utility: Speak out loud
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Utility: Extract item name from query
def extract_item_name(query, known_items):
    for item in known_items:
        if item in query.lower():
            return item
    return None

# Utility: Format timestamp for natural speech
def format_timestamp_for_speech(ts):
    try:
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        time_str = dt.strftime('%I:%M %p').lstrip('0')  # e.g., 2:32 PM
        date_str = dt.strftime('%B %d, %Y')             # e.g., April 11, 2025
        return f"{time_str} on {date_str}"
    except Exception as e:
        print("Timestamp formatting error:", e)
        return ts  # fallback

# POST route to process voice query
@app.route('/voice-query', methods=['POST'])
def voice_query():
    data = request.get_json()
    query = data.get('query', '').lower()
    if not query:
        return jsonify({"error": "No voice query provided"}), 400

    tracked_items = ["tv", "wallet", "bottle", "phone", "bag", "keys", "cell phone", "tie", "person"]
    item = extract_item_name(query, tracked_items)

    if item:
        result = get_item_location(item)
        if result:
            location, timestamp = result
            spoken_time = format_timestamp_for_speech(timestamp)
            response = f"Your {item} was last seen at {location} at {spoken_time}."

            return jsonify({"message": response})
        else:
            response = f"No records found for {item}."
            
            return jsonify({"message": response})
    else:
        response = "I couldn't recognize any known item in your query."

        
        return jsonify({"message": response})

if __name__ == '__main__':
    app.run(debug=True)
