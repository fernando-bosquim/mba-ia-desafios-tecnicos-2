"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml

DICAS DE IMPLEMENTAÇÃO:

- O pull é feito pelo cliente do LangSmith:

      from langsmith import Client
      client = Client()
      prompt = client.pull_prompt(
          "leonanluppi/bug_to_user_story_v1",
          dangerously_pull_public_prompt=True,
      )

- O parâmetro `dangerously_pull_public_prompt=True` é obrigatório sempre que o
  identificador tem dono explícito ("owner/nome"). O LangSmith bloqueia esse pull
  por padrão porque um prompt do Hub é um objeto LangChain serializado, que pode
  vir de terceiros. Aqui o prompt é o do desafio, então o risco é conhecido.

- O retorno é um ChatPromptTemplate. Para extrair o conteúdo das mensagens,
  use a serialização nativa do LangChain (`prompt.messages`, e o atributo
  `.prompt.template` de cada mensagem).

- Use `save_yaml` de utils.py para gravar o resultado no arquivo .yml.
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
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith() -> bool:
    """
    Conecta ao LangSmith, puxa o prompt semente e salva no arquivo YAML.

    Returns:
        True se sucesso, False caso contrário.
    """
    print_section_header("PULL DE PROMPTS DO LANGSMITH PROMPT HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    prompt_identifier = "leonanluppi/bug_to_user_story_v1"
    output_path = Path("prompts") / "bug_to_user_story_v1.yml"

    try:
        print(f"🔄 Conectando ao LangSmith e buscando prompt: {prompt_identifier}...")
        client = Client()
        prompt = client.pull_prompt(
            prompt_identifier,
            dangerously_pull_public_prompt=True,
        )
        print("   ✓ Prompt baixado com sucesso do LangSmith Hub!")

        # Extrair mensagens do ChatPromptTemplate
        system_prompt = ""
        user_prompt = ""

        for message in prompt.messages:
            msg_class = message.__class__.__name__.lower()
            # Obter o template textual da mensagem
            template = getattr(message, "prompt", message)
            content = getattr(template, "template", getattr(message, "content", ""))

            if "system" in msg_class:
                system_prompt = content
            elif "human" in msg_class or "user" in msg_class:
                user_prompt = content

        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"],
            }
        }

        print(f"💾 Salvando prompt em: {output_path}...")
        if save_yaml(prompt_data, str(output_path)):
            print(f"   ✓ Arquivo {output_path} salvo com sucesso!")
            return True
        else:
            print(f"   ❌ Erro ao salvar {output_path}")
            return False

    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        return False


def main():
    """Função principal"""
    success = pull_prompts_from_langsmith()
    if success:
        print("\n✅ Pull de prompts concluído com sucesso!")
        return 0
    else:
        print("\n❌ Falha no pull de prompts.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
