from groq import Groq
import os
import datetime

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": "From this: 'Tradicionalne kuće često nisu prilagođene savremenim potrebama. Ove kuće zavise od fiksnih i manuelnih procesa.  One ne uzimaju u obzir promenljive uslove i potrebe ljudi. Zbog žurbe i nepažnje, ljudi zaboravljaju da uključe ili isključe kućne aparate i sigurnosne uređaje. Nedostatak automatizacije i kontrole uređajima van doma može dovesti do veće potrošnje električne energije i smanjene bezbednosti kuće.' Create Summary"
        },
        {
            "role": "assistant",
            "content": "Summarize text"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message.content)