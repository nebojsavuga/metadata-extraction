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


def get_learning_resource_type(textAnalyzer, text, model, temperature, max_tokens, top_p):
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
