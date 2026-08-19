
import os, io, json, re
from pathlib import Path
import streamlit as st
from utils.clientes import listar_clientes, carregar_cliente, salvar_cliente
from utils.conteudo import montar_prompt, gerar_com_openai, gerar_modelo_local, salvar_historico
from utils.arte import gerar_card

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Painel de Mídias", page_icon="✦", layout="wide")

# ---------- proteção opcional ----------
senha = os.getenv("PANEL_PASSWORD", "").strip()
if senha:
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if not st.session_state.autenticado:
        st.title("Painel de Mídias")
        tentativa = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if tentativa == senha:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
        st.stop()

st.markdown("""
<style>
.block-container {padding-top: 1.4rem;}
[data-testid="stSidebar"] {min-width: 280px;}
.cardbox {border:1px solid #eee; border-radius:16px; padding:16px;}
.small {font-size:.85rem; color:#666;}
</style>
""", unsafe_allow_html=True)

clientes = listar_clientes()
if not clientes:
    st.error("Nenhum cliente cadastrado.")
    st.stop()

with st.sidebar:
    st.title("Painel de Mídias")
    nomes = {c["nome"]: c["id"] for c in clientes}
    opcao = st.radio("Cliente", list(nomes.keys()) + ["＋ Novo cliente"])
    st.divider()
    pagina = st.radio("Área", ["Criar conteúdo", "Biblioteca", "Perfil do cliente", "Histórico"])

if opcao == "＋ Novo cliente":
    st.header("Adicionar novo cliente")
    st.caption("O sistema foi construído para crescer. Cada cliente terá identidade, biblioteca e regras próprias.")
    with st.form("novo_cliente"):
        nome = st.text_input("Nome do cliente")
        descricao = st.text_area("O que faz / área de atuação")
        tom = st.text_input("Tom de comunicação")
        cores = st.text_input("Cores, separadas por vírgula", "#8a25c5,#f9f9f9,#4f0070")
        redes = st.multiselect("Redes", ["Instagram","Facebook","X","WhatsApp","Story","Carrossel Instagram","LinkedIn","TikTok"])
        ok = st.form_submit_button("Criar cliente")
        if ok and nome.strip():
            cid = re.sub(r"[^a-z0-9_]+","_", nome.lower().strip().replace("ç","c").replace("ã","a").replace("á","a").replace("é","e"))
            data = {
                "id": cid, "nome": nome.strip(), "descricao": descricao.strip(), "tom": tom.strip(),
                "cores": [x.strip() for x in cores.split(",") if x.strip()],
                "fontes_preferidas": [], "redes": redes, "temas": [], "logos": [], "fotos": [],
                "referencias": [], "regras_visuais": []
            }
            salvar_cliente(data)
            st.success("Cliente criado. Recarregue a página para vê-lo no menu.")
    st.stop()

cliente = carregar_cliente(nomes[opcao])

