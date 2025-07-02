from experta import *
from datetime import datetime


class Denuncia(Fact):
    nome_denunciante = Field(str, mandatory=True)
    sexo_denunciante = Field(str, mandatory=True)
    nome_denunciado = Field(str, mandatory=True)
    sexo_denunciado = Field(str, mandatory=True)
    local_ocorrencia = Field(str, mandatory=True)
    data_ocorrencia = Field(datetime, mandatory=True)
    periodo_ocorrencia = Field(str, mandatory=False)
    periodo_data_ocorrencia = Field(list, mandatory=False)
    hierarquia_maior = Field(bool, mandatory=True)
    consentimento = Field(dict, mandatory=True)
    acoes_realizadas = Field(list, mandatory=True)
    testemunhas = Field(list, mandatory=False)
    provas = Field(bool, mandatory=True)


class Classificacao(Fact):
    """Trata-se de uma classificacao declarada pelo agente, baseado nas r. de inf."""
    tipo = Field(str)
    subtipo = Field(str)
    acao = Field(str)
    motivo = Field(str)


class Orientacao(Fact):
    """Trata-se de uma orientação declarada pelo agente, baseada no guia"""
    mensagem = Field(str)


class Justificativa(Fact):
    """Fato para armazenar justificativas baseadas no guia de referência."""
    mensagem = Field(str)


class Conclusao(Fact):
    """Sinaliza a conclusão obtida pelo agente (serve mais para gerar
    a orientação final sem a necessidade de chamar o engine.orientar()"""
    pass


ACOES_ASSEDIO = [
    "Aproximação física insistente",
    "Beijo na bochecha", "Beijo na boca", "Beijo na testa", "Beijo no pescoço",
    "Encosto intencional em partes íntimas",
    "Oferecimento de vantagens em troca de favores sexuais",
    "Ameaças para favores sexuais"
]

ACOES_IMPORTUNACAO = [
    "Divulgação de conteúdo íntimo", "Envio de mensagens de teor sexual",
    "Cantadas", "Envio de fotos com teor sexual", "Perseguição", "Perseguição virtual",
    "Humilhações sexistas", "Zombarias públicas"
]

ACOES_CONDUTA = [
    "Exposição de Fetiches", "Expressão de gírias de cunho sexual",
    "Falas com conotação sexual", "Insinuações sobre desempenho sexual",
    "Linguagem corporal insinuante", "Questionamentos íntimos"
]

LEIS_REFERENCIA = {
    "Assédio Sexual Vertical": {
        "lei": "Art. 216-A do Código Penal",
        "descricao": "Assediar alguém com hierarquia superior, com o objetivo de obter vantagem ou favorecimento sexual."
    },
    "Assédio Sexual Horizontal": {
        "lei": "Art. 216-A do Código Penal",
        "descricao": "Assédio praticado por colega ou pessoa do mesmo nível hierárquico, ainda que não haja relação de poder formal."
    },
    "Importunação Sexual": {
        "lei": "Art. 215-A do Código Penal",
        "descricao": "Praticar ato libidinoso sem consentimento para satisfazer desejo próprio ou de terceiros."
    },
    "Conduta Sexual": {
        "lei": "Pode configurar infração ética ou administrativa",
        "descricao": "Comportamentos inadequados de cunho sexual que não chegam a configurar crime, mas violam o respeito no ambiente."
    }
}

LOCAIS = [
    "Transporte Público", "Sala de aula", "Escritório", "Saguão",
    "Corredor A", "Corredor B", "Pátio", "Portão de entrada", "Portão de saída"
]

