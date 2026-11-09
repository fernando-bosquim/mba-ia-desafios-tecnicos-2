"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_V2_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega os dados do prompt v2 para cada teste."""
        assert PROMPT_V2_PATH.exists(), f"Arquivo não encontrado: {PROMPT_V2_PATH}"
        data = load_prompts(str(PROMPT_V2_PATH))
        assert "bug_to_user_story_v2" in data, "Chave 'bug_to_user_story_v2' não encontrada no YAML"
        self.prompt_data = data["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data, "Campo 'system_prompt' ausente no prompt"
        system_prompt = self.prompt_data.get("system_prompt")
        assert system_prompt is not None, "Campo 'system_prompt' é None"
        assert len(system_prompt.strip()) > 0, "Campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt_data["system_prompt"].lower()
        role_indicators = [
            "você é um product manager",
            "você é",
            "product manager",
            "especialista em qa",
        ]
        assert any(
            indicator in system_prompt for indicator in role_indicators
        ), "Nenhuma persona/papel definido no system_prompt"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_data["system_prompt"].lower()
        format_indicators = [
            "markdown",
            "user story",
            "como um",
            "eu quero",
            "para que",
            "critérios de aceitação",
        ]
        assert any(
            indicator in system_prompt for indicator in format_indicators
        ), "O prompt não especifica o formato de saída (Markdown ou User Story)"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_data["system_prompt"].lower()
        few_shot_indicators = [
            "few-shot",
            "exemplo",
            "entrada do usuário",
            "resposta esperada",
        ]
        assert any(
            indicator in system_prompt for indicator in few_shot_indicators
        ), "O prompt não contém exemplos de entrada/saída (Few-shot)"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        user_prompt = self.prompt_data.get("user_prompt", "")
        description = self.prompt_data.get("description", "")

        assert "TODO" not in system_prompt, "system_prompt ainda contém marcadores TODO"
        assert "[TODO]" not in system_prompt, "system_prompt ainda contém marcadores [TODO]"
        assert "TODO" not in user_prompt, "user_prompt ainda contém marcadores TODO"
        assert "TODO" not in description, "description ainda contém marcadores TODO"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert (
            "techniques_applied" in self.prompt_data
        ), "Campo 'techniques_applied' ausente nos metadados"
        techniques = self.prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert (
            len(techniques) >= 2
        ), f"Esperado no mínimo 2 técnicas aplicadas, encontrado: {len(techniques)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
