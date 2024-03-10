from app import app
from flask import render_template, request
import chromadb
from chromadb.utils import embedding_functions
from modules.scraper import Scrapper
from modules.sample_texts import tekst1, teks2

chroma_client = chromadb.PersistentClient(path="vectordb")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "cosine"}
)


@app.route('/')
def index():
    return render_template('simple.html')


@app.route('/submit_link', methods=['POST'])
def submit_link():
    if request.method == 'POST':
        link: str = request.form['link']

        scraped_text: str = Scrapper.scrape_text_from_link2(link)

        collection.add(
            documents=[scraped_text],
            metadatas=[{'source': link}],
            ids=[str(collection.count())]
        )

        return render_template('simple.html')


@app.route('/submit_query', methods=['POST'])
def submit_query():
    if request.method == 'POST':
        user_query = request.form['query']

        result = collection.query(
            query_texts=[user_query],
            n_results=3,
            include=['documents', 'distances', 'metadatas']
        )

        return render_template('simple.html', argument=result)


@app.route('/add_test_data', methods=['POST'])
def add_test_data():
    collection.add(
        documents=[tekst1, teks2],
        metadatas=[{'source': 'tekst1'}, {'source': 'tekst2'}],
        ids=['id_0', 'id_1']
    )

    return render_template('simple.html')
