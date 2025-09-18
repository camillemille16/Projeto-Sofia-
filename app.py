import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

st.set_page_config(page_title="Gestão de Treinamentos", layout="centered")

st.title("Plataforma de Gestão de Treinamentos")
st.write("Bem-vindo! Aqui você pode se inscrever em cursos, carregar relatórios e acompanhar os resultados.")

st.sidebar.title("Menu")
pagina = st.sidebar.radio("Escolha a página:", ["Inscrição", "Upload de Relatórios", "Visualização de Desempenho", "Assistente Virtual"])

# --- Inscrição ---
if pagina == "Inscrição":
    st.subheader("Formulário de Inscrição")
    nome = st.text_input("Digite seu nome completo:")
    curso = st.selectbox("Selecione o curso:", ["Excel", "Python para Dados", "Gestão de Projetos", "Design Thinking"])
    email = st.text_input("Digite seu e-mail:")
    confirmar = st.button("Confirmar inscrição")

    if confirmar and nome and email:
        st.success(f"{nome}, sua inscrição no curso {curso} foi realizada com sucesso! Em breve você receberá um e-mail em {email}.")
    elif confirmar:
        st.warning("Por favor, preencha todos os campos antes de confirmar.")

# --- Upload ---
elif pagina == "Upload de Relatórios":
    st.subheader("Upload de Relatórios CSV")
    st.info("Carregue aqui os relatórios de desempenho dos cursos em formato CSV.")
    arquivo = st.file_uploader("Selecione um arquivo CSV", type=["csv"])

    if arquivo:
        df = pd.read_csv(arquivo)
        st.write("Pré-visualização dos dados:")
        st.dataframe(df)

# --- Dashboard ---
elif pagina == "Visualização de Desempenho":
    st.subheader("Visualização de Desempenho")
    st.write("Acompanhe abaixo as notas médias dos alunos em diferentes cursos:")

    dados = pd.DataFrame({
        "Cursos": ["Excel Avançado", "Python para Dados", "Gestão de Projetos", "Design Thinking"],
        "Média de Notas": [8.7, 9.1, 7.9, 8.3]
    })

    st.bar_chart(dados.set_index("Cursos"))
    st.success("Gráfico gerado com base em dados.")

# --- Assistente Virtual com Groq ---
elif pagina == "Assistente Virtual":
    st.subheader("🤖 Assistente Virtual - IA Groq")
    st.write("Converse com o assistente sobre cursos, relatórios ou desempenho dos alunos.")

    pergunta = st.text_area("Digite sua pergunta:")

    if st.button("Perguntar") and pergunta:
        # Configura o modelo Groq
        llm = ChatGroq(
            groq_api_key=st.secrets["GROQ_API_KEY"],
            model="llama3-8b-8192"
        )

        contexto = """
        Você é um assistente educacional. Responda de forma clara e objetiva.
        Você pode ajudar a explicar sobre cursos, desempenho de alunos e relatórios.
        """

        resposta = llm.invoke([
            SystemMessage(content=contexto),
            HumanMessage(content=pergunta)
        ])

        st.success(resposta.content)
