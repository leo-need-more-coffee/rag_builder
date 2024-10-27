from rag_builder.integrations import YandexLLM, YandexVectorizer, PgVectorVDB
from rag_builder.base import BaseDialog, BaseCommand
from uuid import uuid4


vectorizer = YandexVectorizer(
    api_key="API_KEY",
    catalog_id='CATALOG_ID'
)

vdb = PgVectorVDB(
    vectorizer=vectorizer,
    dbname='vector_db',
    user='test',
    password='test',
    host='0.0.0.0',
    port='5432'
)

llm = YandexLLM(
    db=vdb,
    vectorizer=vectorizer,
    api_key="API_KEY",
    catalog_id='CATALOG_ID'
)

dialog = BaseDialog(
    llm=llm,
    title='Ya Dialog'
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
    description='Получает информацию из БД с помощью текстовых запросов. Если вы хотите узнать ответ на свой вопрос, воспользуйтесь этой командой.',
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
chunks = ['секретный код #1 is 1234', 'секретный код #2 is 3432', 'секретный код #3 is 23123']
for chunk in chunks:
    vdb.insert(uuid=str(uuid4()), text=chunk, meta={'type': 'secret_code'})

# questions about secret codes
dialog.proccess_user_message('Сколько время?')
dialog.proccess_user_message('Какая погода?')
dialog.proccess_user_message('Какой секретный код #3?')

messages = dialog.get_dialog()
for message in messages:

    if message['content'].endswith('\n'):
        message['content'] = message['content'][:-1]

    print(f"{message['role'].upper()}: {message['content']}\n")
