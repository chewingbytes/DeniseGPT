import threading
import subprocess
import os

def run_script(script_name):
    venv_path = r"C:\Users\ASUS\Desktop\Development\denise\venv\Scripts"
    script_path = os.path.join("C:\\Users\\ASUS\\Desktop\\Development\\denise", script_name)

    subprocess.run([os.path.join(venv_path, "python"), script_path])

if __name__ == "__main__":
    try:
        script1_thread = threading.Thread(target=run_script, args=("main.py",))
        script2_thread = threading.Thread(target=run_script, args=("telegram_bot\\telegram.py",))

        script1_thread.start()
        script2_thread.start()

        script1_thread.join()
        script2_thread.join()

        print("Both scripts have finished executing.")

    except KeyboardInterrupt:
        print('Big Daddy Script Exiting')
