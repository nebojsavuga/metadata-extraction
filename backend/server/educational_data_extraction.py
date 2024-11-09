def get_interactivity_type(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get Interactivity type. Answers are active, expositive, mixed"""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the interactivity type of this text: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: active, expositive, mixed. Don't explain answers. Only choose 1 of the given choices. "Active" learning (e.g., learning by doing). An active 
learning object prompts the learner for 
semantically meaningful input or for some 
other kind of productive action or decision, 
not necessarily performed within the learning 
object's framework. Active documents 
include simulations, questionnaires, and 
exercises. 
"Expositive" learning (e.g., passive learning) 
occurs when the learner's job mainly consists 
of absorbing the content exposed to him 
(generally through text, images or sound). An 
expositive learning object displays 
information but does not prompt the learner 
for any semantically meaningful input. 
Expositive documents include essays, video 
clips, all kinds of graphical material, and 
hypertext documents. 
When a learning object blends the active and 
expositive interactivity types, then its 
interactivity type is "mixed". """,
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_interactivity_level(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get Interactivity level."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the interactivity level of this text: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: very low, low, medium, high, very high. Don't explain answers. Only choose 1 of the given choices""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_learning_resource_type(
    textAnalyzer, text, model, temperature, max_tokens, top_p
):
    """Get learning resource type."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the learning resource type of this text: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: exercise, simulation, questionnaire, diagram, figure, graph, index, slide, table, narrative text, exam, experiment, problem statement, self assessment lecture. Don't explain answers. Only choose 1 of the given choices""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_semantic_density(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get learning resource type."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the semantic density of this text: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: very low, low, medium, high, very high. Don't explain answers. Only choose 1 of the given choices""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_intended_user_role(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get intended user role."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the intended user role for text: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: teacher, author, learner, manager. Don't explain answers. Only choose 1 of the given choices""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_educational_context(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get context."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the principal environment within which the learning and use of this learning object is intended to take place.: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: school, higher education, training, other. Don't explain answers. Only choose 1 of the given choices""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_typical_age_range(textAnalyzer, text, model, temperature, max_tokens, top_p):
    """Get typical age range."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"What is the typical age range of user for this text: '{text}'",
            },
            {
                "role": "system",
                "content": """Give me an answer in following format: n years- m years. No explanation needed""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_dificulty(
    textAnalyzer, text, intended_user_role, model, temperature, max_tokens, top_p
):
    """Get dificulty."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"How hard it is to work with or through this learning object for the typical intended target audience. '{intended_user_role}' Learning object: '{text}'",
            },
            {
                "role": "system",
                "content": """Answers: very easy, easy, medium, difficult, very difficult. Don't explain answers. Only choose 1 of the given choices""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_learning_time(
    textAnalyzer, text, context, age_range, model, temperature, max_tokens, top_p
):
    """Get laerning time."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"How long will it take to learn the given materrial. Age: '{age_range}'. Context: '{context}' Learning object: '{text}'",
            },
            {
                "role": "system",
                "content": """Give me an answer in a timespan. Example 5 days, 1 week, etc. Don't explain answers.""",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()


def get_educational_description(
    textAnalyzer, text, model, temperature, max_tokens, top_p
):
    """Get description."""
    completion = textAnalyzer.client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"How is this learning object intented to be used: '{text}'",
            },
            {
                "role": "system",
                "content": "Example answer: Teacher guidelines that come with a textbook.",
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
    )
    return completion.choices[0].message.content.strip()
