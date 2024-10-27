from abc import ABC
from uuid import uuid4

from .llm import BaseLLM
from .command import BaseCommand, RUN_COMMAND_STRING


class BaseDialog(ABC):
    llm: BaseLLM
    uuid: str | None
    title: str
    commands: list[BaseCommand] | None
    _messages: list[dict]

    def __init__(
            self,
            llm: BaseLLM,
            uuid: str | None = None,
            title: str = 'Untitled dialog',
            commands: list[BaseCommand] | None = None,
            messages: list[dict] = None
    ):
        self.llm = llm
        self.uuid = uuid or str(uuid4())
        self.title = title
        self.commands = commands or []
        self._messages = messages or []

    def add_user_message(self, text: str) -> None:
        self._messages.append({'role': 'user', 'content': text})

    def add_system_message(self, text: str) -> None:
        self._messages.append({'role': 'system', 'content': text})

    def add_agent_message(self, text: str) -> None:
        self._messages.append({'role': 'assistant', 'content': text})

    def add_command(self, command: BaseCommand) -> None:
        """Add a command to the dialog."""
        self.commands.append(command)

    def add_command_prompt(self, additional_prompt: str = "") -> None:
        func_list = "\n"
        for command in self.commands:
            func_list += command.explain_command() + "\n"

        self.add_system_message(
            additional_prompt + self.llm.prompts.COMMANDS_PROMPT.format(
                pattern=RUN_COMMAND_STRING.format(name='func_name', data='{"arg": "value"}'),
                func_list=func_list
            )
        )

    def get_dialog(self) -> list[dict]:
        """Return the dialog as a dictionary."""
        return self._messages

    def context_list_to_string(self, context_list: list[dict]) -> str:
        """Convert the context list to a string."""
        return "\n\n".join([context["text"] for context in context_list])

    def generate_agent_message(self) -> None:
        """Generate a response for the user message."""
        agent_message = self.llm.generate_response(self._messages)
        self.add_agent_message(agent_message)

    def proccess_user_message(self, query: str, reach=False, reach_num=5) -> list[dict]:
        """Process the user message."""
        self.add_user_message(query)

        if reach:
            context_list = self.llm.search_query(query, reach_num)
            context_string = self.context_list_to_string(context_list)
            self.add_system_message(context_string)

        for _ in range(3):  # Limit the number of commands in row
            self.generate_agent_message()
            for command in self.commands:
                if command.check_is_command(self._messages[-1]['content']):
                    request = self._messages.pop(-1)
                    msg = f"\nREQUEST: {request}\nSYSTEM RESPONSE:" + command.run(self._messages[-1]['content'])
                    self.add_system_message(msg)
                    break
            else:
                break

        return self.get_dialog()
