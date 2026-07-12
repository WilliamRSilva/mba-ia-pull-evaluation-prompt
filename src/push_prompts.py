"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê o prompt otimizado de prompts/bug_to_user_story_v2.yml
2. Valida o prompt
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.load import load as lc_load
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

# Caminhos do projeto (script fica em scripts/, os arquivos de dados ficam na raiz)
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "bug_to_user_story_v2.yml"
README_PATH = BASE_DIR / "README.md"

# Nome do prompt no Hub (sem o owner). O owner vem de USERNAME_LANGSMITH_HUB.
PROMPT_NAME = "bug_to_user_story_v2"

# Metadados do prompt: descrição e tags com as técnicas utilizadas.
PROMPT_DESCRIPTION = (
    "Transforma relatos de bugs de usuários em User Stories no formato INVEST, "
    "com criterios de aceitacao em Gherkin. Tecnicas de prompt engineering "
    "aplicadas: Role Prompting, Few-shot, Chain of Thought "
)
PROMPT_TAGS = [
    "bug-to-user-story",
    "role-prompting",
    "few-shot",
    "chain-of-thought",
    "product-management",
    "v2",
]


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt (dicionário carregado do YAML).

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros.
    """
    errors: list[str] = []

    if not isinstance(prompt_data, dict):
        return False, ["O arquivo YAML não representa um objeto/dicionário válido."]

    if prompt_data.get("type") != "constructor":
        errors.append("Campo 'type' ausente ou diferente de 'constructor'.")

    kwargs = prompt_data.get("kwargs")
    if not kwargs:
        errors.append("Campo 'kwargs' ausente no prompt.")
        return False, errors

    input_variables = kwargs.get("input_variables")
    if not input_variables:
        errors.append("'kwargs.input_variables' ausente ou vazio.")
    elif "bug_report" not in input_variables:
        errors.append("Variável obrigatória 'bug_report' não está em input_variables.")

    messages = kwargs.get("messages")
    if not messages or not isinstance(messages, list):
        errors.append("'kwargs.messages' ausente ou vazio.")
    else:
        roles_found = set()
        for i, message in enumerate(messages):
            message_id = message.get("id", [])
            if not message_id:
                errors.append(f"Mensagem {i}: campo 'id' ausente.")
                continue
            role = message_id[-1]
            roles_found.add(role)

            template = (
                message.get("kwargs", {})
                .get("prompt", {})
                .get("kwargs", {})
                .get("template", "")
            )
            if not template or not str(template).strip():
                errors.append(f"Mensagem {i} ({role}): template vazio.")

        if "SystemMessagePromptTemplate" not in roles_found:
            errors.append(
                "Nenhuma SystemMessagePromptTemplate encontrada "
                "(persona, regras e exemplos few-shot devem estar no System Message)."
            )
        if "HumanMessagePromptTemplate" not in roles_found:
            errors.append(
                "Nenhuma HumanMessagePromptTemplate encontrada "
                "(a entrada dinâmica do usuário deve estar no Human Message)."
            )

    return (len(errors) == 0, errors)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (sem o owner), ex: "bug_to_user_story_v2".
        prompt_data: Dados do prompt (dicionário carregado do YAML).

    Returns:
        True se sucesso, False caso contrário.
    """
    owner = os.getenv("USERNAME_LANGSMITH_HUB")
    if not owner:
        print("Erro: variável de ambiente USERNAME_LANGSMITH_HUB não definida.")
        return False

    prompt_identifier = f"{owner}/{prompt_name}"

    # Reconstrói o objeto ChatPromptTemplate a partir do dicionário serializado no YAML.
    try:
        chat_prompt_template = lc_load(prompt_data)
    except Exception as exc:
        print(f"Erro ao reconstruir o ChatPromptTemplate a partir do YAML: {exc}")
        return False

    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

    client = Client()

    try:
        url = client.push_prompt(
            prompt_identifier,
            object=chat_prompt_template,
            is_public=True,
            description=PROMPT_DESCRIPTION,
            readme=readme,
            tags=PROMPT_TAGS,
        )
    except Exception as exc:
        print(f"Erro ao fazer push do prompt '{prompt_identifier}': {exc}")
        return False

    print(f"Prompt publicado com sucesso em: {url}")
    return True


def main():
    """Função principal"""
    print_section_header("Push de Prompt Otimizado para o LangSmith Hub")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        print(
            "Defina as variáveis de ambiente necessárias (veja .env.example) "
            "e tente novamente."
        )
        return 1

    if not PROMPT_PATH.exists():
        print(f"Erro: arquivo de prompt não encontrado em {PROMPT_PATH}")
        return 1

    prompt_data = load_yaml(str(PROMPT_PATH))

    print_section_header("Validando prompt")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Prompt inválido. Corrija os erros abaixo antes de publicar:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Prompt válido.")

    print_section_header("Publicando prompt no LangSmith Hub")
    success = push_prompt_to_langsmith(PROMPT_NAME, prompt_data)

    if not success:
        print("Falha ao publicar o prompt.")
        return 1

    owner = os.getenv("USERNAME_LANGSMITH_HUB")
    print_section_header("Concluído")
    print(
        f"Verifique o dashboard em: "
        f"https://smith.langchain.com/hub/{owner}/{PROMPT_NAME}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
