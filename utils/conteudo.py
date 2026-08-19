
import os, json
from datetime import datetime
from pathlib import Path

def montar_prompt(cliente, assunto, rede, formato, objetivo, observacoes=""):
    return f"""
Você é um assistente de social media.

CLIENTE: {cliente['nome']}
PERFIL: {cliente.get('descricao','')}
TOM: {cliente.get('tom','')}
TEMAS: {', '.join(cliente.get('temas', []))}
REDE: {rede}
FORMATO: {formato}
OBJETIVO: {objetivo}
ASSUNTO: {assunto}

REGRAS:
- Escreva em português do Brasil.
- Mantenha tom forte na defesa da mulher, claro e responsável.
- Evite sensacionalismo.
- Não invente leis, estatísticas, falas, datas ou decisões.
- Quando o assunto depender de informação factual atual, sinalize [VERIFICAR FONTE] se a informação não tiver sido fornecida.
- Entregue:
  1) TEXTO DA ARTE
  2) LEGENDA
  3) HASHTAGS
  4) CTA
  5) SUGESTÃO VISUAL
- Para X, seja mais conciso.
- Para WhatsApp, escreva de forma natural e compartilhável.
- Para Story, mantenha texto curto.
- Para carrossel, organize por páginas.
OBSERVAÇÕES: {observacoes}
""".strip()

def gerar_com_openai(prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "OPENAI_API_KEY não configurada."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_TEXT_MODEL", "gpt-5")
        resp = client.responses.create(model=model, input=prompt)
        texto = getattr(resp, "output_text", None)
        if not texto:
            texto = str(resp)
        return texto, None
    except Exception as e:
        return None, str(e)

def gerar_modelo_local(cliente, assunto, rede, formato, objetivo):
    titulo = assunto.strip().rstrip(".")
    if rede == "X":
        legenda = f"{titulo}. Informação, proteção e respeito aos direitos das mulheres precisam estar no centro do debate."
    elif rede == "WhatsApp":
        legenda = f"{titulo}\n\nInformação também é proteção. Compartilhe este conteúdo para que mais mulheres conheçam seus direitos."
    else:
        legenda = (
            f"{titulo}.\n\n"
            "Defender as mulheres também passa por informar, acolher e fortalecer o acesso a direitos. "
            "Nenhuma forma de violência deve ser normalizada.\n\n"
            "Compartilhe esta mensagem."
        )
    return f"""TEXTO DA ARTE
{titulo}

LEGENDA
{legenda}

HASHTAGS
#DireitosDasMulheres #EnfrentamentoÀViolência #Mulheres #InformaçãoÉProteção

CTA
Compartilhe esta mensagem.

SUGESTÃO VISUAL
Usar a identidade roxa da Lúcia Bessa, composição limpa, mensagem central em destaque e logos selecionadas no rodapé.
"""

def salvar_historico(cliente_id, dados):
    pasta = Path(__file__).resolve().parents[1] / "data" / "historico"
    pasta.mkdir(parents=True, exist_ok=True)
    dados = dict(dados)
    dados["criado_em"] = datetime.now().isoformat(timespec="seconds")
    nome = datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{cliente_id}.json"
    (pasta / nome).write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
