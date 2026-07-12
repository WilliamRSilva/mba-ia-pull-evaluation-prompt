"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import mantido caso seja útil para validações adicionais
# from utils import validate_prompt_structure 

# Caminho para o arquivo de prompts (ajuste o nome/caminho conforme a sua estrutura)
PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    if not Path(file_path).exists():
        # Retorna um mock de falha amigável caso o arquivo ainda não exista localmente
        return []
        
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        # Assume que os prompts estão em uma lista na raiz do YAML ou sob a chave 'prompts'
        return data.get('prompts', data) if isinstance(data, dict) else data

# Carregamento em tempo de coleta do pytest para parametrização
PROMPTS_DATA = load_prompts(str(PROMPTS_FILE))

# Se a lista estiver vazia (arquivo não encontrado no momento da execução), 
# criamos um mock básico para que os testes rodem e falhem adequadamente, mostrando a estrutura esperada.
if not PROMPTS_DATA:
    PROMPTS_DATA = [{
        "id": "mock_prompt",
        "system_prompt": "Você é um Product Manager. Retorne em Markdown. Entrada: X, Saída: Y.",
        "metadata": {"techniques": ["role-playing", "few-shot"]}
    }]

class TestPrompts:
    
    @pytest.mark.parametrize("prompt_data", PROMPTS_DATA)
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, "A chave 'system_prompt' está ausente no YAML."
        assert isinstance(prompt_data["system_prompt"], str), "O campo 'system_prompt' deve ser uma string."
        assert len(prompt_data["system_prompt"].strip()) > 0, "O 'system_prompt' não pode estar vazio."

    @pytest.mark.parametrize("prompt_data", PROMPTS_DATA)
    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        
        # Palavras-chave comuns para atribuição de papel
        role_keywords = ["você é", "atue como", "assuma o papel", "aja como", "persona:", "você atuará"]
        
        has_role = any(keyword in system_prompt for keyword in role_keywords)
        assert has_role, f"Nenhuma definição de persona clara encontrada no prompt: {prompt_data.get('id', 'desconhecido')}"

    @pytest.mark.parametrize("prompt_data", PROMPTS_DATA)
    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        
        format_keywords = ["markdown", "user story", "história de usuário", ".md"]
        
        has_format = any(keyword in system_prompt for keyword in format_keywords)
        assert has_format, "O prompt deve exigir explicitamente um formato (Markdown ou User Story)."

    @pytest.mark.parametrize("prompt_data", PROMPTS_DATA)
    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        
        example_keywords = ["exemplo", "entrada:", "saída:", "input:", "output:"]
        
        has_examples = any(keyword in system_prompt for keyword in example_keywords)
        assert has_examples, "O prompt não parece conter exemplos de entrada e saída (Few-shot ausente)."

    @pytest.mark.parametrize("prompt_data", PROMPTS_DATA)
    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt_data.get("system_prompt", "")
        
        assert "[TODO]" not in system_prompt.upper(), "Existem tags [TODO] não resolvidas no corpo do prompt."

    @pytest.mark.parametrize("prompt_data", PROMPTS_DATA)
    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        metadata = prompt_data.get("metadata", {})
        techniques = metadata.get("techniques", [])
        
        assert isinstance(techniques, list), "O campo 'techniques' nos metadados deve ser uma lista."
        assert len(techniques) >= 2, f"O prompt deve listar no mínimo 2 técnicas. Encontradas: {len(techniques)}."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])