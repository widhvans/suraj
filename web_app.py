# web_app.py
from flask import Flask, render_template
import config

app = Flask(__name__)

@app.route('/')
def index():
    # index.html फाइल को रेंडर (प्रदर्शित) करें
    return render_template('index.html', channel_link=config.STUDY_CHANNEL_LINK)

if __name__ == '__main__':
    # वेब ऐप को VPS के IP और दिए गए पोर्ट पर चलाएं
    print(f"Web server starting on http://{config.VPS_IP}:{config.PORT}")
    app.run(host=config.VPS_IP, port=config.PORT, debug=True)
