from setuptools import find_packages, setup

setup(
    name = 'Chatbot',
    version = '1.0.0',
    author = 'Jeeval Shah',
    url='https://github.com/JeevalShah/MedicalChatbot',
    packages= find_packages(),
    install_requires=[
        'ctransformers==0.2.27',
        'sentence-transformers==3.0.1',
        'pinecone-client==4.1.1',
        'langchain==0.2.6',
        'flask==3.0.3',
        'pypdf==4.2.0',
        'python-dotenv==1.0.1',
        'langchain-huggingface==0.0.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8'
)