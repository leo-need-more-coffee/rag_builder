from setuptools import setup


setup(
    name="llm-rag-builder",
    version="0.1.4",
    description="Это библиотека на Python, предназначенная для упрощения создания и управления моделями генерации"
                " с использованием поиска (Retrieval-Augmented Generation, RAG).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="лень",
    author_email="pzrnqt1vrss@protonmail.com",
    url="https://github.com/leo-need-more-coffee/rag_builder",
    packages=[
        'rag_builder',
        'rag_builder.core',
        'rag_builder.integrations',
        'rag_builder.integrations.chromadb',
        'rag_builder.integrations.gemini',
        'rag_builder.integrations.openai',
        'rag_builder.integrations.pgvector',
        'rag_builder.integrations.yandex',
        'rag_builder.utils'
    ],
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
