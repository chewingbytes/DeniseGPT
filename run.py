import threading
import subprocess
import os

def run_script(script_path):
    # Get the current file's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the virtual environment
    venv_path = os.path.join(base_dir, 'venv', 'Scripts')

    # Run the script using the virtual environment's Python
    subprocess.run([os.path.join(venv_path, "python"), script_path])

if __name__ == "__main__":
    try:
        # Construct paths for both scripts
        script1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        script2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telegram_bot", "telegram.py")

        # Create threads for running the scripts
        script1_thread = threading.Thread(target=run_script, args=(script1_path,))
        script2_thread = threading.Thread(target=run_script, args=(script2_path,))

        # Start the threads
        script1_thread.start()
        script2_thread.start()

        # Wait for both threads to finish
        script1_thread.join()
        script2_thread.join()

        print("Both scripts have finished executing.")

    except KeyboardInterrupt:
        print('Big Script Exiting')
