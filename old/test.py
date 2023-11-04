from flask import Flask, stream_template, request, Response
import openai
from dotenv import load_dotenv
import os

load_dotenv()
# put these values in an .env file parallel to this file
openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get('OPENAI_API_KEY')
def send_messages(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

app = Flask(__name__)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        messages = request.json['messages']
        def event_stream():
            for line in send_messages(messages=messages):
                print(line)
                text = line.choices[0].delta.get('content', '')
                if len(text):
                    yield text

        return Response(event_stream(), mimetype='text/event-stream')
    else:
        return stream_template('./chat.html')

if __name__ == '__main__':
    app.run()
