import requests
from bs4 import BeautifulSoup
import re
import tempfile
from urllib.parse import urlparse
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import whisper


class Scrapper:

    @staticmethod
    def scrape_text_from_link(link):
        parsed_url = urlparse(link)
        # print(parsed_url.netloc)
        if parsed_url.netloc == 'przetargowa.pl' and parsed_url.path.startswith('/'):
            lista = Scrapper.scrape_text_from_przetargowa_article(link)
            lista.append("article_link")
            return lista
        elif parsed_url.netloc == 'www.youtube.com' and parsed_url.path.startswith('/watch'):
            lista = Scrapper.scrape_text_from_youtube_video(link)
            lista.append("youtube_link")
            return lista
        else:
            # Default scrapper function - for now
            if link:
                return Scrapper.scrape_text_from_article(link), "article_link"

    @staticmethod
    def scrape_text_from_file(file_path):
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == '.mp3':
            return Scrapper.scrape_text_from_mp3_file(file_path)
        elif file_extension.lower() == '.mp4':
            return Scrapper.scrape_text_from_mp4_file(file_path)
        else:
            return f"Nieobsługiwane rozszerzenie pliku: {file_extension}"

    @staticmethod
    def scrape_text_from_article(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                for script in soup(["script", "style"]):
                    script.extract()

                text: str = soup.get_text(separator='\n')
                text: str = re.sub(r'\n+', '\n', text)
                text: str = re.sub(r'\n{2,}', '\n\n', text)
                text: str = text.strip()

                return text
            else:
                return "Nie udało się pobrać strony. Spróbuj ponownie później."
        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def scrape_text_from_przetargowa_article(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('h1', class_='tdb-title-text').text
                elements = soup.find_all(re.compile(r'^h[1-2]$|^p$|^ul$|^ol$'))
                text_list = []

                for el in elements:
                    if el.parent == el.find_parent('div', class_=['tdb-block-inner', 'td-fix-index']):
                        if el.parent.get('class')[0] == 'tdb-block-inner':
                            text_list.append(el.get_text().strip())

                text = ' '.join(text_list)

                return [text, title]

            else:
                return "Nie udało się pobrać strony. Spróbuj ponownie później."
        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def scrape_text_from_youtube_video(link):
        try:
            yt = YouTube(link)
            audio = yt.streams.filter(only_audio=True).first()

            with tempfile.TemporaryDirectory() as temp_dir:
                audio.download(output_path=temp_dir, filename="audio.mp3")
                file_path = os.path.join(temp_dir, 'audio.mp3')

                result = Scrapper.audio_to_text_function(file_path)
                title = yt.title

                return [result, title]

        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def scrape_text_from_mp3_file(file_path):
        try:
            result = Scrapper.audio_to_text_function(file_path)

            return result

        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def scrape_text_from_mp4_file(file_path):
        try:
            mp3_file_path = os.path.splitext(file_path)[0] + '.mp3'

            with VideoFileClip(file_path) as clip:
                audio = clip.audio
                audio.write_audiofile(mp3_file_path, verbose=False)

            result = Scrapper.audio_to_text_function(mp3_file_path)

            return result

        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def audio_to_text_function(file_path):
        try:
            model = whisper.load_model("small")
            result = model.transcribe(file_path, fp16=False, language="pl")

            return result["text"]

        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"
