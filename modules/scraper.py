import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from pytube import YouTube
import os
import whisper


class Scrapper:

    @staticmethod
    def scrape_text(link):
        parsed_url = urlparse(link)
        # print(parsed_url.netloc)
        if parsed_url.netloc == 'przetargowa.pl' and parsed_url.path.startswith('/'):
            return Scrapper.scrape_text_from_przetargowa_article(link)
        elif parsed_url.netloc == 'www.youtube.com' and parsed_url.path.startswith('/watch'):
            return Scrapper.scrape_text_from_youtube_video(link)
        else:
            # Default scrapper function - for now
            return Scrapper.scrape_text_from_link2(link)

    @staticmethod
    def scrape_text_from_link(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Tutaj możemy znaleźć i zwrócić interesujący nas tekst ze strony
                # W tym przypadku znajdźmy tekst zawarty w tagu <p>
                paragraphs = soup.find_all('p')
                text: str = '\n'.join([p.get_text() for p in paragraphs])
                return text
            else:
                return "Nie udało się pobrać strony. Spróbuj ponownie później."
        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def scrape_text_from_link2(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Remove script and style tags
                for script in soup(["script", "style"]):
                    script.extract()

                # Get text
                text: str = soup.get_text(separator='\n')

                # Clean up text
                text: str = re.sub(r'\n+', '\n', text)  # Remove excessive newlines
                text: str = re.sub(r'\n{2,}', '\n\n', text)  # Collapse multiple newlines to one
                text: str = text.strip()  # Strip leading and trailing whitespaces

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
                elements = soup.find_all(re.compile(r'^h[1-2]$|^p$|^ul$|^ol$'))
                text_list = []

                for el in elements:
                    if el.parent == el.find_parent('div', class_=['tdb-block-inner', 'td-fix-index']):
                        if el.parent.get('class')[0] == 'tdb-block-inner':
                            text_list.append(el.get_text().strip())

                text = ' '.join(text_list)

                return text

            else:
                return "Nie udało się pobrać strony. Spróbuj ponownie później."
        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"

    @staticmethod
    def scrape_text_from_youtube_video(link):
        try:
            yt = YouTube(link)
            audio = yt.streams.filter(only_audio=True).first()
            directory = "./files/youtube"
            audio.download(output_path=directory, filename="audio.mp3")
            mp3_file_path = "files/youtube/audio.mp3"

            if os.path.exists(mp3_file_path):
                model = whisper.load_model("medium")
                result = model.transcribe(mp3_file_path, fp16=False, language="pl")
                os.remove(mp3_file_path)

                with open(f"files/youtube/{yt.title}.txt", 'w') as f:
                    f.write(result["text"])

                return result["text"]
            else:
                return "Nie udało się pobrać audio z filmu YouTube."
        except Exception as e:
            return f"Wystąpił błąd: {str(e)}"
