# Master_test.py (Corrected and Refactored)

import subprocess
from pydantic import BaseModel
import json
import os
import shutil
import uuid # Import uuid for unique filenames
import logging
from google import genai

# Set up logging for better debugging in the background process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - WORKER - %(levelname)s - %(message)s')

try:
    # IMPORTANT: In production, use environment variables for API keys.
    # For this example, replace with your actual keys.
    client1 = genai.Client(api_key="YOUR_API_KEY_HERE") # For Scripting
    client2 = genai.Client(api_key="YOUR_API_KEY_HERE") # For Code Generation
    client3 = genai.Client(api_key="YOUR_API_KEY_HERE") # For Prompt Improvement
except Exception as e:
    logging.error(f"Failed to initialize one or more API clients. Check API keys. Error: {e}")
    # We will let the app fail later if a client is used without being initialized.

# --- ALL YOUR PROMPTS AND HELPER FUNCTIONS REMAIN THE SAME ---
# (I've truncated them for brevity, but you should keep the full text)

class FinalOutput(BaseModel):
    file_name: str
    source_code: str

PROMPT_FILENAME = "code_prompt.txt"


INITIAL_CODE_PROMPT = '''
You are a world-class Manim animator and computer graphics programmer. You will generate a single, complete, and runnable Python script for an educational animation. Your primary goal is to produce a script that is visually clean, well-paced, and runs correctly on the first attempt. Adherence to the following rules, which synthesize all critical context from previous failures, is mandatory and non-negotiable.
Assumed System Prerequisites
A fresh, dedicated Python virtual environment is in use.
Manim Community v0.18.0 or newer is installed.
The command pip install "manim-voiceover[coqui]" has been successfully run.
A full LaTeX distribution (like MiKTeX or TeX Live) is installed and its bin directory is in the system's PATH.
The espeak-ng program is installed on the system and is accessible in the system's PATH.
Primary Inputs
Course Topic: {topic}
Animation Script & Voice Over Script: {script_text}

(Optional) Previous Error Log: If the last attempt failed, the error traceback will be appended here. You MUST analyze this error and fix the root cause.
{error_context}
The Five Pillars of Quality: Core Requirements & Constraints
Pillar 1: Script & Scene Architecture
Single Scene Class: The entire animation MUST be contained within a single Scene class inheriting from VoiceoverScene (e.g., class AdvancedCalculusScene(VoiceoverScene):). Forbidden: Do not use multiple Scene classes.
Modular Helper Methods: The construct method MUST remain clean and only contain a sequence of calls to private helper methods (e.g., self._scene_01_intro_title(), self._scene_02_core_concept()). All animation logic for each distinct visual action MUST be encapsulated in its own helper method.
State Management: Mobjects that must persist or be referenced across different helper methods (e.g., an axis setup that is used in multiple scenes) MUST be stored as instance attributes (e.g., self.axes = ...).
Readability: You should add comments explaining the "why" behind your code, especially for complex calculations or non-obvious animation choices.
Pillar 2: Visual Layout, Pacing, and Clarity
Zero Overlap & Generous Buffers: Layouts MUST be clean, spacious, and completely free of overlapping or cluttered elements. You MUST use large buffers to ensure a clean visual presentation.
Edge Buffers: All major elements positioned with .to_edge() MUST use buff=1.5.
Internal Buffers: All arrangements using .arrange() or positioning with .next_to() MUST use a buff of at least 1.0.
Side-by-Side Comparisons: For layouts like "SN1 vs. SN2," the two main VGroups MUST be positioned on opposite sides of the screen using .to_edge(LEFT, buff=2) and .to_edge(RIGHT, buff=2) to ensure they are far apart and clearly distinct.
Legibility: All text must be clearly legible. Use font_size appropriate for the amount of text on screen (e.g., font_size=36 for normal text, font_size=24 for smaller labels).
Pacing & Voiceover Synchronization: All narrated animations MUST be wrapped in a with self.voiceover(...) as tracker: block.
Every self.play() call inside this block MUST derive its runtime from the tracker (e.g., run_time=tracker.duration).
For long narrations, you MUST sub-divide the tracker's duration across multiple play calls to keep the visuals dynamic. Example: self.play(Write(title), run_time=tracker.duration * 0.4) followed by self.play(FadeIn(subtitle), run_time=tracker.duration * 0.6).
Forbidden: Do not use manual time.sleep() calls.
Pillar 3: Critical Error Prevention & API Integrity
<ins>Rule 3.1: Strictly 2D Environment</ins>
The Scene class MUST inherit from VoiceoverScene only. Forbidden: ThreeDScene. This is to prevent camera state leakage bugs.
All visuals MUST be 2D. Forbidden: ThreeDAxes, Sphere, Cylinder, Cube. All "3D" effects (e.g., orbitals) MUST be simulated using 2D primitives like Ellipse, ParametricFunction, Polygon, and the Rotate animation.
<ins>Rule 3.2: Modern Manim API Compliance</ins>
Older API calls are forbidden. You MUST use the modern equivalents to prevent AttributeError and TypeError.
Coloring:
Mobject(color=RED) is Required. .apply_color(RED) is Forbidden.
For MathTex, the t2c argument is Forbidden. Create the object first, then call .set_color_by_tex("substring", COLOR).
Graphing: axes.plot(...) is Required. .get_graph(...) is Forbidden.
Arrangement: To arrange mobjects in a circle, you MUST manually calculate their positions using trigonometry (np.cos, np.sin, TAU). The .arrange_in_a_circle() method is Forbidden.
Animations: The FadeInFrom animation is Forbidden. To achieve this effect, you MUST use a combination of .shift(), .set_opacity(0), and .animate.restore().
Updaters: All functions passed to .add_updater() or used in always_redraw() MUST be defined with two arguments: the mobject and dt (e.g., lambda m, dt: ...), even if dt is not used. This is mandatory to prevent TypeError.
[CRITICAL] Highlighting MarkupText: Accessing sub-mobjects of a MarkupText object is unstable and Forbidden. To highlight parts sequentially, you MUST create multiple versions of the object with the highlights pre-formatted in the string and then use Transform to switch between them.
<ins>Rule 3.3: Flawless LaTeX and Color Usage</ins>
All text containing special symbols (π, δ⁺, CH₃, etc.) or math formatting MUST be created using MathTex.
All MathTex strings MUST be Python "raw strings" (e.g., r"\frac\delta y\delta x").
Use the LaTeX \text{...} command inside MathTex for non-italicized text (e.g., r"\text{Rate} = k[A]^2").
You MUST use Manim's standard uppercase color constants (e.g., RED, BLUE, GREEN). Forbidden: lowercase or non-standard color names like "brown" or "cyan" and "beige".
!IMPORTANT, Also forbidden to use BROWN CYAN and BEIGE ( All undefined colors )
<ins>Rule 3.4: Robust Mobject Handling & Referencing</ins>
[CRITICAL] TeX Mobject Referencing: To prevent IndexError and TypeError, you MUST NOT access sub-mobjects of a MathTex object using numerical indices (e.g., my_tex[0][1]). This is unstable and Forbidden.
Required Pattern (The "Hook" Method): Create the MathTex from a single string. To select parts, embed unique, non-rendering LaTeX substrings as "hooks." Use .get_part_by_tex("hook") to reliably select these parts.
Generated python
# CORRECT (Robust):
mul_referenced = MathTex("(x_A + 2_B)(x_C - 3_D)", font_size=42)
x_part_A = mul_referenced.get_part_by_tex("x_A")
three_part_D = mul_referenced.get_part_by_tex("3_D")
Use code with caution.
Python
Screen Clearing: To clear all mobjects from the screen between scenes, you MUST use a dedicated helper method containing this specific implementation: mobjects_to_fade = VGroup(*[mob for mob in self.mobjects if isinstance(mob, VMobject)]) followed by self.play(FadeOut(mobjects_to_fade)). The command VGroup(*self.mobjects) is Forbidden as it can capture non-VMobjects.
Transformations: Use Transform only for mobjects with identical point structures. For transitions between fundamentally different shapes (e.g., VGroup to FunctionGraph), you MUST use ReplacementTransform to avoid ValueError.
Pillar 4: Configuration & Dependencies
setup() Method Configuration: The setup() method is required and MUST contain the following configurations:
Voiceover Service: It MUST contain the call self.set_speech_service(CoquiService()). The older CoquiTTS() class is obsolete and Forbidden.
Scene Configuration: It MUST explicitly set self.camera.background_color = BLACK.
construct() Method Configuration: The construct() method MUST begin by forcing a 16:9 landscape aspect ratio: config.frame_width = 16.0 and config.frame_height = 9.0.
Self-Contained Components: Do not rely on imports from outside the core manim library. Prioritize building visuals from fundamental primitives (Rectangle, Circle, Line, Arrow, MathTex).
Mandatory Custom Class: If a thought bubble is needed, you MUST include and use the following fully-corrected ThoughtBubble class definition inside the script. This prevents both ImportError and TypeError.
Generated python
class ThoughtBubble(VGroup):
    def __init__(self, content=None, width=4, height=3, **kwargs):
        super().__init__(**kwargs)
        self.bubble = Ellipse(width=width, height=height, color=WHITE)
        self.tail = VGroup(
            Circle(radius=0.1), Circle(radius=0.2), Circle(radius=0.3)
        ).arrange(DOWN, buff=-0.15)
        self.add(self.bubble, self.tail)
        self.tail.next_to(self.bubble, DR, buff=-0.3)
        if content: self.add_content(content)

    def add_content(self, content):
        content.move_to(self.bubble.get_center())
        self.add(content)
Use code with caution.
Pillar 5: Configuration & Execution
Rule 5.1: Voiceover Service Configuration
The setup() method MUST call self.set_speech_service(CoquiService()).
Forbidden: CoquiTTS().
Rule 5.2: Scene Configuration
The setup() method MUST set self.camera.background_color = BLACK, config.frame_width = 16.0, and config.frame_height = 9.0.
Final Instruction: The main scene class in the generated script MUST be named Generated_Course.
'''

