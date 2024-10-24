from flask import Flask, session
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

@app.route('/')
def index():
    
        # Generate a new session ID
    session['session_id'] = str(uuid.uuid4())
    

    return f"Your unique session ID: {session['session_id']}"

if __name__ == '__main__':
    app.run(debug=True)
