from flask import Flask, render_template, request, jsonify
from moviepy.editor import AudioFileClip
import speech_recognition as sr
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    video_file = request.files['file']
    audio_path = 'temp_audio.wav'
    video_path = 'temp_video.mp4'
    video_file.save(video_path)

    video = AudioFileClip(video_path)
    video.write_audiofile(audio_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    os.remove(audio_path)
    os.remove(video_path)

    try:
        text = recognizer.recognize_google(audio_data, language='ja-JP')
        return jsonify({'text': text})  # JSON応答を送信
    except sr.UnknownValueError:
        return jsonify({'text': "Google Speech Recognition could not understand audio"}), 422
    except sr.RequestError as e:
        return jsonify({'text': f"Could not request results from Google Speech Recognition service; {e}"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
