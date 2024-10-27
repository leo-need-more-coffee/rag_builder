from abc import ABC, abstractmethod
from .vector_db import BaseVectorDB
from .vectorizer import BaseVectorizer


class BasePrompts:
    COMMANDS_PROMPT = """
To use a function, reply with a string: {pattern}, where name is the name of the function and data is the data you want to pass to the function.

Here is a list of available commands and their descriptions: {func_list}

IMPORTANT: The data must be in JSON format, not in the usual Python format.
IMPORTANT: You can only use one function at a time.
IMPORTANT: If you want to use a command, REPLY WITH THE FUNCTION STRING ONLY, NOTHING ELSE.
IMPORTANT: You can only use a function if it is in the list above.
IMPORTANT: The user CANNOT run functions, that's your job - just reply with the function string.
IMPORTANT: The user CANNOT see system messages, so you have to answer their questions.
IMPORTANT: If you got the data you wanted, answer the user's question,
DO NOT USE COMMANDS WHEN ANSWERING THE USER'S QUESTION, OTHERWISE THE USER WILL NOT SEE YOUR MESSAGE.
"""

    AGENT_PROMPT = """
You are an assistant working with the system, you are its interface.
You must help the user using the command and context.
You will execute the commands, not the user.
System messages may be attached to the user's message, which you must carefully study and answer the user's question.
THE USER DOES NOT SEE SYSTEM MESSAGES.
Answer as if the system does not exist, and you yourself were looking for the answer to the user's question.
THE DATA THAT THE SYSTEM GIVES YOU IS THE OBJECTIVE TRUTH, YOU SHOULD NOT CHANGE IT.
WHERE POSSIBLE, YOU SHOULD ALWAYS USE THE SYSTEM TO OBTAIN DATA.

Example of a dialogue:
User: What day is it today?
You: <RUNFUNC>get_current_date()</RUNFUNC>
System: 2022-01-0 You: 2022-01-01
User: Thank you, when did the Roman Empire collapse?
You: <RUNFUNC>get_info({"query": "The Collapse of the Roman Empire"})</RUNFUNC>
System: 476
You: 476

1. The user asks a question.
2. You use a command if it is necessary for the answer, IF YOU DON'T NEED COMMANDS, YOU DON'T HAVE TO USE THEM.
3. The system returns the data to you.
4. You analyze the information received and compose an answer, if the information is little or unimportant, then you can return to point 2.
"""


class BaseLLM(ABC):
    db: BaseVectorDB
    vectorizer: BaseVectorizer
    prompts = BasePrompts()

    def __init__(self, db: BaseVectorDB, vectorizer: BaseVectorizer):
        self.db = db
        self.vectorizer = vectorizer

    def vectorize(self, text: str) -> list[float]:
        """Convert input text to its vector representation."""
        return self.vectorizer.vectorize(text)

    def prepare_query(self, query: str) -> str:
        """Prepare the input query for searching."""
        return query

    def search_query(self, query: str, num_results: int) -> list[dict]:
        """Search the query in the vector database."""
        query = self.prepare_query(query)
        vector = self.vectorize(query)
        return self.db.query(vector, num_results)

    @abstractmethod
    def generate_response(self, messages: list | None) -> str:
        """Generate a response for the query."""
        pass
