import streamlit as st
from datetime import datetime, date
from agente import AgenteAssedio, Denuncia

def main():
    st.markdown("### Sistema Especialista - Guia de Bolso sobre Assédio Sexual")

    denunciante_e_vitima = st.radio(
        "Você é a vítima?", options=["Sim", "Não"], index=0
    ) == "Sim"

    if denunciante_e_vitima:
        nome_denunciante = st.text_input("Nome do denunciante", value="Vítima Desconhecida")
        sexo_denunciante = st.selectbox("Sexo do denunciante", options=["Feminino", "Masculino"])
    else:
        nome_denunciante = st.text_input("Nome da vítima")
        sexo_denunciante = st.selectbox("Sexo da vítima", options=["Feminino", "Masculino"])

    nome_denunciado = st.text_input("Nome do denunciado", value="Denunciado Desconhecido")
    sexo_denunciado = st.selectbox("Sexo do denunciado", options=["Feminino", "Masculino"])

    local_ocorrencia = st.selectbox("Local da ocorrência", options=[
        "Transporte Público", "Sala de aula", "Escritório", "Saguão", "Corredor A", "Corredor B", "Pátio",
        "Portão de entrada", "Portão de saída"
    ])

    data_ocorrencia = st.date_input("Data da ocorrência", value=date.today())
    if data_ocorrencia > date.today():
        st.warning("A data da ocorrência não pode ser no futuro.")

    periodo_ocorrencia = st.selectbox("Frequência da ocorrência", options=[
        "Nunca ocorreu", "Já ocorreu antes", "Ocorreu muitas vezes antes"
    ])

    periodo_data_ocorrencia = []
    if periodo_ocorrencia == "Já ocorreu antes" or periodo_ocorrencia == "Ocorreu muitas vezes antes":
        data_inicial_periodo_ocorrencia = st.date_input("Data de início da ocorrência anterior", value=date.today())
        data_final_periodo_ocorrencia = st.date_input("Data de fim da ocorrência anterior", value=date.today())
        if data_inicial_periodo_ocorrencia > data_final_periodo_ocorrencia:
            st.warning("A data final não pode ser menor que a data inicial.")
        if data_final_periodo_ocorrencia > date.today():
            st.warning("A data final não pode ser no futuro.")
        if data_inicial_periodo_ocorrencia > date.today():
            st.warning("A data inicial não pode ser no futuro.")
        periodo_data_ocorrencia = [data_inicial_periodo_ocorrencia, data_final_periodo_ocorrencia]


    hierarquia_maior = st.radio(
        "O denunciado ocupa cargo hierárquico superior ao da vítima?",
        options=["Sim", "Não"]
    ) == "Sim"

    # Ações realizadas
    acoes_disponiveis = [
        "Aproximação física insistente"
        "Beijo na bochecha", "Beijo na boca", "Beijo na testa", "Beijo no pescoço",
        "Cantadas",
        "Divulgação de conteúdo íntimo",
        "Encosto intencional em partes íntimas",
        "Envio de mensagens de teor sexual", "Envio de fotos com teor sexual",
        "Exposição de Fetiches",
        "Expressão de gírias de cunho sexual",
        "Falas com conotação sexual",
        "Humilhações sexistas",
        "Insinuações sobre desempenho sexual",
        "Linguagem corporal insinuante",
        "Oferecimento de vantagens em troca de favores sexuais",
        "Perseguição", "Perseguição virtual",
        "Questionamentos íntimos",
        "Zombarias públicas"
    ]
    acoes_realizadas = st.multiselect("Ações realizadas pelo denunciado", acoes_disponiveis)

    if acoes_realizadas:
        st.markdown("#### Consentimento para cada ação (marque se houve consentimento)")
    consentimento = {}
    for acao in acoes_realizadas:
        consentimento[acao] = st.checkbox(f"Houve consentimento para: {acao}", value=False)

    testemunhas_str = st.text_area("Testemunhas (separe os nomes por vírgula)")
    testemunhas = [nome.strip() for nome in testemunhas_str.split(",") if nome.strip()]

    nome_testemunha = ""
    if not denunciante_e_vitima:
        nome_testemunha = st.text_input("Seu nome (testemunha)")
        if nome_testemunha:
            testemunhas.append(nome_testemunha)

    provas = st.radio("Existem provas?", options=["Sim", "Não"]) == "Sim"

    if st.button("Registrar denúncia"):
        if not nome_denunciante or not nome_denunciado:
            st.error("Preencha os nomes do denunciado e da vítima.")
            return

        if not denunciante_e_vitima and not nome_testemunha:
            st.error("Informe seu nome como testemunha.")
            return

        if data_ocorrencia > date.today():
            st.error("A data da ocorrência não pode ser no futuro.")
            return

        denuncia = Denuncia(
            nome_denunciante=nome_denunciante,
            sexo_denunciante=sexo_denunciante.lower(),
            nome_denunciado=nome_denunciado,
            sexo_denunciado=sexo_denunciado.lower(),
            local_ocorrencia=local_ocorrencia.lower(),
            data_ocorrencia=datetime.combine(data_ocorrencia, datetime.min.time()),
            periodo_ocorrencia=periodo_ocorrencia.lower(),
            periodo_data_ocorrencia=periodo_data_ocorrencia,
            hierarquia_maior=hierarquia_maior,
            consentimento=consentimento,
            acoes_realizadas=acoes_realizadas,
            testemunhas=testemunhas,
            provas=provas
        )

        engine = AgenteAssedio()
        engine.reset()
        engine.declare(denuncia)
        engine.run()

        st.subheader("Classificações encontradas:")
        for resultado in engine.resultados:
            st.write(f"- {resultado}")

        st.subheader("Justificativas:")
        for explicacao in engine.explicacoes:
            st.write(f"- {explicacao}")

if __name__ == "__main__":
    main()
