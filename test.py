import pyaudio

def test_microphone():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=1024
    )

    print("Recording...")

    try:
        for _ in range(0, int(16000 / 1024 * 5)):  # Record for 5 seconds
            data = stream.read(1024)
            print("Audio data:", data[:10])  # Print the first few bytes of audio data

    except Exception as e:
        print("Error:", e)

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        print("Finished recording")

test_microphone()