if pagina == "Criar conteúdo":
    st.header(f"Criar conteúdo · {cliente['nome']}")
    c1,c2 = st.columns([2,1])
    with c1:
        assunto = st.text_area("Assunto do post", placeholder="Ex.: Violência psicológica também é violência.")
        rede = st.selectbox("Rede / canal", cliente.get("redes", ["Instagram"]))
        formato = st.selectbox("Formato", ["Post único","Carrossel","Story","Texto para WhatsApp","Texto para X"])
        objetivo = st.selectbox("Objetivo", ["Conscientizar","Informar","Engajar","Divulgar campanha","Comentar assunto atual"])
        observacoes = st.text_area("Observações", placeholder="Ex.: destacar uma frase, evitar muito texto, usar campanha X...")
    with c2:
        st.subheader("Elementos da arte")
        todas_logos = cliente.get("logos", [])
        nomes_logos = [x["nome"] for x in todas_logos]
        escolhidas = st.multiselect("Logos", nomes_logos, default=nomes_logos[:1])
        usar_foto = st.checkbox("Usar foto da Lúcia")
        foto_idx = None
        if usar_foto and cliente.get("fotos"):
            foto_idx = st.selectbox("Foto", list(range(len(cliente["fotos"]))), format_func=lambda i: f"Foto {i+1}")

    colA,colB,colC = st.columns(3)
    gerar_texto = colA.button("Gerar texto", use_container_width=True, type="primary")
    gerar_prompt = colB.button("Montar prompt", use_container_width=True)
    gerar_arte_btn = colC.button("Gerar arte-base", use_container_width=True)

    if assunto.strip():
        prompt = montar_prompt(cliente, assunto, rede, formato, objetivo, observacoes)
        if gerar_prompt:
            st.code(prompt, language=None)

        if gerar_texto:
            texto, erro = gerar_com_openai(prompt)
            if texto is None:
                st.info("IA online não configurada ou indisponível. Mostrando um modelo local editável.")
                if erro:
                    st.caption(f"Detalhe técnico: {erro}")
                texto = gerar_modelo_local(cliente, assunto, rede, formato, objetivo)
            st.session_state["texto_gerado"] = texto

        if "texto_gerado" in st.session_state:
            st.subheader("Conteúdo")
            editado = st.text_area("Edite antes de publicar", st.session_state["texto_gerado"], height=420)
            st.download_button("Baixar texto (.txt)", editado, file_name=f"{cliente['id']}_{rede.lower()}.txt")
            if st.button("Salvar no histórico"):
                salvar_historico(cliente["id"], {
                    "assunto": assunto, "rede": rede, "formato": formato, "objetivo": objetivo,
                    "conteudo": editado, "logos": escolhidas, "foto": foto_idx
                })
                st.success("Salvo no histórico.")

        if gerar_arte_btn:
            rel_logos = [x["arquivo"] for x in todas_logos if x["nome"] in escolhidas]
            foto = cliente["fotos"][foto_idx] if (foto_idx is not None and cliente.get("fotos")) else None
            card = gerar_card(cliente, assunto, "Informação também é proteção.", rel_logos, foto)
            buf = io.BytesIO()
            card.save(buf, format="PNG")
            st.image(card, caption="Arte-base automática")
            st.download_button("Baixar arte PNG", buf.getvalue(), file_name=f"{cliente['id']}_card.png", mime="image/png")
    else:
        st.info("Digite um assunto para começar.")

elif pagina == "Biblioteca":
    st.header(f"Biblioteca · {cliente['nome']}")
    st.subheader("Logos")
    cols = st.columns(3)
    for i, item in enumerate(cliente.get("logos", [])):
        p = ROOT / item["arquivo"]
        with cols[i % 3]:
            if p.exists():
                st.image(str(p), caption=item["nome"])
    st.subheader("Fotos")
    cols = st.columns(3)
    for i, rel in enumerate(cliente.get("fotos", [])):
        p = ROOT / rel
        with cols[i % 3]:
            if p.exists():
                st.image(str(p), caption=f"Foto {i+1}")
    st.subheader("Referências")
    for rel in cliente.get("referencias", []):
        p = ROOT / rel
        if p.exists():
            st.image(str(p), width=420)

elif pagina == "Perfil do cliente":
    st.header(f"Perfil · {cliente['nome']}")
    st.write(cliente.get("descricao",""))
    st.markdown(f"**Tom:** {cliente.get('tom','')}")
    st.markdown("**Cores:** " + " · ".join(cliente.get("cores", [])))
    st.markdown("**Fontes:** " + ", ".join(cliente.get("fontes_preferidas", [])))
    st.markdown("**Redes:** " + ", ".join(cliente.get("redes", [])))
    st.markdown("**Temas:**")
    for x in cliente.get("temas", []):
        st.write("•", x)
    st.markdown("**Regras visuais:**")
    for x in cliente.get("regras_visuais", []):
        st.write("•", x)

elif pagina == "Histórico":
    st.header(f"Histórico · {cliente['nome']}")
    arquivos = sorted((ROOT/"data"/"historico").glob(f"*_{cliente['id']}.json"), reverse=True)
    if not arquivos:
        st.info("Ainda não há conteúdos salvos.")
    for arq in arquivos:
        data = json.loads(arq.read_text(encoding="utf-8"))
        with st.expander(f"{data.get('criado_em','')} · {data.get('rede','')} · {data.get('assunto','')}"):
            st.write(data.get("conteudo",""))
