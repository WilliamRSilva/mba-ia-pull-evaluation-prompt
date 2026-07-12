"""Upload dataset to LangSmith with metadata support."""
import json
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client

# Carrega as variáveis de ambiente do seu arquivo .env
load_dotenv()

SCRIPT_DIR = Path(__file__).parent
# Sobe para a raiz e entra na pasta 'data'
DATASET_FILE = SCRIPT_DIR.parent / "datasets" / "bug_to_user_story.jsonl" 
DATASET_NAME = "bug_to_user_story"

# 1. Inicializa o cliente oficial do LangSmith
# Ele vai ler automaticamente as chaves LANGCHAIN_API_KEY do seu .env
client = Client()

# 2. Cria o dataset no LangSmith se ele não existir
if not client.has_dataset(dataset_name=DATASET_NAME):
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Bug to User Story conversion dataset"
    )
    print(f"Dataset '{DATASET_NAME}' criado com sucesso.")
else:
    print(f"Dataset '{DATASET_NAME}' já existe. Atualizando exemplos...")

# 3. Lê o arquivo dataset.jsonl e faz o upload dos exemplos
count = 0
if DATASET_FILE.exists():
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            
            # Converte a linha JSONL em dicionário Python
            data = json.loads(line)
            
            # O formato esperado depende do seu jsonl, geralmente possui 'inputs' e 'outputs'
            # Aqui fazemos o upload de cada linha como um exemplo
            client.create_example(
                inputs=data.get("inputs", data), 
                outputs=data.get("outputs", None),
                metadata=data.get("metadata", None),
                dataset_name=DATASET_NAME
            )
            count += 1
            
    print(f"Dataset '{DATASET_NAME}' atualizado com {count} exemplos.")
else:
    print(f"Erro: O arquivo {DATASET_FILE} não foi encontrado na pasta 'src'.")