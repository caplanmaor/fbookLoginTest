from flask import Flask, request, redirect, session
from flask.templating import render_template
import json
import os
import requests
from requests.sessions import session


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login/", methods=["POST"])
def login():
    # invoking login dialog setting redirect URL
    get_code_url = f"https://www.facebook.com/dialog/oauth?client_id={os.environ.get('CLIENT_ID')}&redirect_uri={os.environ.get('REDIRECT_URI')}&scope=email"
    return redirect(get_code_url)


@app.route("/login-redirect/", methods=["GET"])
def login_redirect():
    # do get ?code= and exchange code for acces_token, store token in session
    code = request.args.get("code")
    get_token_url = f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={os.environ.get('CLIENT_ID')}&redirect_uri={os.environ.get('REDIRECT_URI')}&client_secret={os.environ.get('CLIENT_SECRET')}&code={code}"
    access_token_json = requests.get(get_token_url)
    access_token_dict = json.loads(access_token_json.text)
    access_token = access_token_dict["access_token"]

    user_json = requests.get(
        f"https://graph.facebook.com/me?access_token={access_token}"
    )
    user_dict = json.loads(user_json.text)
    user_id = user_dict["id"]

    pic_json = requests.get(
        f"https://graph.facebook.com/{user_id}?fields=picture.width(720).height(720)&redirect=false&access_token={access_token}"
    )
    pic_dict = json.loads(pic_json.text)
    pic_url = pic_dict["picture"]["data"]["url"]
    return redirect(pic_url)


if __name__ == "__main__":
    app.run()
