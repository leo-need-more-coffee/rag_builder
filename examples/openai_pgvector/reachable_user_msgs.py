from rag_builder.integrations import OpenAILLM, OpenAIVectorizer, PgVectorVDB
from rag_builder.base import BaseDialog
from uuid import uuid4

vectorizer = OpenAIVectorizer(
    api_key="API_KEY",
    base_url=None,
    embeddings_model="text-embedding-3-small",
)

vdb = PgVectorVDB(
    vectorizer=vectorizer,
    dbname='vector_db',
    user='test',
    password='test',
    host='0.0.0.0',
    port='5432'
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

# Add some prompts to the dialog
dialog.add_system_message('When user asks about secret code, provide the secret code.')
dialog.add_system_message('The secret code is a number.')
dialog.add_system_message('System will provide the secret code when user asks about it.')

# Add some secret codes in vector database
chunks = ['secret code #1 is 1234', 'secret code #2 is 3432', 'secret code #3 is 23123']
for chunk in chunks:
    vdb.insert(uuid=str(uuid4()), text=chunk, meta={'type': 'secret_code'})

# questions about secret codes
dialog.proccess_user_message('What is the secret code #1?', True, 3)
dialog.proccess_user_message('What is the secret code #2?', True, 3)
dialog.proccess_user_message('What is the secret code #3?', True, 3)

messages = dialog.get_dialog()
for message in messages:

    if message['content'].endswith('\n'):
        message['content'] = message['content'][:-1]

    print(f"{message['role'].upper()}: {message['content']}\n")
