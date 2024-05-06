import os
import tempfile
from datetime import datetime, timedelta
import random
from app import app, mail, db
from flask import render_template, request, redirect
import chromadb
from chromadb.utils import embedding_functions
from modules.models import Auth, User
from modules.scraper import Scrapper
from modules.sample_texts import tekst1, teks2
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

# Settings
chroma_client = chromadb.PersistentClient(path="vectordb")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "cosine"}
)

# Index
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET' and 'query' in request.args:
        app.logger.info('hello')
        result = collection.query(
            query_texts=[request.args.get('query')],
            n_results=5,
            include=['documents', 'distances', 'metadatas']
        )
        return render_template('index.html', result=result)
    app.logger.info(request.args.to_dict())
    return render_template('index.html')

# Sign in
@app.route('/sign-in', methods=['GET'])
def get_sign_in():
    app.logger.info(list(map(lambda auth: auth.password, Auth.query.all())))
    return render_template('sign-in.html')
    
@app.route('/sign-in', methods=['POST'])
def post_sign_in():
    email: str = request.form.get('email', '')
    if email == 'admin@admin.admin':
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User()
            user.email = email
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect('/panel')
    else:
        code: str = request.form.get('code', None)
        if code is None:
            user = User.query.filter_by(email=email).first()
            if user is not None:
                generated_code = str(random.randint(0, 999999)).zfill(6)
                expiration_time = datetime.now() + timedelta(hours=1)
                auth = Auth()
                auth.password = generated_code
                auth.expiration_time = expiration_time
                auth.user_id = user.id
                db.session.add(auth)
                db.session.commit()
                
                msg = Message(subject='Kod logowania', sender=app.config['MAIL_USERNAME'], recipients=[email])
                msg.body = f"Kod logowania to: {generated_code}. Kod jest ważny tylko przez godzinę."
                mail.send(msg)
            return render_template('sign-in.html', email=email)
        else:
            user = User.query.filter_by(email=email).first()
            if user is not None:
                for auth in Auth.query.filter(Auth.user_id == user.id, Auth.expiration_time >= datetime.now()).all():
                    if auth.password == code:
                        login_user(user)
                        return redirect('/panel')
                return render_template('sign-in.html', failure=True)
            else:
                return render_template('sign-in.html', failure=True)

# sign out
@app.route('/sign-out')
@login_required
def logout():
    logout_user()
    return redirect('/')

# panel
def get_all_urls():
    data = collection.get(include=['metadatas'])['metadatas']

    return map(
        lambda meta: meta['source'],
        data
    )

def get_all_tags():
    data = collection.get(include=['metadatas'])['metadatas']

    return map(
        lambda meta: meta['tags'],
        data
    )

def get_all_emails():
    return map(
        lambda user: user.email,
        User.query.filter(User.email != 'admin@admin.admin').all()
    )

@app.route('/panel', methods=['GET'])
@login_required
def panel():
    return render_template('panel.html', urls=get_all_urls(), tags=get_all_tags(), emails=get_all_emails())

# Add link
@app.route('/submit_link', methods=['POST'])
@login_required
def submit_link():
    if request.method == 'POST':
        link: str = request.form['link']
        date: str = request.form['date']
        tags = request.form['tags']

        args = Scrapper.scrape_text_from_link(link)

        collection.add(
            documents=[tags + " " + args[0]],
            metadatas=[{'source': link, 'title': args[1], 'date': date, 'file_type': args[2], 'tags': tags}],
            ids=[str(collection.count())]
        )

        return redirect('/panel')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        date = request.form['date']
        tags = request.form['tags']

        name, extension = os.path.splitext(file.filename)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)
            scraped_text = Scrapper.scrape_text_from_file(file_path)

            if scraped_text:
                collection.add(
                    documents=[tags + " " + scraped_text],
                    metadatas=[{'source': file.filename, 'title': name, 'date': date, 'file_type': extension, 'tags': tags}],
                    ids=[str(collection.count())]
                )

        return redirect('/panel')

@app.route('/add_test_data', methods=['POST'])
@login_required
def add_test_data():
    collection.add(
        documents=[tekst1, teks2],
        metadatas=[{'source': 'tekst1'}, {'source': 'tekst2'}],
        ids=['id_0', 'id_1']
    )

    return redirect('/panel')

# Register
@app.route('/register', methods=['POST'])
def register():
    email: str = request.form.get('email', '')
    if len(email) < 0:
        return redirect('/panel')
    else:
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User()
            user.email = email
            db.session.add(user)
            db.session.commit()
        return redirect('/panel')


@app.context_processor
def utility_processor():
    def current_date():
        return datetime.now().strftime('%Y-%m-%d')

    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d')

    def get_timedelta(days):
        return timedelta(days=days)

    return dict(current_date=current_date, parse_date=parse_date, timedelta=get_timedelta)
