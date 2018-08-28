from flask import Flask, render_template, jsonify, redirect, session
from authlib.flask.client import OAuth
from flask_pymongo import PyMongo
from functools import wraps
import os

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ['MONGODB_URI']
app.config['SECRET_KEY'] = os.environ['AUTH_SECRET']
mongo = PyMongo(app)
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=os.environ['AUTH_CLIENT'],
    client_secret=os.environ['AUTH_SECRET'],
    api_base_url='https://gigdb.auth0.com',
    access_token_url='https://gigdb.auth0.com/oauth/token',
    authorize_url='https://gigdb.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://gigdb.herokuapp.com/callback', audience='https://gigdb.auth0.com/userinfo')

@app.route('/dashboard')
def dashboard():
    return render_template("index2.html")

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
