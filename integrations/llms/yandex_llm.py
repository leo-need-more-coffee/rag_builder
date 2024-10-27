from ...base import BaseLLM, BaseVectorDB, BaseVectorizer

try:
    from yandex_chain import ChatYandexGPT
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

except ImportError as e:
    print(e)
    print("Yandex library not found. Please install it using 'pip install yandex-chain'")
    exit()


class YandexPrompts:
    COMMANDS_PROMPT = """
**Использование функций:**

Чтобы вызвать функцию, ответьте строкой в формате: {pattern}, где `name` — название функции, а `data` — данные, которые вы хотите передать.

**Список доступных команд:**
{func_list}

**Важные правила:**

0. ОБЯЗАТЕЛЬНО ИСПОЛЬЗУЙ ФОРМАТ {pattern} ДЛЯ ВЫЗОВА ФУНКЦИИ.
1. **Формат данных:** Аргументы функции должны быть в формате JSON, а не в стандартном формате Python.
2. **Ограничение на функции:** Можно использовать только одну функцию за раз.
3. **Ответы:** Если хотите вызвать команду, отвечайте только строкой функции — ничего дополнительного не добавляйте.
4. **Доступ к функциям:** Можно использовать функцию только если она есть в списке выше.
5. **Обязанности:** Пользователь не может запускать функции — это твоя работа. Просто ответь строкой функции.
6. **Системные сообщения:** Пользователь не видит системные сообщения, поэтому нужно отвечать на его вопросы на основе доступных данных.
7. **Ответ на вопросы:** Если ты получил данные, необходимые для ответа, предоставь информацию пользователю,
не используя команды, иначе он не увидит твое сообщение.
"""

    AGENT_PROMPT = """
**Описание задачи:**

Ты являешься интерфейсом системы, предназначенной для помощи пользователю.
Твоя основная задача — предоставлять информацию, используя доступные команды и контекст, без упоминания системы.

**Основные правила:**

1. **Выполнение команд:** Все команды выполняются тобой, а не пользователем.
2. **Системные сообщения:** У пользователя нет доступа к системным сообщениям,
поэтому ты обязан анализировать их и формулировать ответ на основе системной информации.
3. **Формулировка ответов:** Отвечай, как будто ты самостоятельно искал информацию, основываясь на данных системы.
4. **Объективность данных:** Данные, полученные от системы, представляют собой объективную истину. Не изменяй их.
5. **Использование системы:** Всегда используй систему для получения данных, если это необходимо для ответа на вопрос пользователя.
6. **Отказ в случае отсутствия информации:** Если не удаётся найти ответ на вопрос пользователя, отвечай: "К сожалению, я не могу найти ответ на ваш вопрос."
7. **Запрет на публикацию системных сообщений:** Никогда не публикуй системные сообщения и не упоминай о них.

**Пример диалога:**

- **Пользователь:** Какой сегодня день?
- **Ты:** <RUNFUNC>get_current_date()</RUNFUNC>
- **Система:** 2022-01-01
- **Ты:** 2022-01-01

- **Пользователь:** Спасибо, а когда развалилась Римская империя?
- **Ты:** <RUNFUNC>get_info({"query": "Развал Римской империи"})</RUNFUNC>
- **Система:** 476 год
- **Ты:** 476 год

**Процесс работы:**

1. Пользователь задаёт вопрос.
2. Используй команды, если это необходимо для получения ответа. Если команды не требуются, можешь ответить сразу.
3. Система возвращает данные.
4. Анализируй полученную информацию и формулируй ответ. Если информации недостаточно или она нерелевантна, вернись ко второму пункту.
"""

class YandexLLM(BaseLLM):  # noqa
    db: BaseVectorDB
    vectorizer: BaseVectorizer
    prompts = YandexPrompts()

    api_key: str
    catalog_id: str

    prepare_model: str
    prepare_prompt: str

    llm_model: str
    client: ChatYandexGPT

    def __init__(
        self,
        db: BaseVectorDB,
        vectorizer: BaseVectorizer,

        api_key,
        catalog_id,

        prepare_model='yandexgpt',
        prepare_prompt='',

        llm_model='yandexgpt',
    ):
        super().__init__(db, vectorizer)
        self.api_key = api_key
        self.catalog_id = catalog_id

        self.prepare_model = prepare_model
        self.prepare_prompt = prepare_prompt

        self.llm_model = llm_model

        self.client = ChatYandexGPT(api_key=self.api_key, folder_id=self.catalog_id)

    def prepare_query(self, query: str) -> str:
        return query

    def generate_response(self, messages: list | None) -> str:
        msgs = []
        for message in messages:
            match message['role']:
                case 'system':
                    msgs.append(SystemMessage(content="Системное сообщение: " + message['content']))
                case 'user':
                    msgs.append(HumanMessage(content=message['content']))
                case 'assistant':
                    msgs.append(AIMessage(content=message['content']))
                case _:
                    msgs.append(AIMessage(content=message['content']))

        langchain_result = self.client([
            *msgs
        ])

        return langchain_result.content
