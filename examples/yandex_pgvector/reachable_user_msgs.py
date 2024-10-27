from rag_builder.integrations import YandexLLM, YandexVectorizer, PgVectorVDB
from rag_builder.base import BaseDialog
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

# Add some prompts to the dialog
dialog.add_system_message('Когда пользователь спрашивает секретный код, отвечай секретным кодом.')
dialog.add_system_message('Система будет предоставлять секретный код, когда пользователь спросит об этом.')

# Add some secret codes in vector database
chunks = ['секретный код #1 is 1234', 'секретный код #2 is 3432', 'секретный код #3 is 23123']
for chunk in chunks:
    vdb.insert(uuid=str(uuid4()), text=chunk, meta={'type': 'secret_code'})

# questions about secret codes
dialog.proccess_user_message('Какой секретный код #1?', True, 3)
dialog.proccess_user_message('Какой секретный код #2?', True, 3)
dialog.proccess_user_message('Какой секретный код #3?', True, 3)

messages = dialog.get_dialog()
for message in messages:

    if message['content'].endswith('\n'):
        message['content'] = message['content'][:-1]

    print(f"{message['role'].upper()}: {message['content']}\n")
