from flask import Flask, render_template, request, jsonify
from model import db, Enquiry, Application
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load variables from your local .env file
load_dotenv()

app = Flask(__name__)

# Fall back to your local SQLite file if DATABASE_URL isn't present in your env 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///trilateral.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ── email config ──
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From']    = os.getenv('EMAIL_ADDRESS')
    msg['To']      = os.getenv('EMAIL_ADDRESS')
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
            smtp.send_message(msg)
    except Exception as e:
        print("Email error:", e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    data = request.get_json()
    entry = Enquiry(
        name    = data.get('name'),
        company = data.get('company'),
        contact = data.get('contact'),
        type    = data.get('type'),
        message = data.get('message')
    )
    db.session.add(entry)
    db.session.commit()
    send_email(
        subject = f"New Enquiry from {data.get('name')}",
        body    = f"Name: {data.get('name')}\n"
                  f"Company: {data.get('company')}\n"
                  f"Contact: {data.get('contact')}\n"
                  f"Project Type: {data.get('type')}\n"
                  f"Message: {data.get('message')}"
    )
    return jsonify({"status": "ok"})

@app.route('/submit-application', methods=['POST'])
def submit_application():
    data = request.get_json()
    entry = Application(
        name       = data.get('name'),
        email      = data.get('email'),
        phone      = data.get('phone'),
        position   = data.get('position'),
        experience = data.get('experience'),
        cover      = data.get('cover'),
        link       = data.get('link')
    )
    db.session.add(entry)
    db.session.commit()
    send_email(
        subject = f"New Application — {data.get('position')} from {data.get('name')}",
        body    = f"Name: {data.get('name')}\n"
                  f"Email: {data.get('email')}\n"
                  f"Phone: {data.get('phone')}\n"
                  f"Position: {data.get('position')}\n"
                  f"Experience: {data.get('experience')}\n"
                  f"Cover Note: {data.get('cover')}\n"
                  f"Link: {data.get('link')}"
    )
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
    