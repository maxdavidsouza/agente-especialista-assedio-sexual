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

ACOES_ASSEDIO = [
    "Aproximação física insistente",
    "Beijo na bochecha", "Beijo na boca", "Beijo na testa", "Beijo no pescoço",
    "Cantadas", "Encosto intencional em partes íntimas",
    "Oferecimento de vantagens em troca de favores sexuais",
    "Ameaças para favores sexuais"
]

ACOES_IMPORTUNACAO = [
    "Divulgação de conteúdo íntimo", "Envio de mensagens de teor sexual",
    "Envio de fotos com teor sexual", "Perseguição", "Perseguição virtual",
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

LOCAIS_SENSIVEIS = [
    "Transporte Público", "Sala de aula", "Escritório", "Saguão",
    "Corredor A", "Corredor B", "Pátio", "Portão de entrada", "Portão de saída"
]

class AgenteAssedio(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = set()
        self.explicacoes = []
        self.orientacoes = []
        self.contexto = {}

    # METODO MAIS DETALHADO DE CLASSIFICACAO DE ASSEDIO SEXUAL
    def classificar(self, tipo, acao, extra=None):
        if tipo == "Assédio Sexual":
            subtipo = "Vertical" if extra else "Horizontal"
            tipo = f"{tipo} {subtipo}"
            self.resultados.add(tipo)
            self.explicacoes.append(
                f"SE houver {acao} sem consentimento e {'com' if extra else 'sem'} hierarquia, "
                f"ENTÃO configura {tipo}."
            )
        else:
            self.resultados.add(tipo)
            self.explicacoes.append(f"SE houver {acao}, ENTÃO configura {tipo}.")

    # METODO UM POUCO MAIS GENERICO PARA ANALISE DAS ACOES FEITAS PELO DENUNCIANTE
    @Rule(Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent,
                   hierarquia_maior=MATCH.hierarquia, provas=MATCH.provas,
                   testemunhas=MATCH.testemunhas, periodo_ocorrencia=MATCH.periodo,
                   local_ocorrencia=MATCH.local, periodo_data_ocorrencia=MATCH.periodos,
                   data_ocorrencia=MATCH.data_atual,
                   nome_denunciante=MATCH.vitima, nome_denunciado=MATCH.acusado))
    def analisar_acoes(self, acoes, consent, hierarquia, provas, testemunhas, periodo, local, periodos, data_atual, vitima, acusado):
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
                    self.classificar("Assédio Sexual", acao, hierarquia or acao in ["Oferecimento de vantagens em troca de favores sexuais", "Ameaças para favores sexuais"])
            elif acao in ACOES_IMPORTUNACAO:
                if not consent.get(acao, True) or acao in ["Divulgação de conteúdo íntimo", "Perseguição", "Zombarias públicas", "Humilhações sexistas"]:
                    self.classificar("Importunação Sexual", acao)
            elif acao in ACOES_CONDUTA:
                self.classificar("Conduta Sexual", acao)

    # METODOS DE FORMATACAO SIMPLES PARA TESTEMUNHAS E PERIODOS PARA EXPLICABILIDADE
    def formatar_testemunhas(self, lista):
        if not lista:
            return ""
        if len(lista) == 1:
            return lista[0]
        if len(lista) == 2:
            return f"{lista[0]} e {lista[1]}"
        return f"{', '.join(lista[:-1])} e {lista[-1]}"

    def formatar_periodos(self, lista):
        periodos = []
        for i in range(0, len(lista), 2):
            try:
                inicio = lista[i].strftime("%d/%m/%Y")
                fim = lista[i+1].strftime("%d/%m/%Y")
                periodos.append(f"entre {inicio} e {fim}")
            except:
                continue
        return periodos

    # METODO RESPONSAVEL POR GERAR AS ORIENTAÇÕES PARA O DENUNCIANTE
    def orientar(self):
        provas = self.contexto.get("provas")
        testemunhas = self.contexto.get("testemunhas")
        periodo = self.contexto.get("periodo")
        local = self.contexto.get("local")
        vitima = self.contexto.get("vitima")
        acusado = self.contexto.get("acusado")
        periodos = self.contexto.get("periodo_data")
        data_ocorrencia = self.contexto.get("data_ocorrencia")

        descricao_tipos = []
        leis_citadas = []

        for tipo in self.resultados:
            info = LEIS_REFERENCIA.get(tipo, {})
            if info:
                descricao_tipos.append(f"{tipo}: '{info['descricao']}'")
                leis_citadas.append(f"{tipo} — {info['lei']}")

        recomendacao = f"{vitima}, você relatou uma situação envolvendo {acusado}, que se enquadra nas seguintes classificações: \n- " + "\n- ".join(descricao_tipos) + ".\n\n"

        recomendacao += f"A última ocorrência relatada foi em {data_ocorrencia.strftime('%d/%m/%Y')}. "

        if periodos:
            lista_formatada = self.formatar_periodos(periodos)
            if lista_formatada:
                recomendacao += "Esses comportamentos já ocorreram antes " + ", ".join(lista_formatada) + ". "

        if provas:
            recomendacao += "Você mencionou possuir provas, o que pode fortalecer sua denúncia e facilitar a responsabilização do acusado. "
        else:
            recomendacao += "Mesmo sem provas materiais, seu relato é válido e pode ser suficiente para iniciar uma apuração. "

        if testemunhas:
            nomes = self.formatar_testemunhas(testemunhas)
            recomendacao += f"As testemunhas que podem corroborar sua versão são: {nomes}. Isso pode aumentar a credibilidade do seu relato. "
        else:
            recomendacao += "Não foram indicadas testemunhas, mas forneça todos os detalhes que puder. "

        if periodo in ["Já ocorreu antes", "Ocorreu muitas vezes antes"]:
            recomendacao += "O fato de a conduta ter ocorrido repetidamente indica padrão de comportamento e deve ser destacado. "
        elif periodo == "Nunca ocorreu":
            recomendacao += "Mesmo sendo a primeira ocorrência, o ato relatado é grave e merece atenção. "

        if local in LOCAIS_SENSIVEIS:
            recomendacao += f"O local do ocorrido ({local}) é um espaço sensível e institucional, o que torna o episódio ainda mais preocupante. "

        assedio_detectado = any("Assédio Sexual" in tipo for tipo in self.resultados)
        reincidente = (
                    periodo in ["Já ocorreu antes", "Ocorreu muitas vezes antes"] or (periodos and len(periodos) > 0))

        if assedio_detectado:
            recomendacao += (
                "Dado que o caso envolve assédio sexual, recomendamos fortemente que você registre um boletim de ocorrência, "
                "além de comunicar o fato aos canais formais da instituição, como a ouvidoria. Casos de assédio são graves e merecem apuração imediata. "
            )
        elif reincidente:
            recomendacao += (
                "Como o comportamento relatado se repetiu em outras ocasiões, é aconselhável registrar um boletim de ocorrência, "
                "além de procurar a ouvidoria ou os canais internos da instituição. A reincidência torna o caso ainda mais sério e merece atenção das autoridades. "
            )
        else:
            recomendacao += (
                "Recomendamos que você procure os canais formais da instituição, como a ouvidoria, para relatar a situação. "
                "Mesmo ocorrendo pela primeira vez, seu relato é importante para prevenir futuras ocorrências. "
            )

        recomendacao += "Você tem direito a um ambiente seguro e respeitoso."

        self.orientacoes.append(
            "\n".join(leis_citadas) + "\n\n" + recomendacao
        )