GUIA_REFERENCIA = {
    "Assédio Sexual Vertical": {
        "pagina": ["Página 11", "Página 23", "Página 24"],
        "trecho": [
            f"Ocorre quando uma pessoa se vale da sua condição de superioridade hierárquica ou de ascendência "
            f"inerentes ao exercício de cargo ou função para constranger alguém com objetivo de obter vantagem ou "
            f"favorecimento sexual.Essa forma clássica de assédio é caracterizada como crime"]
    },
    "Assédio Sexual Horizontal": {
        "pagina": ["Página 11", "Página 23", "Página 25"],
        "trecho": [
            f"do Guia de Bolso sobre Assédio Sexual da UFAPE..",
            f"A pessoa que assedia trabalha com a assediada, sem hierarquia. Um exemplo é o constrangimento entre colegas de trabalho"]
    },
    "Importunação Sexual": {
        "pagina": ["Página 24", "Página 25"],
        "trecho": [
            """DESCRITA NO ART. 216-A DO CÓDIGO
                PENAL, BEM COMO NO ART. 215-A,
                IMPORTUNAÇÃO SEXUAL, SENADO
                FEDERAL, 2017, P. 1.""",
            """NÃO É “CRIME DE ASSÉDIO” PREVISTO NO CÓDIGO PENAL BRASILEIRO, 
                 MAS PODE SER ENTENDIDO COMO O CRIME DE IMPORTUNAÇÃO SEXUAL 
                 PREVISTO NO MESMO CÓDIGO PENAL, EM SEU ART. 215-A. PODE SER PUNIDO 
                 ADMINISTRATIVAMENTE, CIVILMENTE E PENALMENTE (1 A 5 ANOS DE PRISÃO)."""
        ]
    },
    "Conduta Sexual": {
        "pagina": ["Página 12", "Página 13", "Página 15", "Página 19", "Página 20", "Página 21"],
        "trecho": [
            """Passou a ser o gênero que engloba tanto as situações mais gravosas, denominadas de “Assédio Sexual”,
                como as demais situações, denominadas de “outras condutas de natureza sexual”.""",
            """INSINUAÇÕES Incluem mensagens escritas, gestos, cantadas, chantagens ou ameaças.
                CONTATOS FÍSICOS Forçados como condição para dar ou manter o emprego.
                PREJUDICAR O rendimento profissional da pessoa por meio de comentários ou investidas sexuais.
                HUMILHAR, INSULTAR OU INTIMIDAR A vítima de maneira sexual.
                INFLUIR Nas promoções ou na carreira da pessoa.""",
            """DÚVIDAS FREQUENTES SOBRE ASSÉDIO SEXUAL
                Precisa ser literal?
                Não. A abordagem pode ser sutil ou explícita.
                
                Precisa ter contato físico?
                Não. Basta haver perseguição indesejada ou investida não consentida.
                
                O que caracteriza?
                O não consentimento da pessoa assediada.
                Tudo que é conduta sexual desagradável, ofensivo e impertinente pela vítima.""",
            """OUTRAS CONDUTAS DE CONOTAÇÃO SEXUAL
                Narração de piadas ou uso de expressões de conteúdo sexual.
                Contato físico não desejado.
                Convites impertinentes.
                Criação de um ambiente pornográfico.
                Promessas de tratamento diferenciado.
                Ameaças veladas ou explícitas, de represálias, como a de perder o emprego."""
        ]

    }
}


