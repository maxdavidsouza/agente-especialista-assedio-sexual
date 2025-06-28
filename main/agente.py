from experta import *
from datetime import datetime

# BASE DE CONHECIMENTO
class Denuncia(Fact):
    """Assume um conjunto de informações para gerar uma denúncia"""
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

class ClassificacaoFeita(Fact):
    """Caso uma classificação de conduta ou crime já tenha sido identificada"""
    pass

# MOTOR DE INFERÊNCIA
class AgenteAssedio(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = []
        self.explicacoes = []

    # Aproximação física insistente
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent, hierarquia_maior=MATCH.hierarquia),
        TEST(lambda acoes, consent: "Aproximação física insistente" in acoes and not consent.get("Aproximação física insistente", True))
    )
    def aproximacao_fisica(self):
        if self.facts[1]['hierarquia_maior']:
            self.resultados.append("Assédio Sexual Vertical")
            self.explicacoes.append(
                "SE houver aproximação física insistente sem consentimento e existir relação de hierarquia, "
                "ENTÃO configura Assédio Sexual Vertical."
            )
        else:
            self.resultados.append("Assédio Sexual Horizontal")
            self.explicacoes.append(
                "SE houver aproximação física insistente sem consentimento e não houver relação de hierarquia, "
                "ENTÃO configura Assédio Sexual Horizontal."
            )

    # Beijos (bochecha, boca, testa, pescoço)
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent, hierarquia_maior=MATCH.hierarquia),
        TEST(lambda acoes, consent: any(
            b in acoes and not consent.get(b, True)
            for b in ["Beijo na bochecha", "Beijo na boca", "Beijo na testa", "Beijo no pescoço"]
        ))
    )
    def beijos(self):
        hierarquia = self.facts[1]['hierarquia_maior']
        if hierarquia:
            self.resultados.append("Assédio Sexual Vertical")
            self.explicacoes.append(
                "SE houver beijo sem consentimento e existir relação de hierarquia, "
                "ENTÃO configura Assédio Sexual Vertical."
            )
        else:
            self.resultados.append("Assédio Sexual Horizontal")
            self.explicacoes.append(
                "SE houver beijo sem consentimento e não houver relação de hierarquia, "
                "ENTÃO configura Assédio Sexual Horizontal."
            )

    # Cantadas
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent, hierarquia_maior=MATCH.hierarquia),
        TEST(lambda acoes, consent: "Cantadas" in acoes and not consent.get("Cantadas", True))
    )
    def cantadas(self):
        if self.facts[1]['hierarquia_maior']:
            self.resultados.append("Assédio Sexual Vertical")
            self.explicacoes.append(
                "SE houver cantadas sem consentimento em contexto hierárquico, "
                "ENTÃO configura Assédio Sexual Vertical."
            )
        else:
            self.resultados.append("Assédio Sexual Horizontal")
            self.explicacoes.append(
                "SE houver cantadas sem consentimento e não houver relação hierárquica, "
                "ENTÃO configura Assédio Sexual Horizontal."
            )

    # Divulgação de conteúdo íntimo
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Divulgação de conteúdo íntimo" in acoes)
    )
    def divulgacao_conteudo(self):
        self.resultados.append("Importunação Sexual")
        self.explicacoes.append(
            "SE houver divulgação de conteúdo íntimo, "
            "ENTÃO configura Importunação Sexual."
        )

    # Encosto intencional em partes íntimas
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent, hierarquia_maior=MATCH.hierarquia),
        TEST(lambda acoes, consent: "Encosto intencional em partes íntimas" in acoes and not consent.get("Encosto intencional em partes íntimas", True))
    )
    def encosto_intencional(self):
        if self.facts[1]['hierarquia_maior']:
            self.resultados.append("Assédio Sexual Vertical")
            self.explicacoes.append(
                "SE houver encosto intencional em partes íntimas sem consentimento e existir relação hierárquica, "
                "ENTÃO configura Assédio Sexual Vertical."
            )
        else:
            self.resultados.append("Assédio Sexual Horizontal")
            self.explicacoes.append(
                "SE houver encosto intencional em partes íntimas sem consentimento e não houver relação hierárquica, "
                "ENTÃO configura Assédio Sexual Horizontal."
            )

    # Envio de mensagens/fotos com teor sexual
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consent),
        TEST(lambda acoes, consent: ("Envio de mensagens de teor sexual" in acoes and not consent.get("Envio de mensagens de teor sexual", True))
                                    or ("Envio de fotos com teor sexual" in acoes and not consent.get("Envio de fotos com teor sexual", True)))
    )
    def envio_teor_sexual(self):
        self.resultados.append("Importunação Sexual")
        self.explicacoes.append(
            "SE houver envio de mensagens ou fotos com teor sexual sem consentimento, "
            "ENTÃO configura Importunação Sexual."
        )

    # Exposição de Fetiches
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Exposição de Fetiches" in acoes)
    )
    def exposicao_fetiches(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "SE houver exposição de fetiches, "
            "ENTÃO pode configurar Conduta Sexual, dependendo do contexto."
        )

    # Expressão de gírias de cunho sexual
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Expressão de gírias de cunho sexual" in acoes)
    )
    def girias_cunho_sexual(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "SE houver expressão de gírias de cunho sexual, "
            "ENTÃO pode configurar Conduta Sexual inadequada."
        )

    # Falas com conotação sexual
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Falas com conotação sexual" in acoes)
    )
    def falas_conotacao(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "SE houver falas com conotação sexual, "
            "ENTÃO pode configurar Conduta Sexual inadequada."
        )

    # Humilhações sexistas
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Humilhações sexistas" in acoes)
    )
    def humilhacoes_sexistas(self):
        self.resultados.append("Importunação Sexual")
        self.explicacoes.append(
            "SE houver humilhações sexistas, "
            "ENTÃO configura Importunação Sexual."
        )

    # Insinuações sobre desempenho sexual
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Insinuações sobre desempenho sexual" in acoes)
    )
    def insinuacoes_desempenho(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "SE houver insinuações sobre desempenho sexual, "
            "ENTÃO pode configurar Conduta Sexual inadequada."
        )

    # Linguagem corporal insinuante
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Linguagem corporal insinuante" in acoes)
    )
    def linguagem_corporal(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "SE houver linguagem corporal insinuante, "
            "ENTÃO pode configurar Conduta Sexual inadequada."
        )

    # Oferecimento de vantagens em troca de favores sexuais
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Oferecimento de vantagens em troca de favores sexuais" in acoes)
    )
    def vantagens_por_favores(self):
        self.resultados.append("Assédio Sexual Vertical")
        self.explicacoes.append(
            "SE houver oferecimento de vantagens em troca de favores sexuais, "
            "ENTÃO configura Assédio Sexual Vertical por abuso de hierarquia."
        )

    # Perseguição e Perseguição virtual
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Perseguição" in acoes or "Perseguição virtual" in acoes)
    )
    def perseguicoes(self):
        self.resultados.append("Importunação Sexual")
        self.explicacoes.append(
            "SE houver perseguição ou perseguição virtual, "
            "ENTÃO configura Importunação Sexual."
        )

    # Questionamentos íntimos
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Questionamentos íntimos" in acoes)
    )
    def questionamentos(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "SE houver questionamentos íntimos, "
            "ENTÃO pode configurar Conduta Sexual inadequada."
        )

    # Zombarias públicas
    @Rule(
        Denuncia(acoes_realizadas=MATCH.acoes),
        TEST(lambda acoes: "Zombarias públicas" in acoes)
    )
    def zombarias_publicas(self):
        self.resultados.append("Importunação Sexual")
        self.explicacoes.append(
            "SE houver zombarias públicas, "
            "ENTÃO configura Importunação Sexual."
        )