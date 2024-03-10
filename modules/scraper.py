import requests
from bs4 import BeautifulSoup
import re


class Scrapper:
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
