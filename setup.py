from setuptools import setup, find_packages


setup(
    name="llm-rag-builder",
    version="0.1.0",
    description="Это библиотека на Python, предназначенная для упрощения создания и управления моделями генерации с использованием поиска (Retrieval-Augmented Generation, RAG).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="лень",
    author_email="pzrnqt1vrss@protonmail.com",
    url="https://github.com/leo-need-more-coffee/rag_builder",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
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
