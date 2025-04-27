import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        # Correction : utilisation de attrs={"indent": "0"}
        elements = soup.find_all("td", class_="ind", attrs={"indent": "0"})

        comments = [e.find_next(class_="comment") for e in elements if e]

        keywords = {"python": 0, "javascript": 0, "typescript": 0, "go": 0, "c#": 0, "java": 0, "rust": 0}

        for comment in comments:
            if comment:
                comment_text = comment.get_text().lower()
                words = {w.strip(".,/:;!@") for w in comment_text.split()}

                for k in keywords:
                    if k in words:
                        keywords[k] += 1

        print(keywords)

        plt.figure(figsize=(10, 6))
        plt.bar(keywords.keys(), keywords.values())
        plt.xlabel("Langage")
        plt.ylabel("# de Mentions")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")


if __name__ == "__main__":
    main()