class AgenteAssedio(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.justificativas = []
        self.resultados = set()
        self.explicacoes = []
        self.orientacoes = []
        self.contexto = {}
        self.fatos_gerados = []

    # METODO UM POUCO MAIS GENERICO PARA ANALISE DAS ACOES FEITAS PELO DENUNCIANTE
    @Rule(Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent,
                   hierarquia_maior=MATCH.hierarquia, provas=MATCH.provas,
                   testemunhas=MATCH.testemunhas, periodo_ocorrencia=MATCH.periodo,
                   local_ocorrencia=MATCH.local, periodo_data_ocorrencia=MATCH.periodos,
                   data_ocorrencia=MATCH.data_atual,
                   nome_denunciante=MATCH.vitima, nome_denunciado=MATCH.acusado))
    def analisar_acoes(self, acoes, consent, hierarquia, provas, testemunhas, periodo, local, periodos, data_atual,
                       vitima, acusado):
        # DEFININDO CONTEXTO PARA FUTURA EXPLICABILIDADE
        self.contexto = {
            "provas": provas,
            "testemunhas": testemunhas,
            "periodo": periodo,
            "local": local,
            "periodo_data": periodos,
            "data_ocorrencia": data_atual,
            "vitima": vitima,
            "acusado": acusado
        }

        for acao in acoes:
            if acao in ACOES_ASSEDIO:
                if not consent.get(acao, True):
                    if hierarquia:
                        self.declare(
                            Classificacao(tipo="Assédio Sexual", subtipo="Vertical", acao=acao,
                                          motivo="sem consentimento"))
                    else:
                        self.declare(
                            Classificacao(tipo="Assédio Sexual", subtipo="Horizontal", acao=acao,
                                          motivo="sem consentimento"))
                else:
                    self.declare(
                        Classificacao(tipo="Conduta Sexual", subtipo="", acao=acao, motivo="com consentimento"))

            elif acao in ACOES_IMPORTUNACAO:
                if not consent.get(acao, True) or acao in [
                    "Divulgação de conteúdo íntimo", "Perseguição",
                    "Zombarias públicas", "Humilhações sexistas"
                ]:
                    self.declare(Classificacao(tipo="Importunação Sexual", subtipo="", acao=acao,
                                               motivo="sem consentimento ou violência moral"))
                else:
                    self.declare(
                        Classificacao(tipo="Conduta Sexual", subtipo="", acao=acao, motivo="com consentimento"))

            elif acao in ACOES_CONDUTA:
                self.declare(Classificacao(tipo="Conduta Sexual", subtipo="", acao=acao, motivo="conduta inadequada"))

        self.declare(Conclusao())

    # METODO MAIS DETALHADO DE CLASSIFICACAO DE ASSEDIO SEXUAL
    @Rule(Classificacao(tipo=MATCH.tipo, subtipo=MATCH.subtipo, acao=MATCH.acao, motivo=MATCH.motivo))
    def explicar(self, tipo, subtipo, acao, motivo):
        chave = f"{tipo} ({subtipo})" if subtipo else tipo
        self.resultados.add(chave)

        if subtipo == "Horizontal":
            self.explicacoes.append(
                f"SE houve {acao} por colega ou desconhecido {motivo}, ENTÃO pode haver {chave}."
            )
        elif subtipo == "Vertical":
            self.explicacoes.append(
                f"SE houve {acao} por superior hierárquico {motivo}, ENTÃO pode haver {chave}."
            )
        else:
            self.explicacoes.append(
                f"SE houve {acao} {motivo}, ENTÃO pode haver {tipo}."
            )

        self.fatos_gerados.append(Classificacao(tipo=tipo, subtipo=subtipo, acao=acao, motivo=motivo))

    @Rule(Denuncia(provas=True))
    def orientar_com_provas(self):
        self.declare(Orientacao(
            mensagem="Como há provas do ocorrido, isso fortalece o processo de apuração e responsabilização. Guarde e compartilhe essas evidências com os canais oficiais."
        ))

    @Rule(Denuncia(provas=False))
    def orientar_sem_provas(self):
        self.declare(Orientacao(
            mensagem="Mesmo sem provas materiais, seu relato é importante."
        ))

    @Rule(Denuncia(periodo_ocorrencia="Nunca ocorreu"))
    def orientar_nunca_ocorreu(self):
        self.declare(Orientacao(
            mensagem="Você sinalizou que a situação nunca ocorreu. Caso venha a ocorrer, procure registrar os fatos detalhadamente."
        ))

    @Rule(Denuncia(periodo_ocorrencia="Já ocorreu antes"))
    def orientar_ocorreu_uma_vez(self):
        self.declare(Orientacao(
            mensagem="Como a situação já ocorreu anteriormente, é importante avaliar se há padrão de comportamento. Registre os detalhes e busque orientação especializada."
        ))

    @Rule(Denuncia(periodo_ocorrencia="Ocorreu muitas vezes antes"))
    def orientar_ocorreu_muitas_vezes(self):
        self.declare(Orientacao(
            mensagem="A recorrência do comportamento é um agravante. Reúna informações e considere formalizar a denúncia imediatamente."
        ))

    @Rule(Denuncia(periodo_ocorrencia=MATCH.periodo,
                   periodo_data_ocorrencia=MATCH.periodos),
          TEST(lambda periodo, periodos: periodo in ["Já ocorreu antes", "Ocorreu muitas vezes antes"] and isinstance(
              periodos, list)))
    def orientar_com_periodos(self, periodo, periodos):
        if periodos:
            periodos_formatados = [
                f"{inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}"
                for inicio, fim in periodos
            ]
            mensagem = (
                    f"As ações ocorreram em {len(periodos)} período(s): " +
                    "; ".join(periodos_formatados) +
                    ". Isso ajuda a demonstrar a persistência e gravidade do comportamento."
            )
            self.declare(Orientacao(mensagem=mensagem))

    @Rule(Denuncia(testemunhas=MATCH.testemunhas),
          TEST(lambda testemunhas: testemunhas is not None and len(testemunhas) > 0))
    def orientar_com_testemunhas(self, testemunhas):
        nomes = ", ".join(testemunhas)
        self.declare(Orientacao(
            mensagem=f"Foram identificadas testemunhas do ocorrido: {nomes}. Elas podem contribuir no processo de apuração dos fatos."
        ))

    # Orientação para casos de Assédio Sexual
    @Rule(OR(
        Classificacao(tipo="Assédio Sexual", subtipo="Vertical"),
        Classificacao(tipo="Assédio Sexual", subtipo="Horizontal")
    ))
    def orientar_boletim_ocorrencia(self):
        self.declare(Orientacao(
            mensagem="Recomendamos que você registre um boletim de ocorrência."))

    # Orientação para casos de Importunação Sexual
    @Rule(Classificacao(tipo="Importunação Sexual"))
    def orientar_importunacao(self):
        self.declare(
            Orientacao(mensagem="Recomendamos comunicar o ocorrido à ouvidoria da UFAPE."))

    # Orientação para casos de Conduta Sexual
    @Rule(Classificacao(tipo="Conduta Sexual", acao=MATCH.acao))
    def orientar_conduta(self, acao):
        self.declare(Orientacao(
            mensagem=f"Sugerimos que relate a situação de '{acao}' à diretoria da UFAPE, pois ainda que não seja crime, é inadequado para o ambiente acadêmico."))

    # Registro da Orientação no conjunto de orientações
    @Rule(Orientacao(mensagem=MATCH.msg))
    def registrar_orientacao(self, msg):
        self.orientacoes.append(msg)

    @Rule(Classificacao(tipo=MATCH.tipo, subtipo=MATCH.subtipo))
    def referenciar_guia(self, tipo, subtipo):
        if subtipo:
            chave = f"{tipo} {subtipo}"
        else:
            chave = tipo

        guia_info = GUIA_REFERENCIA.get(chave) or GUIA_REFERENCIA.get(tipo)
        if guia_info:
            paginas = ", ".join(str(p) for p in guia_info['pagina'])

            trechos = guia_info['trecho']
            if isinstance(trechos, str):
                trechos = [trechos]

            mensagem = f"Considerando o ato de {tipo}, de acordo com as páginas {paginas} do Guia de Bolso da UFAPE:\n\n"
            mensagem += "\n\n".join(trecho.strip() for trecho in trechos)

            # Verifica se já existe justificativa com essa mensagem para não duplicar
            if not any(isinstance(f, Justificativa) and f['mensagem'] == mensagem for f in self.facts.values()):
                self.declare(Justificativa(mensagem=mensagem))

    @Rule(Justificativa(mensagem=MATCH.msg))
    def registrar_justificativa(self, msg):
        if msg not in self.justificativas:
            self.justificativas.append(msg)