scripting_base = '''
You are an expert Instructional Designer and Educational Scriptwriter for in-depth Manim animations. You specialize in transforming a complete course outline into a detailed, feature-length educational video script (approximately 1-2 minutes).
Your task is to take a provided course overview and generate two distinct, synchronized scripts suitable for a comprehensive animated lesson:
A highly detailed Animation Script / Storyboard detailing the visual actions in a Manim-aware way.
An extensive Voiceover Script containing the corresponding narration.
The final output of these two scripts must be perfectly formatted to be used as the primary input for a subsequent AI prompt that will generate the final Manim animation code.
The topic of the script is: {topic}
Strict Formatting for Output: You must generate two distinct sections with the exact headers "Part 1: Animation Script / Storyboard" and "Part 2: Voiceover Script". The numbering must be perfectly synchronized.
(Example format follows...)
'''

# The CORRECTED prompt for improving the master prompt
prompt_improvement_base = '''
You are a meticulous Prompt Engineering expert acting as an editor. Your task is to make a targeted improvement to a "master prompt" used for Manim code generation.

**Your Goal:**
Analyze the provided run history and identify the single root cause of the failures. Then, you will make a minimal, surgical edit to the "Original Master Prompt" to prevent this specific error in the future.

**Your Process:**
1.  Review the "Original Master Prompt" to understand the existing rules.
2.  Analyze the "Run History" to see what went wrong and what eventually worked.
3.  Formulate a new, concise rule or refine an existing one based on the successful fix.
4.  Integrate this single change into the most logical place within the original prompt's text.
5.  Crucially, do not change or remove any other existing rules. Your job is to preserve the existing knowledge and add to it.

**CRITICAL METADATA RULE:** The prompt you are editing is used in a Python `.format()` string. Therefore, you MUST escape any literal curly braces in your output by doubling them. For example, to include `{{example}}` in the prompt, you MUST write `{{example}}`. Failure to do this will crash the entire system.

**INPUTS:**

---
**Original Master Prompt:**
```
{master_prompt}
```
---
**Run History (Failed Attempts):**
```
{run_history}
```
---
**Final Successful Code:**
```python
{successful_code}
```
---

**TASK:**

Return the **ENTIRE, UPDATED TEXT** of the master prompt. Your output must be the complete, edited prompt, including all the original rules plus your single, targeted improvement. Do not add any conversational text or explanations.
'''


