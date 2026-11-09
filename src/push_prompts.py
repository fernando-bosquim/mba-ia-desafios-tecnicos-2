"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    is_valid, errors = validate_prompt_structure(prompt_data)

    user_prompt = prompt_data.get("user_prompt", "")
    if "{bug_report}" not in user_prompt:
        errors.append("user_prompt deve conter a variável {bug_report}")
        is_valid = False

    return (is_valid, errors)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt (ex: bug_to_user_story_v2)
        prompt_data: Dados do prompt carregados do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurado no .env")
        return False

    full_prompt_name = f"{username}/{prompt_name}"

    try:
        client = Client()
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "{bug_report}")

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt),
        ])

        description = prompt_data.get(
            "description",
            "Prompt para converter relatos de bugs em User Stories",
        )
        tags = prompt_data.get("tags", [])
        techniques = prompt_data.get("techniques_applied", [])
        if techniques:
            tags = list(set(tags + [t.lower().replace(" ", "-") for t in techniques]))

        print(f"🚀 Enviando prompt para o LangSmith Hub: {full_prompt_name} (público)...")

        url = client.push_prompt(
            full_prompt_name,
            object=prompt_template,
            is_public=True,
            description=description,
            tags=tags,
        )

        print(f"   ✓ Prompt publicado com sucesso!")
        print(f"   ✓ URL pública: {url}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt '{full_prompt_name}': {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    yaml_path = Path("prompts") / "bug_to_user_story_v2.yml"
    if not yaml_path.exists():
        print(f"❌ Arquivo não encontrado: {yaml_path}")
        return 1

    prompts = load_yaml(str(yaml_path))
    if not prompts:
        print("❌ Não foi possível carregar os prompts do arquivo YAML.")
        return 1

    all_success = True

    for prompt_name, prompt_data in prompts.items():
        print(f"\n🔍 Validando prompt: {prompt_name}...")
        is_valid, errors = validate_prompt(prompt_data)

        if not is_valid:
            print(f"   ❌ Prompt '{prompt_name}' inválido:")
            for err in errors:
                print(f"      - {err}")
            all_success = False
            continue

        print("   ✓ Estrutura válida")
        success = push_prompt_to_langsmith(prompt_name, prompt_data)
        if not success:
            all_success = False

    if all_success:
        print("\n✅ Todos os prompts foram validados e publicados com sucesso!")
        return 0
    else:
        print("\n❌ Ocorreram erros durante o push de prompts.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
