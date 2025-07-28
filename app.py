import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session, send_from_directory
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_migrate import Migrate
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Set the database path dynamically so that it's stored in your new project directory.
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_dir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Mail configuration (hosted mail)
app.config['MAIL_SERVER'] = 'mail.bluewaveoil.com.ng'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "bluewaveoil.com@bluewaveoil.com.ng"
app.config['MAIL_PASSWORD'] = "Knowledge2020."
app.config['MAIL_DEFAULT_SENDER'] = ('BlueWave Petroleum', 'bluewaveoil.com@bluewaveoil.com.ng')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Initialize Flask-SocketIO for real-time chat functionality
socketio = SocketIO(app)

# ----------------------------
# Models
# ----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # In production, store hashed passwords!
    verified = db.Column(db.Boolean, default=False)

# New model to store newsletter subscribers
class NewsletterSubscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ----------------------------
# Main Website Routes
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/who-we-are')
def who_we_are():
    return render_template('who-we-are.html')

@app.route('/energy-needs')
def energy_needs():
    return render_template('energy-needs.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/americas-region')
def americas_region():
    return render_template('americas-region.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/middle-east-africa')
def middle_east_africa_region():
    return render_template('middle-east-africa.html')

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/global-organization')
def global_organization():
    return render_template('our-global-organization.html')

@app.route('/our-approach')
def our_approach():
    return render_template('our-approach.html')

@app.route('/technology-and-collaborations')
def technology_and_collaborations():
    return render_template('technology-and-collaborations.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/exploration-and-production')
def exploration_and_production():
    return render_template('exploration-production.html')

@app.route('/refining-and-distribution')
def refining_and_distribution():
    return render_template('refining-distribution.html')

@app.route('/innovative-solutions')
def innovative_solutions():
    return render_template('innovative-solutions.html')

@app.route('/operational-excellence')
def operational_excellence():
    return render_template('operational-excellence.html')

@app.route('/environmental-impact')
def environmental_impact():
    return render_template('environmental-impact.html')

@app.route('/resource-efficiency')
def resource_efficiency():
    return render_template('resource-efficiency.html')

@app.route('/green-innovations')
def green_innovations():
    return render_template('green-innovations.html')

@app.route('/community-engagement')
def community_engagement():
    return render_template('community-engagement.html')

@app.route('/local-partnerships')
def local_partnerships():
    return render_template('local-partnerships.html')

@app.route('/social-programs')
def social_programs():
    return render_template('social-programs.html')

@app.route('/employee-engagement')
def employee_engagement():
    return render_template('employee-engagement.html')

@app.route('/volunteer-initiatives')
def volunteer_initiatives():
    return render_template('volunteer-initiatives.html')

@app.route('/press-releases')
def press_releases():
    return render_template('press-releases.html')

@app.route('/media-coverage')
def media_coverage():
    return render_template('media-coverage.html')

@app.route('/industry-insights')
def industry_insights():
    return render_template('industry-insights.html')

@app.route('/expert-commentary')
def expert_commentary():
    return render_template('expert-commentary.html')

@app.route('/financial-reports')
def financial_reports():
    return render_template('financial-reports.html')

@app.route('/market-trends')
def market_trends():
    return render_template('market-trends.html')

@app.route('/strategic-vision')
def strategic_vision():
    return render_template('strategic-vision.html')

@app.route('/shareholder-updates')
def shareholder_updates():
    return render_template('shareholder-updates.html')

@app.route('/job-openings')
def job_openings():
    return render_template('job-openings.html')

@app.route('/internships')
def internships():
    return render_template('internships.html')

@app.route('/employee-benefits')
def employee_benefits():
    return render_template('employee-benefits.html')

@app.route('/diversity-inclusion')
def diversity_inclusion():
    return render_template('diversity-inclusion.html')

@app.route("/what-we-do")
def what_we_do():
    return render_template("what-we-do.html")

