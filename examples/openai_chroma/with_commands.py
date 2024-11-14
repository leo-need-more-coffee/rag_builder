from rag_builder.integrations import OpenAILLM, OpenAIVectorizer, PersistentChromaVDB
from rag_builder.base import BaseDialog, BaseCommand
from uuid import uuid4


vectorizer = OpenAIVectorizer(
    api_key="API_KEY",
    base_url=None,
    embeddings_model="text-embedding-3-small",
)

vdb = PersistentChromaVDB(
    vectorizer=vectorizer,
    path="vdb.chromadb"
)

llm = OpenAILLM(
    db=vdb,
    vectorizer=vectorizer,
    api_key="API_KEY",
    base_url=None,
    prepare_model="gpt-3.5-turbo",
    prepare_prompt="",
    llm_model="gpt-3.5-turbo"
)

dialog = BaseDialog(
    llm=llm,
    title='OpenAI Dialog'
)

get_time_func = BaseCommand(
    name='get_time',
    description='Get the current time.',
    examples=[
        'get_time()',
    ],
    run=lambda args: "Current time is 12:00",
)

get_weather_func = BaseCommand(
    name='get_weather',
    description='Get the current weather.',
    examples=[
        'get_weather()',
    ],
    run=lambda args: "Current weather is sunny",
)

get_information_func = BaseCommand(
    name='query_to_db',
    description='Get the information from db by text query. IF YOU CANT ANSWER USER QUESTION, PLEASE USE THIS FUNCTION WITH USER QUERY.',
    params={'query': 'Just text query to search in db.'},
    examples=[
        'query_to_db({"query": "What is the secret code #5?"})',
        'query_to_db({"query": "How to review my code?"})'
    ],
    run=lambda query: dialog.context_list_to_string(llm.search_query(query, 5)),
)

dialog.add_system_message(
    llm.prompts.AGENT_PROMPT
)
dialog.add_command(get_time_func)
dialog.add_command(get_weather_func)
dialog.add_command(get_information_func)
dialog.add_command_prompt()

# Add some secret codes in vector database
chunks = ['secret code #1 is 1234', 'secret code #2 is 3432', 'secret code #3 is 23123']
for chunk in chunks:
    vdb.insert(uuid=str(uuid4()), text=chunk, meta={'type': 'secret_code'})

dialog.proccess_user_message('What time now?')
dialog.proccess_user_message('What is the weather?')
dialog.proccess_user_message('What is the secret code #2?')
dialog.proccess_user_message('What is the secret code #5?')

messages = dialog.get_dialog()
for message in messages:

    if message['content'].endswith('\n'):
        message['content'] = message['content'][:-1]

    print(f"{message['role'].upper()}: {message['content']}\n")
