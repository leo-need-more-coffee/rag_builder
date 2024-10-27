from setuptools import setup


setup(
    name="rag_builder",
    version="0.1",
    install_requires=[

    ],
    extras_require={
        "all": ["openai", "google-generativeai", "yandex-chain", "chromadb", "psycopg2", "pgvector"],
        "openai": ["openai"],
        "gemini": ["google-generativeai"],
        "yandex": ["yandex-chain"],
        "chroma": ["chromadb"],
        "pgvector": ["psycopg2", "pgvector"]
    }
)
