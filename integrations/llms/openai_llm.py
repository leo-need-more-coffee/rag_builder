from ...base import BaseLLM, BaseVectorDB, BaseVectorizer

try:
    import openai
except ImportError as e:
    print(e)
    print("OpenAI library not found. Please install it using 'pip install openai'")
    exit()


class OpenAIPrompts:
    COMMANDS_PROMPT = """
To use a function, respond with the string: `{pattern}`, where `name` is the function's name and `data` is the data you
wish to pass to that function. Below is a list of available functions and their descriptions:
{func_list}

**Example dialogue:**
**User:** What day is it today?
**You:** `<RUNFUNC>get_current_date()</RUNFUNC>`
**System:** 2022-01-01
**You:** 2022-01-01

**User:** Thank you, when did the Roman Empire collapse?
**You:** `<RUNFUNC>get_info({{"query": "The Collapse of the Roman Empire"}})</RUNFUNC>`
**System:** 476
**You:** 476

**Important Reminders:**
1. To use a function, reply **only** with the function string.
2. Once you receive the data, answer the user's
"""

    AGENT_PROMPT = """
You are an assistant working with the system, you are its interface.
You must help the user using the command and context.
You will execute the commands, not the user.
System messages may be attached to the user's message, which you must carefully study and answer the user's question.
The user does not see system messages.
Answer as if the system does not exist, and you yourself were looking for the answer to the user's question.
The data that the system gives you is the objective truth, you should not change it.
Where possible, you should always use the system to obtain data.
If the system information does not contain an answer to the user's question, reply "Unfortunately, I cannot find an answer to your question"
"""


class OpenAILLM(BaseLLM):  # noqa
    db: BaseVectorDB
    vectorizer: BaseVectorizer
    prompts = OpenAIPrompts()

    api_key: str
    base_url: str

    prepare_model: str
    prepare_prompt: str

    llm_model: str
    client: openai.Client

    def __init__(
        self,
        db: BaseVectorDB,
        vectorizer: BaseVectorizer,

        api_key,
        base_url='https://api.openai.com/v1',

        prepare_model='gpt-3.5-turbo',
        prepare_prompt='',

        llm_model='gpt-3.5-turbo',
    ):
        super().__init__(db, vectorizer)
        self.api_key = api_key
        self.base_url = base_url

        self.prepare_model = prepare_model
        self.prepare_prompt = prepare_prompt

        self.llm_model = llm_model
        self.client = openai.Client(api_key=self.api_key, base_url=self.base_url)

    def prepare_query(self, query: str) -> str:
        return query

    def generate_response(self, messages: list | None) -> str:
        msgs = []
        for message in messages:
            match message['role']:
                case 'user':
                    msgs.append({"role": "user", "content": message['content']})
                case 'system':
                    msgs.append({"role": "system", "content": "SYSTEM INFO: " + message['content']})
                case 'assistant':
                    msgs.append({"role": "assistant", "content": message['content']})

        response = self.client.chat.completions.create(
            messages=messages,
            model=self.llm_model,
        )
        return response.choices[0].message.content
