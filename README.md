# Painel de Mídias — clientes

Projeto inicial em **Python + Streamlit** para organizar clientes de social media e gerar conteúdos.

## O que já vem pronto

- Cliente piloto: **Lúcia Bessa**
- 3 logos cadastradas
- 5 fotos cadastradas
- 1 referência visual cadastrada
- paleta: `#8a25c5`, `#f9f9f9`, `#4f0070`
- fontes preferidas registradas: DM Sans, Amazin Slab e Poppins
- canais: Instagram, Facebook, X, WhatsApp, Story e Carrossel Instagram
- escolha de 0/1/2/3 logos por post
- escolha opcional de foto
- gerador de texto
- gerador de arte-base PNG
- histórico local
- tela para criar novos clientes
- senha opcional para o painel

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá o painel local.

## IA online (opcional)

O painel funciona sem chave de IA, usando um modelo de texto local simples.
Para ativar geração de texto por IA, defina:

```bash
export OPENAI_API_KEY="sua-chave"
export OPENAI_TEXT_MODEL="modelo-disponivel-na-sua-conta"
```

No Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="sua-chave"
$env:OPENAI_TEXT_MODEL="modelo-disponivel-na-sua-conta"
```

O nome do modelo foi deixado configurável para não prender o sistema a um modelo específico.

## Senha do painel

Se quiser que o painel peça senha:

```bash
export PANEL_PASSWORD="sua-senha"
```

## Adicionar novos clientes

Use `＋ Novo cliente` no menu lateral. O cliente é salvo em `data/clientes/`.

Nesta primeira versão, o cadastro pelo painel cria o perfil básico. Logos e fotos podem ser adicionadas manualmente às pastas do projeto e registradas no JSON do cliente. Uma próxima etapa pode incluir upload e gerenciamento desses arquivos diretamente na interface.

## Observação importante sobre logos e fotos

Os arquivos originais da Lúcia são usados diretamente. A arte-base não recria logos ou o rosto dela com IA.

## Estrutura

```text
painel_midias_clientes/
├── app.py
├── requirements.txt
├── .env.example
├── assets/
│   └── lucia_bessa/
│       ├── logos/
│       ├── fotos/
│       └── referencias/
├── data/
│   ├── clientes/
│   └── historico/
└── utils/
    ├── arte.py
    ├── clientes.py
    └── conteudo.py
```
