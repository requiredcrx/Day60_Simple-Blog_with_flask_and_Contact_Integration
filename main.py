from flask import Flask, render_template, request
from smtplib import SMTP
import requests
from dotenv import load_dotenv
import os

load_dotenv()

posts = requests.get("https://api.npoint.io/d0935fc8e15e3ff2c2ad").json()
email = os.getenv('EMAIL')
email_pass = os.getenv('PASSWORD')

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        user_email = data['email']
        phone = data['phone']
        message = data['message']
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=email_pass)
            connection.sendmail(from_addr=email, to_addrs=email, msg=f"Subject:New Message "
                                                                     f"\n\nName: {name} "
                                                                     f"\nEmail: {user_email} \nPhone: {phone} "
                                                                     f"\nMessage: {message}")
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
