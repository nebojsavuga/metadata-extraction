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
            "content": "When was the Kosovo Batle"
        },
        {
            "role": "assistant",
            "content": "When was the kosovo battle"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message)