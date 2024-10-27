from ...base import BaseLLM, BaseVectorDB, BaseVectorizer

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError as e:
    print(e)
    print("google-generativeai library not found. Please install it using 'pip install -q -U google-generativeai'")
    exit()


class GeminiPrompts:
    COMMANDS_PROMPT = """
**Using Functions:**

To call a function, reply with a string in the format: {pattern}, where `name` is the function name and `data` is the data you want to pass.

**List of Available Commands:**
{func_list}

**Important Rules:**

0. ALWAYS USE THE {pattern} FORMAT TO CALL A FUNCTION.
1. **Data Format:** Function arguments must be in JSON format, not standard Python format.
2. **Function Limitation:** You can only use one function at a time.
3. **Responses:** If you want to call a command, reply with just the function string — don't add anything extra.
4. **Access to Functions:** You can only use a function if it's in the list above.
5. **Responsibilities:** The user cannot run functions — that's your job. Just reply with a function string.
6. **System Messages:** The user does not see system messages, so you need to answer their questions based on the data available.
7. **Answering Questions:** If you have received the data needed to answer, provide the information to the user without
using commands, otherwise they will not see your message.
"""

    AGENT_PROMPT = """
**Task Description:**

You are an interface for a system designed to assist users. Your primary role is to provide information based on
available commands and context, without mentioning the system.

**Main Rules:**

1. **Executing Commands:** You execute all commands yourself on behalf of the user.
2. **System Messages:** The user does not have access to system messages, so you must analyze them and respond based on the system’s information.
3. **Answer Formulation:** Formulate responses as if you independently found the information, without referencing the system.
4. **Data Objectivity:** The system data is considered objective truth. Do not alter it.
5. **System Utilization:** Always rely on the system’s data when needed to answer the user’s question.
6. **Response When Lacking Information:** If the system does not contain an answer to the question, respond,
“Unfortunately, I cannot find an answer to your question.”
7. **No Disclosure of System Messages:** Never publish or mention system messages.

**Example Dialogue:**

- **User:** What’s today’s date?
- **You:** <RUNFUNC>get_current_date()</RUNFUNC>
- **System:** 2022-01-01
- **You:** 2022-01-01

- **User:** Thank you! And when did the Roman Empire fall?
- **You:** <RUNFUNC>get_info({"query": "Fall of the Roman Empire"})</RUNFUNC>
- **System:** 476 AD
- **You:** 476 AD

**Working Process:**

1. The user asks a question.
2. Use commands if required to obtain the answer. If a command is not needed, you may answer immediately.
3. The system returns data.
4. Analyze the received information and respond to the user. If the data is insufficient or irrelevant, return to step two.
"""


class GeminiLLM(BaseLLM):  # noqa
    db: BaseVectorDB
    vectorizer: BaseVectorizer

    api_key: str

    prepare_model: str
    prepare_prompt: str

    llm_model: str
    client: genai.GenerativeModel

    def __init__(
        self,
        db: BaseVectorDB,
        vectorizer: BaseVectorizer,

        api_key,

        prepare_model='gemini-1.5-flash',
        prepare_prompt='',

        llm_model='gemini-1.5-flash',
    ):
        super().__init__(db, vectorizer)
        self.api_key = api_key

        self.prepare_model = prepare_model
        self.prepare_prompt = prepare_prompt

        self.llm_model = llm_model
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(
            self.llm_model,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

        )

    def prepare_query(self, query: str) -> str:
        return query

    def generate_response(self, messages: list | None) -> str:
        msgs = []
        for msg in messages:
            match msg['role']:
                case 'user':
                    msgs.append({"role": "user", "parts": msg['content']})
                case 'assistant':
                    msgs.append({"role": "model", "parts": msg['content']})
                case 'system':
                    msgs.append({"role": "user", "parts": 'SYSTEM INFO: ' + msg['content']})
                case _:
                    msgs.append({"role": "model", "parts": msg['content']})

        chat = self.client.start_chat(
            history=msgs[:-1],
        )
        return chat.send_message(msgs[-1]).text
