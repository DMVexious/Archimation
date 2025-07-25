import os
import uuid
from flask import Flask, render_template, request, url_for, jsonify
from Master_test import generate_video_from_topic
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html') 

@app.route('/index.html')
def home():
    return render_template('index.html') 

@app.route('/input.html')
def input_page():
    return render_template('input.html')
    

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get('text_prompt')
    if not topic:
        return jsonify({"error": "text_prompt is missing"}), 400

    # 1. Create a unique filename to prevent user collisions
    unique_id = uuid.uuid4()
    safe_topic_name = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"{unique_id}-{safe_topic_name}.mp4"
    
    # 2. Define where the video will be saved in the static folder
    # Note: Flask serves files from the '/static' directory
    output_dir = os.path.join('static', 'videos')
    os.makedirs(output_dir, exist_ok=True) # Ensure the directory exists
    output_path = os.path.join(output_dir, filename)

    # 3. Define the public URL the browser will use to access the video
    video_url = url_for('static', filename=f'videos/{filename}')

    # 4. Start the Manim render in a background thread
    print(f"FLASK: Starting background thread for video: {filename}")
    thread = threading.Thread(target=generate_video_from_topic, args=(topic, output_path))
    thread.start()

    # 5. Respond IMMEDIATELY with the URL where the video will be
    return jsonify({"video_url": video_url})
    
@app.route('/result/<filename>')
def show_result(filename):
    video_url = url_for('static', filename=os.path.join('videos', filename))
    return render_template('result.html', video_url=video_url)

@app.route('/library.html')
def library():
    return render_template('library.html')

@app.route('/result.html')
def result():
    return render_template('result.html')
  
if __name__=='__main__':
    os.makedirs(os.path.join('static', 'videos'), exist_ok=True)
    app.run(debug=True, port=5001)