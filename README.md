Features
Simple Web Interface: An intuitive and clean UI for users to input any topic.
Dynamic Video Generation: Utilizes the powerful Manim engine to create animations programmatically.
Asynchronous Workflow: Employs background processing to handle long video render times without crashing the web server or timing out the user's browser.
Real-time Feedback: A loading screen informs the user that their video is being crafted.
Instant Playback: The final video is embedded directly on the page for immediate viewing and download.

How It Works (Architecture)
This project is built on a client-server model designed to handle long-running tasks initiated from a web request.
Frontend (HTML/JS): A user enters a topic (e.g., "Quantum Physics") into a form. JavaScript's fetch API sends this topic to the Flask backend.
Backend (Flask): The /generate API route receives the request. To avoid the 30-60 second browser timeout, it does not render the video directly. Instead, it:
a. Creates a unique filename for the video that will be generated.
b. Starts a new background thread (threading) to run the time-consuming create_manim_video function.
c. Immediately sends a response back to the frontend, containing the public URL where the video will eventually be located.
Polling (Frontend): After receiving the future video URL, the JavaScript begins to "poll" it—checking every few seconds to see if the file exists yet. It expects to receive 404 Not Found errors initially.
Video Generation (Manim): In the background, the thread executes the Manim render command. This process can take several minutes. Once complete, the final .mp4 video file is saved to the /static/videos/ directory, making it accessible at the URL the frontend is polling.
Display Video: As soon as the polling check receives a 200 OK status (meaning the file now exists), it stops. The JavaScript then hides the loading animation, creates an HTML <video> player, and displays the finished animation to the user.

Technology Stack
Backend: Python 3, Flask
Frontend: HTML5, CSS3, JavaScript (ES6+)
Animation Engine: Manim
Core Python Library: threading (for background task execution)

Setup and Installation
Follow these steps to get the project running on your local machine.
1. Prerequisites:
You must have Python 3.8+ and Pip installed. Most importantly, you need a working installation of Manim and its dependencies (FFmpeg, LaTeX).
Note: Manim installation is complex. Please follow the official Manim Installation Guide for your operating system before proceeding.
2. Clone the Repository:
Generated bash
git clone https://github.com/your-username/archimation.git
cd archimation
3. Install Python Dependencies:
Create a requirements.txt file with the following content:
Generated code
# requirements.txt
Flask
manim
manim-voiceover
tts
threading

Then, install it using pip:
pip install -r requirements.txt


4. Project Structure:
Ensure your project directory is organized as follows. You will need to create your Manim scene file (e.g., scene.py).
Generated code
/archimation
|-- app.py              # The main Flask application logic
|-- scene.py            # Your Manim scene definitions
|-- requirements.txt    # Python dependencies
|-- static/
|   |-- css/
|   |   |-- style.css
|   |-- videos/         # Generated videos are saved here (create this folder)
|-- templates/
|   |-- index.html      # The main HTML page with the form
|-- README.md           # This file

5. Run the Application:
python app.py

Generated code
6. Access in Browser:
Open your web browser and navigate to `http://127.0.0.1:5000`.
📖 How to Use
1.  Launch the application using `python app.py`.
2.  Open your browser to `http://127.0.0.1:5000`.
3.  Enter the subject you want to learn about in the input field.
4.  Click the generate button (the arrow).
5.  Wait while the loading animation is displayed. This can take several minutes depending on your video's complexity and your computer's speed.
6.  Once complete, the video player will appear. You can play the animation directly or use the download button.
