from groq import Groq
import os
import datetime

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

text = (
    "Tradicionalne kuće često nisu prilagođene savremenim potrebama. "
    "Ove kuće zavise od fiksnih i manuelnih procesa. "
    "One ne uzimaju u obzir promenljive uslove i potrebe ljudi. "
    "Zbog žurbe i nepažnje, ljudi zaboravljaju da uključe ili isključe "
    "kućne aparate i sigurnosne uređaje. "
    "Nedostatak automatizacije i kontrole uređajima van doma može "
    "dovesti do veće potrošnje električne energije i smanjene bezbednosti kuće. Internet stvari"
   "(Internet of Things - IoT) mogu da reše probleme sa kojim se susreću tradicionalne kuće. IoT predstavljaju "
    "mrežu povezanih fizičkih uređaja [1]. Cilj je razmenjivanje podataka sa ostalim uređajima i elementima sistema."
   " Uređaji sistema komuniciraju međusobno preko interneta [2]. "
	"Raznim vrstama senzora mogu da se detektuju temperatura, pokret, vlaga i udaljenost. Dobijanjem i analizom"
 "vrednosti sa senzora sistem može da upravlja uređajima bez uticaja čoveka. Pored senzora, ovaj sistem sadrži i aktuatore."
" Pomoću aktuatora čovek može da upravlja uređajima i van kuće. Povezivanjem uređaja sa sistemom alarma dobijamo daljinsko"
" praćenje, automatizaciju, brzu detekciju i preventivno upozorenje."

)

# Poziv za sažetak celokupnog teksta
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "user", "content": f"Provide a keywords of the following text: '{text}'"}
    ],
    temperature=0.7,
    max_tokens=150,  # Ograničenje za dužinu sažetka
    top_p=1,
    stream=False,
)

# Ispis sažetka
summary = completion.choices[0].message.content.strip()
print(summary)