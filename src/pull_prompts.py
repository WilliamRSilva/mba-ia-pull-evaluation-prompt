"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
import yaml
from dotenv import load_dotenv
import langchainhub as hub
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header
from pathlib import Path
from langchain_core.load import dumpd

env_path = Path(__file__).resolve().parent.parent / ".env"  # ajuste conforme onde o .env estiver

print(env_path)
load_dotenv(env_path)

def pull_prompts_from_langsmith():
    client = Client()
    prompt = client.pull_prompt("leonanluppi/bug_to_user_story_v1", dangerously_pull_public_prompt=True)
    return prompt

def main():
    """Função principal"""
    prompt = pull_prompts_from_langsmith()
    output_path = Path(__file__).resolve().parent.parent / "prompts" / "bug_to_user_story_v1.yml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    prompt_dict = dumpd(prompt)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(prompt_dict, f, allow_unicode=True, sort_keys=False)

    print(f"Prompt salvo em: {output_path}")

if __name__ == "__main__":
    sys.exit(main())
