# rag_builder

`rag_builder` — это библиотека на Python, предназначенная для упрощения создания и управления моделями генерации с использованием поиска (Retrieval-Augmented Generation, RAG). Библиотека интегрируется с различными языковыми моделями и предоставляет удобный интерфейс для создания, запроса и управления диалоговыми системами.

## Возможности

- **Управление командами**: Легко добавляйте и управляйте командами для вашей диалоговой системы.
- **Интеграция с LLM**: Используйте различные языковые модели для генерации текста.
- **Интеграция с Vector DB**: Используйте различные базы данных векторов для поиска похожих запросов.
- **Интеграция с Vectorizers**: Используйте различные инструменты для преобразования текста в векторное представление.

## Интеграции
| Модели           | Минимальная интеграция | Оптимизированная интеграция | Полностью интегрировано |
|------------------|-----------------|-----------------------------|--------------------------|
| **LLMs:**        |                 |                             |                          |
| OpenAI models    | ✅                | ⬜                           | ⬜                        |
| Yandex models    | ✅                | ⬜                           | ⬜                        |
| Gemini models    | ✅                | ⬜                           | ⬜                        |
| **Vector DB:**   |                 |                             |                          |
| Chroma           | ✅                | ⬜                           | ⬜                        |
| pgvector         | ✅                | ⬜                           | ⬜                        |
| **Vectorizers:** |                 |                             |                          |
| OpenAI embeddings| ✅                | ⬜                           | ⬜                        |
| Yandex embeddings| ✅                | ⬜                           | ⬜                        |


## Установка

Для установки `rag_builder` можно использовать pip:

```bash
# Без интеграций
pip install llm-rag-builder

# Все интеграции
pip install "llm-rag-builder[all]"  

# Интеграции по отдельности
pip install "llm-rag-builder[openai]"
pip install "llm-rag-builder[yandex]"
pip install "llm-rag-builder[gemini]"
pip install "llm-rag-builder[chroma]"
pip install "llm-rag-builder[pgvector]"
```

## Использование

### Базовая настройка

Пример настройки базовой диалоговой системы с использованием `rag_builder`:

```python
from rag_builder import BaseDialog, BaseCommand, YandexLLM, GeminiLLM

# Инициализация LLM
llm = GeminiLLM(
    db=vdb,
    vectorizer=vectorizer,
    api_key="YOUR_API_KEY",
    llm_model="gemini-1.5-flash",
)

# Создание экземпляра диалога
dialog = BaseDialog(
    llm=llm,
    title='OpenAI Dialog'
)

# Определение команд
get_time_func = BaseCommand(
    name='get_time',
    description='Получить текущее время.',
    examples=['get_time()'],
    run=lambda args: f"Текущее время 12:00",
)

get_weather_func = BaseCommand(
    name='get_weather',
    description='Получить текущую погоду.',
    examples=['get_weather()'],
    run=lambda args: f"Текущая погода солнечная",
)

# Добавление команд в диалог
dialog.add_command(get_time_func)
dialog.add_command(get_weather_func)

# Обработка сообщения пользователя
dialog.proccess_user_message('Какая погода?')
```
Вывод:
```
USER: Какая погода?
ASSISTANT: <RUNFUNC> get_weather() </RUNFUNC>
SYSTEM: Текущая погода солнечная
ASSISTANT: Текущая погода солнечная
```

Больше примеров использования можно найти в папке `examples`.
## Вклад

Ваши идеи и вклад приветствуются! Пожалуйста, отправляйте запросы на добавление изменений (pull requests) или открывайте issue для обсуждения ваших идей.

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности можно найти в файле `LICENSE`.

## Контакты

По любым вопросам и запросам обращайтесь на [pzrnqt1vrss@protonmail.com](mailto:pzrnqt1vrss@protonmail.com)