@app.route("/sustainability")
def sustainability():
    return render_template("sustainability.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route('/newsroom')
def newsroom():
    return render_template('newsroom.html')

@app.route('/investor')
def investors():
    return render_template('investor.html')

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route("/privacy-center")
def privacy_center():
    return render_template("privacy-center.html")

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(
        app.static_folder, 'manifest.json',
        mimetype='application/json'
    )

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(
        app.static_folder,
        'service-worker.js',
        mimetype='text/javascript'
    )




# ----------------------------
# Newsletter Subscription Endpoint
# ----------------------------

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400
    # Check if already subscribed
    if NewsletterSubscriber.query.filter_by(email=email).first():
        return jsonify({"status": "success", "message": "You are already subscribed."})
    subscriber = NewsletterSubscriber(email=email)
    db.session.add(subscriber)
    db.session.commit()
    # Debug: Print current subscribers to console
    all_subscribers = NewsletterSubscriber.query.all()
    print("Current subscribers:", [sub.email for sub in all_subscribers])
    
    # Send confirmation email to the subscriber
    subject = "Subscription Confirmation - BlueWave Petroleum"
    confirmation_body = (
        "Thank you for subscribing to BlueWave Petroleum updates! "
        "You will receive an email notification whenever we post a new update in our newsroom. "
        "To view the newsroom at any time, please visit: " + url_for('newsroom', _external=True)
    )
    msg = Message(subject, recipients=[email])
    msg.body = confirmation_body
    try:
        mail.send(msg)
    except Exception as e:
        print("Error sending confirmation email:", str(e))
    return jsonify({"status": "success", "message": "Subscription successful!"})

# ----------------------------
# Helper Function for Notifying Subscribers
# ----------------------------
def notify_subscribers():
    subscribers = NewsletterSubscriber.query.all()
    # Debug: Print subscribers before sending notifications
    print("Notifying subscribers. Current subscriber emails:",
          [sub.email for sub in subscribers])
    if not subscribers:
        print("No subscribers to notify.")
        return False
    subject = "New Update in Our Newsroom - BlueWave Petroleum"
    # Generate the full URL to the newsroom page
    newsroom_url = url_for('newsroom', _external=True)
    body = f"We have a new update in our Newsroom! Click the link below to view the latest news:\n{newsroom_url}"
    for sub in subscribers:
        msg = Message(subject, recipients=[sub.email])
        msg.body = body
        try:
            mail.send(msg)
            print(f"Notification sent to {sub.email}")
        except Exception as e:
            print(f"Error sending email to {sub.email}: {str(e)}")
    return True

# ----------------------------
# Admin Publish Action: Update Newsroom Content and Notify Subscribers
# ----------------------------
@app.route('/admin/update-newsroom', methods=['GET', 'POST'])
def update_newsroom():
    # In a real application, protect this route with admin authentication.
    if request.method == 'POST':
        # Get new newsroom content from the form (adjust field name as needed)
        new_content = request.form.get('content')
        if not new_content:
            flash("No content provided.", "error")
            return redirect(url_for('update_newsroom'))

        # Example: Save the new content to a file.
        # Adjust the path and method if you are storing content in a database.
        newsroom_path = os.path.join(basedir, 'templates', 'newsroom.html')
        try:
            with open(newsroom_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            flash("Newsroom content updated successfully.", "success")
        except Exception as e:
            flash("Failed to update newsroom content: " + str(e), "error")
            return redirect(url_for('update_newsroom'))

        # After updating the content, notify all subscribers automatically.
        if notify_subscribers():
            flash("Subscribers have been notified about the new update.", "success")
        else:
            flash("No subscribers to notify.", "info")
        return redirect(url_for('newsroom'))

    # For GET requests, render an admin update form.
    return render_template('admin_update_newsroom.html')

# ----------------------------
# Newsroom Update Notification Endpoint
# ----------------------------
@app.route('/notify-newsroom-update', methods=['POST'])
def notify_newsroom_update():
    try:
        subscribers = db.session.execute(db.select(NewsletterSubscriber.email)).all()
    except Exception as e:
        app.logger.error(f"Failed to fetch subscribers: {e}")
        return jsonify(status="error", message="Could not fetch subscribers."), 500

    if not subscribers:
        return jsonify(status="error", message="No subscribers to notify."), 400

    subject = "New Update in Our Newsroom - BlueWave Petroleum"
    newsroom_url = url_for('newsroom', _external=True)

    text_body = f"We have a new update in our Newsroom! Click here: {newsroom_url}"

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Newsroom Update</title></head>
<body style="margin:0;padding:0;background:#f2f2f2;font-family:Arial,sans-serif;">
  <div style="max-width:600px;margin:auto;background:#fff;border:1px solid #ddd;">
    <div style="background:#004080;padding:20px;text-align:center;">
      <img src="cid:bluewave_logo" alt="BlueWave Logo" style="max-width:100px;">
    </div>
    <div style="padding:20px;color:#333;line-height:1.5;">
      <h1 style="color:#004080;margin-top:0;">Newsroom Updates</h1>
      <p>Dear Subscriber,</p>
      <p>We’re excited to share new content. <a href="{newsroom_url}" style="color:#004080;text-decoration:none;font-weight:bold;">Click here to read it.</a></p>
      <p>Thank you for staying with us!</p>
      <p>Best regards,<br>The BlueWave Team</p>
    </div>
    <div style="background:#eee;padding:10px;text-align:center;font-size:12px;color:#666;">
      &copy; 2025 BlueWave Petroleum. All rights reserved.
    </div>
  </div>
</body>
</html>"""

    errors = []

    for (email,) in subscribers:  # ✅ CORRECTED UNPACKING
        try:
            msg = Message(subject, recipients=[email])
            msg.body = text_body
            msg.html = html_body

            # Attach the logo inline
            with app.open_resource("static/images/bluewave_logo1.webp") as fp:
                msg.attach(
                    filename="bluewave_logo1.webp",
                    content_type="image/webp",
                    data=fp.read(),
                    disposition="inline",
                    headers=[("Content-ID", "<bluewave_logo>")]  # ✅ correct format
                )

            mail.send(msg)

        except Exception as e:
            app.logger.error(f"Notify failed for {email}: {e}")
            errors.append(f"{email}: {e}")

    if errors:
        return jsonify(
            status="partial_error",
            message="Some notifications failed: " + "; ".join(errors)
        ), 500

    return jsonify(status="success", message="All subscribers notified!")

# ----------------------------
# Contact Form Email Sending Endpoint (hosted SMTP)
SMTP_SERVER = "mail.bluewaveoil.com.ng"
SMTP_PORT = 465
EMAIL_ADDRESS = "bluewaveoil.com@bluewaveoil.com.ng"
EMAIL_PASSWORD = "Knowledge2020."

@app.route('/send-email', methods=['POST'])
def send_email_route():
    try:
        name    = request.form["name"]
        email   = request.form["email"]
        message = request.form["message"]
        subject = f"New Support Message from {name}"
        body    = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        msg = MIMEMultipart()
        msg["From"]    = EMAIL_ADDRESS
        msg["To"]      = EMAIL_ADDRESS
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

        return jsonify({"status": "success", "message": "Your message has been sent successfully!"})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to send message: {e}"
        }), 500


# New Reply Email Sending Endpoint
@app.route('/reply-contact', methods=['POST'])
def reply_contact():
    try:
        # Get form details
        user_email = request.form["user_email"]
        user_name = request.form["user_name"]
        reply_message = request.form["reply_message"]
        
        app.logger.info("Preparing reply email for %s", user_email)
        
        subject = f"Re: Your Support Message, {user_name}"
        
        # Plain text fallback version
        text_content = f"""Dear {user_name},

{reply_message}

Thank you for reaching out to us.

Best regards,
Bluewave Oil&Gas Team"""
        
        # Simplified HTML version with inline CSS and minimal markup
        html_content = f"""
        <html>
          <body style="margin:0; padding:0; background-color:#f2f2f2; font-family:Arial, sans-serif;">
            <div style="max-width:600px; margin:auto; background-color:#ffffff; border:1px solid #dddddd;">
              <!-- Header -->
              <div style="background-color:#004080; padding:20px; text-align:center;">
                <h1 style="color:#ffffff; margin:0; font-size:24px;">Bluewave Oil&amp;Gas</h1>
              </div>
              <!-- Content -->
              <div style="padding:20px; color:#333333; line-height:1.5;">
                <p style="margin-top:0;">Dear {user_name},</p>
                <p style="margin:0;">{reply_message}</p>
                <p style="margin:0;">Thank you for reaching out to us. Please let us know if you have any further questions.</p>
                <p style="margin:0;">Best regards,<br>The Bluewave Oil&amp;Gas Team</p>
              </div>
              <!-- Footer -->
              <div style="background-color:#eeeeee; padding:10px; text-align:center; font-size:12px; color:#666666;">
                &copy; 2025 Bluewave Oil&amp;Gas. All rights reserved.
              </div>
            </div>
          </body>
        </html>
        """
        
        # Create a multipart MIME message with both plain and HTML parts
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = user_email
        msg["Subject"] = subject

        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        app.logger.info("Sending reply email to %s", user_email)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, user_email, msg.as_string())
        
        app.logger.info("Reply email sent successfully to %s", user_email)
        return jsonify({"status": "success", "message": "Reply email sent successfully!"})
    except Exception as e:
        app.logger.error("Error sending reply email: %s", str(e))
        return jsonify({"status": "error", "message": "Failed to send reply email. Try again later."})


# ----------------------------
# Authentication Routes
# ----------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "user_email" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("profile"))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        if User.query.filter_by(email=email).first():
            flash('This email is already registered. Please log in instead.', 'error')
            return redirect(url_for('login'))
        new_user = User(username=username, email=email, password=password, verified=False)
        db.session.add(new_user)
        db.session.commit()
        token = serializer.dumps(email, salt='email-confirm-salt')
        verify_url = url_for('confirm_email', token=token, _external=True)
        subject = "Verify your email for BlueWave Petroleum"
        html_body = render_template('verify_email.html', verify_url=verify_url, username=username)
        msg = Message(subject, recipients=[email], html=html_body)
        try:
            mail.send(msg)
            flash('A verification link has been sent to your email. Please check your inbox.', 'success')
        except Exception as e:
            flash('Error sending verification email: ' + str(e), 'error')
        return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=86400)
    except Exception as e:
        flash('The verification link is invalid or has expired.', 'error')
        return redirect(url_for('signup'))
    user = User.query.filter_by(email=email).first()
    if user:
        user.verified = True
        db.session.commit()
        flash('Your email has been verified! You can now log in.', 'success')
    else:
        flash('User not found.', 'error')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_email" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("profile"))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("No account found with that email. Please sign up first.", "error")
            return render_template("login.html")
        if not user.verified:
            flash("Your account is not verified. Please check your email for the verification link.", "error")
            return render_template("login.html")
        if user.password != password:
            flash("The email or password you entered is incorrect.", "error")
            return render_template("login.html")
        session["user_email"] = email
        flash("Login successful! Welcome back.", "success")
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            subject = "Reset your password for BlueWave Petroleum"
            html_body = render_template('forgot_password_email.html', reset_url=reset_url, username=user.username)
            msg = Message(subject, recipients=[email], html=html_body)
            try:
                mail.send(msg)
                flash('A password reset link has been sent to your email. Please check your inbox.', 'success')
            except Exception as e:
                flash('Error sending password reset email: ' + str(e), 'error')
        else:
            flash('No account found with that email.', 'error')
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = password  # In production, be sure to hash the password!
            db.session.commit()
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('forgot_password'))
    return render_template('reset_password.html')

@app.route('/profile')
def profile():
    if "user_email" in session:
        user = User.query.filter_by(email=session["user_email"]).first()
        if user:
            return render_template("profile.html", user=user)
    flash("Please log in first.", "error")
    return redirect(url_for("login"))

# ----------------------------
# Additional Routes: Support and Chat
# ----------------------------
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# ----------------------------
# Socket.IO Events for Real-Time Chat
# ----------------------------
@socketio.on('message')
def handle_message(msg):
    print("Message received: " + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)



