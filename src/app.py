from flask import Flask, request, redirect, url_for, render_template, session


from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_groq import ChatGroq

import os
import uuid
from langchain.schema import Document



from utils_code.DataLoader import get_word_count_and_docs_from_youtube_url
from utils_code.DataCleaning import clean_text
from utils_code.chunking_and_embedding import chunking_and_loading_vectorDB
from utils_code.prompts import PromptFraming
from dotenv import load_dotenv

load_dotenv()







app = Flask(__name__)
app.secret_key = 'SEC123'  # Set a secret key for session

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


EmbedModel = HuggingFaceEndpointEmbeddings(model="intfloat/multilingual-e5-large", huggingfacehub_api_token=os.getenv("HUGGINGFACE_HUB_API"))

llm=ChatGroq(groq_api_key=os.getenv("GROQ_API"),
             model_name="Llama3-8b-8192")

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

    session['session_id'] = str(uuid.uuid4())

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


@app.route("/result", methods=['GET','POST'])
def display_content():

    """This function displays the content based on the provided URL."""
    
    url_input = request.form.get('urlInput')  # Get the URL from the session
    if url_input:
        word_count, docs = get_word_count_and_docs_from_youtube_url(url_input)  # Pass the URL to your function
        
        #cleaning the text
        content = clean_text(docs[0].page_content)

        try:
            #loading the text to folder using name of session['session_id'] 
            with open(file=fr"texts\{session['session_id']}.txt", encoding="utf-8", mode="w") as obj:
                obj.write(content)

        except FileNotFoundError :
            os.makedirs(name="texts/")
            #loading the text to folder using name of session['session_id'] 
            with open(file=fr"texts\{session['session_id']}.txt", encoding="utf-8", mode="w") as obj:
                obj.write(content)
     
        # content = Document(page_content=content)
        # print(content)

        vector_db = chunking_and_loading_vectorDB(content, EmbedModel,session['session_id'])

        obj = PromptFraming(llm,vector_db)

        chain = obj.create_conversational_rag_chain()


        user_question = "Highlight the important points in the podcast!"
        session_id = "u1"
        # user_questio = input("Enter: ")
        response = chain.invoke(
            {"input": user_question},
            config={"configurable": {"session_id": session_id}},
        )


        return render_template('result.html', content=response['answer'])
    
    return 'No URL provided!'  # Handle the case where no URL was stored
    

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)



# # saving the loaded docs to the txt files
