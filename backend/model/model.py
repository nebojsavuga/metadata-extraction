from groq import Groq
import os

class TextAnalyzer:
    def __init__(self, api_key=None):
        self.client = Groq(
            api_key=api_key or os.environ.get("GROQ_API_KEY")
        )

    def get_keywords(self, text, model="llama3-70b-8192", temperature=0.7, max_tokens=1000, top_p=1):
        """Generate keywords from the given text using the Groq API."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"Provide a keywords of the following text: '{text}'"}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content.strip()

# Usage example
if __name__ == "__main__":
    text = (
        "Tradicionalne kuće često nisu prilagođene savremenim potrebama. "
        "Ove kuće zavise od fiksnih i manuelnih procesa. "
        "One ne uzimaju u obzir promenljive uslove i potrebe ljudi. "
        "Zbog žurbe i nepažnje, ljudi zaboravljaju da uključe ili isključe "
        "kućne aparate i sigurnosne uređaje. "
        "Nedostatak automatizacije i kontrole uređajima van doma može "
        "dovesti do veće potrošnje električne energije i smanjene bezbednosti kuće. Internet stvari "
        "(Internet of Things - IoT) mogu da reše probleme sa kojim se susreću tradicionalne kuće. IoT predstavlja "
        "mrežu povezanih fizičkih uređaja. Cilj je razmenjivanje podataka sa ostalim uređajima i elementima sistema. "
        "Uređaji sistema komuniciraju međusobno preko interneta. Raznim vrstama senzora mogu da se detektuju "
        "temperatura, pokret, vlaga i udaljenost. Dobijanjem i analizom vrednosti sa senzora sistem može da upravlja "
        "uređajima bez uticaja čoveka. Pored senzora, ovaj sistem sadrži i aktuatore. Pomoću aktuatora čovek može "
        "da upravlja uređajima i van kuće. Povezivanjem uređaja sa sistemom alarma dobijamo daljinsko praćenje, "
        "automatizaciju, brzu detekciju i preventivno upozorenje."
    )

    analyzer = TextAnalyzer()
    keywords = analyzer.get_keywords(text)
    print(keywords)