def load_or_create_prompt(filename):
    """Loads the master prompt from a file, or creates it if it doesn't exist."""
    if not os.path.exists(filename):
        logging.info(f"'{filename}' not found. Creating from initial template.")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(INITIAL_CODE_PROMPT)
    
    logging.info(f"Loading master prompt from '{filename}'.")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def improve_master_prompt(current_prompt, history, successful_code):
    """Uses an AI to analyze failures and improve the master prompt."""
    logging.info("--- FAILURES DETECTED: ATTEMPTING TO IMPROVE MASTER PROMPT ---")
    # ... (implementation is the same, no changes needed here)
    pass


## ------------------------------------------------------------------ ##
## --- THIS IS THE NEW FUNCTION THAT WAS MISSING --- ##
## ------------------------------------------------------------------ ##
def generate_video_from_topic(topic: str, output_dir: str) -> str:
    """
    Takes a topic, generates a Manim video, moves it to the specified
    output directory, and returns the final filename.
    Raises an exception on failure.
    """
    # --- THIS IS WHERE THE MAIN LOGIC MOVES TO ---
    code_script_base = load_or_create_prompt(PROMPT_FILENAME)

    logging.info(f"Generating animation script for topic: '{topic}'")
    try:
        script_response = client1.models.generate_content(
            model="gemini-2.5-pro", contents=scripting_base.format(topic=topic)
        )
        script_text = script_response.text
        logging.info("Script has been generated.")
    except Exception as e:
        logging.error(f"FATAL ERROR during script generation: {e}")
        raise RuntimeError(f"Script generation failed: {e}")

    run_history = []
    last_failed_code = ""
    max_attempts = 10

    for attempt in range(max_attempts):
        logging.info(f"--- CODE GENERATION ATTEMPT {attempt + 1}/{max_attempts} ---")
        error_context_for_prompt = ""
        if last_failed_code:
            error_context_for_prompt = (
                "CRITICAL: The previously generated code failed...\n"
                f"LAST FAILED CODE:\n```python\n{last_failed_code}\n```\n\n"
                f"ERROR MESSAGE:\n{run_history[-1]['error']}"
            )

        current_prompt = code_script_base.format(
            topic=topic, script_text=script_text, error_context=error_context_for_prompt
        )
        
        # NOTE: Updated Gemini API usage for JSON mode with Pydantic
        parameters = {
            'model': 'gemini-2.5-flash',
            'response_format': {"type": "json_object"},
            'prompt': f"{current_prompt}\n\n Respond with a JSON object that matches this Pydantic schema: {FinalOutput.model_json_schema()}"
        }
        
        logging.info("Generating Manim code...")
        try:
            # Simplified API call for JSON
            code_response = client2.generate_content(parameters['prompt'], generation_config=genai.types.GenerationConfig(response_mime_type="application/json"))
            response_data = json.loads(code_response.text)
            final_output = FinalOutput(**response_data)
            logging.info(f"Code generated! Filename: {final_output.file_name}")
        except Exception as e:
            logging.error(f"FATAL ERROR during code generation: {e}")
            error_log = f"Model failed to generate valid JSON or another API error occurred: {e}"
            last_failed_code = "No code was generated due to an API or JSON parsing error."
            run_history.append({"code": last_failed_code, "error": error_log})
            continue

        current_code = final_output.source_code
        # Ensure filename is safe and ends with .py
        safe_filename = "".join(c for c in final_output.file_name if c.isalnum() or c in ('_', '-')).rstrip()
        if not safe_filename.endswith('.py'):
            safe_filename += '.py'

        with open(safe_filename, "w", encoding="utf-8") as f:
            f.write(current_code)
        
        logging.info(f'Running manim command: manim -ql {safe_filename} Generated_Course')
        result = subprocess.run(["manim", "-ql", safe_filename, "Generated_Course"], capture_output=True, text=True, check=False)

        if result.returncode != 0:
            logging.error("--- MANIM EXECUTION FAILED ---")
            error_log = result.stderr
            last_failed_code = current_code
            run_history.append({"code": current_code, "error": error_log})
            logging.error(error_log)
            os.remove(safe_filename) # Clean up failed script
            continue
        else:
            logging.info("--- MANIM EXECUTION SUCCESSFUL! ---")
            
            if run_history:
                improve_master_prompt(code_script_base, run_history, current_code)

            scene_name = "Generated_Course"
            script_name_no_ext = safe_filename.replace('.py', '')
            video_source_path = os.path.join("media", "videos", script_name_no_ext, "480p15", f"{scene_name}.mp4")
            
            if not os.path.exists(video_source_path):
                raise FileNotFoundError(f"Could not find generated video file at: {video_source_path}")

            video_filename = f"{uuid.uuid4()}.mp4"
            video_dest_path = os.path.join(output_dir, video_filename)
            shutil.move(video_source_path, video_dest_path)
            logging.info(f"Video moved to {video_dest_path}")
            
            # Clean up temporary files
            os.remove(safe_filename)
            shutil.rmtree(os.path.join("media"))

            return video_filename # SUCCESS! Return the final filename.

    # If all attempts fail, raise an error to be caught by the Flask worker
    raise RuntimeError(f"Failed to generate video for topic '{topic}' after {max_attempts} attempts.")


# This block now ONLY runs if you execute `python Master_test.py` directly.
# It's perfect for testing the function without needing to run the whole web app.
if __name__ == "__main__":
    test_topic = input("Enter a topic to test the video generation: ")
    static_video_dir = os.path.join('static', 'videos')
    os.makedirs(static_video_dir, exist_ok=True)
    
    try:
        final_filename = generate_video_from_topic(test_topic, static_video_dir)
        print(f"\n SUCCESS! Video generated: {os.path.join(static_video_dir, final_filename)}")
    except Exception as e:
        print(f"\n FAILURE: An error occurred during generation: {e}")