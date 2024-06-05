""" Módulo contendo as funções que acessam a API da OpenAI """

from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat
from inspect import cleandoc
import json


OPENAI_MODEL = "gpt-3.5-turbo-0125"
TEMPERATURE = 1.2

# Carrega a prompt do sistema em uma variável global
with open("system_prompt.txt") as f:
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = f.read()

# A chave OPENAI_API_KEY é definida como uma variável de ambiente
# e lida automaticamente pela biblioteca da OpenAI
gpt_client = OpenAI()


def generate_word(theme: str, language: str, difficulty: str, word_history: list[str]):
    """
    Pede pro modelo da OpenAI criar uma palavra com as características
    desejadas e retorna a palavra gerada.
    """

    # cleandoc(...) remove a tabulação na frente de cada linha
    user_prompt = cleandoc(f"""
    LANGUAGE: {language}
    THEME: {theme}
    DIFFICULTY: {difficulty}
    HISTORY: {", ".join(word_history) if len(word_history) > 0 else "(no history)"}
    """)

    prompt = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    
    response = gpt_client.chat.completions.create(
        messages = prompt,
        model = OPENAI_MODEL,
        temperature = TEMPERATURE,
        # Exige que o modelo retorne uma string JSON
        response_format = ResponseFormat(type = "json_object")
    ).choices[0].message.content

    # Dada a resposta no formato
    #
    # {
    #     "word": "palavra gerada"  
    # }
    #
    # a função extrai e retorna o campo "word" do json

    return json.loads(response)["word"].capitalize()
