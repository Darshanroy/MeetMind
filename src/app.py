from flask import Flask, request, redirect, url_for, render_template
import os

from utils_code.DataLoader import get_word_count_and_docs_from_youtube_url



app = Flask(__name__)

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




# Function to check allowed file extensions
def allowed_file(filename):
    """
    Check which extensions are allowed
    args: Filename which is uploaded
    return:
        Boolean value
    """
    allowed_extensions = {'mp4', 'mp3', 'pdf'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions




@app.route('/')
def index():
    """Loads the index Page"""

    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def upload_file_or_url():

    """this function takecare of uploaded files"""

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'fileUpload' in request.files:
            file = request.files['fileUpload']
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(f"File uploaded: {filename}")
        
        # Check if a URL was provided
        url_input = request.form.get('urlInput')
        if url_input:
            print(f"URL provided: {url_input}")
        
        return 'Form submitted successfully!'

    return render_template('home.html')

@app.route("/result", methods=['GET', 'POST'])
def display_content():
    

    word_count, docs = get_word_count_and_docs_from_youtube_url()

    content = word_count

    return render_template('result.html',content=content)



if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
