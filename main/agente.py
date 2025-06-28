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

### CLASSIFICAÇÕES DE CONDUTAS ###
# ASSÉDIO MORAL
# VIOLÊNCIA PSICOLÓGICA
# SEXISMO
# IMPORTUNAÇÃO SEXUAL
# ASSÉDIO SEXUAL
#

# MOTOR DE INFERÊNCIA
class AgenteAssedio(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = [] # Conjunto de classificações feitas
        self.explicacoes = [] # Conjunto de explicações sobre as classificações

    @Rule(Denuncia(hierarquia_maior=True,acoes_realizadas=MATCH.acoes,consentimento=MATCH.consent),
        TEST(lambda acoes, consent: any(
            (acao in acoes and not consent.get(acao, True))
            for acao in acoes
        ))
    )
    def assedio_sexual_vertical(self):
        self.resultados.append("Assédio Sexual Vertical")
        self.explicacoes.append(
            "Se há hierarquia entre a vítima e o denunciado, e o denunciado "
            "realizou ações sem consentimento, pode haver Assédio Sexual Horizontal."
        )
        self.declare(ClassificacaoFeita())

    @Rule(Denuncia(hierarquia_maior=False,acoes_realizadas=MATCH.acoes,consentimento=MATCH.consent),
        TEST(lambda acoes, consent: any(
            (acao in acoes and not consent.get(acao, True))
            for acao in acoes
        ))
    )
    def assedio_sexual_horizontal(self):
        self.resultados.append("Assédio Sexual Horizontal")
        self.explicacoes.append(
            "Se não há hierarquia entre a vítima e o denunciado, e o denunciado "
            "realizou ações sem consentimento, pode haver Assédio Sexual Horizontal."
        )
        self.declare(ClassificacaoFeita())

    @Rule(Denuncia(acoes_realizadas=MATCH.acoes,consentimento=MATCH.consent),
        TEST(lambda acoes, consent: any(
            acao in acoes and not consent.get(acao, True)
            for acao in ["insinuar algo", "conversas sexuais", "comentários sexuais"]
        ))
    )
    def conduta_sexual(self):
        self.resultados.append("Conduta Sexual")
        self.explicacoes.append(
            "Se há ações verbais de cunho sexual sem consentimento, então pode haver Conduta Sexual."
        )
        self.declare(ClassificacaoFeita())

    @Rule(Denuncia(acoes_realizadas=MATCH.acoes,consentimento=MATCH.consent),
        TEST(lambda acoes, consent: any(
            acao in acoes and not consent.get(acao, True)
            for acao in ["beijo na boca", "abraço por trás", "abraço pela frente", "agarrar partes íntimas", "segurar a mão", "segurar o braço", "mexer no cabelo"]
        ))
    )
    def importunacao_sexual(self):
        self.resultados.append("Importunação Sexual")
        self.explicacoes.append(
            "Se há contato físico sem consentimento, então pode haver Importunação Sexual."
        )
        self.declare(ClassificacaoFeita())

    @Rule(Denuncia(acoes_realizadas=MATCH.acoes,consentimento=MATCH.consent),
        TEST(lambda acoes, consent: any(
            acao in acoes and not consent.get(acao, True)
            for acao in ["falar mal para outras pessoas", "xingamentos"]
        ))
    )
    def difamacao(self):
        self.resultados.append("Difamação")
        self.explicacoes.append(
            "Se há ações verbais públicas ofensivas sem consentimento, então pode haver Difamação."
        )
        self.declare(ClassificacaoFeita())

    @Rule(Denuncia(hierarquia_maior=True, consentimento=MATCH.consent),
        TEST(lambda consent: any(not permitido for permitido in consent.values())))
    def abuso_de_funcao(self):
        self.resultados.append("Abuso de Função")
        self.explicacoes.append(
            "Se há uma hierarquia entre a vítima e o denunciado, então pode haver Abuso de Função."
        )
        self.declare(ClassificacaoFeita())

    @Rule(Denuncia(testemunhas=MATCH.testemunhas, provas=False))
    def alerta_sem_testemunha_ou_prova(self, testemunhas):
        if len(testemunhas) == 0:
            self.resultados.append("Alerta: denúncia sem testemunhas e sem provas.")
            self.explicacoes.append(
                "Se não há testemunhas e provas, a denúncia pode não ser reforçada."
            )

    @Rule(Denuncia(testemunhas=MATCH.testemunhas),
        TEST(lambda testemunhas: len(testemunhas) > 0)
    )
    def reforca_com_testemunhas(self):
        self.explicacoes.append(
            "Se há testemunhas, a denúncia pode ser reforçada."
        )

    @Rule(Denuncia(testemunhas=MATCH.testemunhas,
                   acoes_realizadas=MATCH.acoes,
                   nome_denunciante=MATCH.nome_vitima,
                   nome_denunciado=MATCH.nome_denunciado,
                   data_ocorrencia=MATCH.data))
    def explicacao_testemunha_lista(self, testemunhas, acoes, nome_vitima, nome_denunciado, data):
        if testemunhas:  # só se tiver testemunhas
            data_str = data.strftime("%d/%m/%Y")
            nomes_testemunhas = ", ".join(testemunhas)
            acoes_str = ", ".join(acoes)
            classificacoes = [r for r in self.resultados if r not in ["Alerta: denúncia sem testemunhas e sem provas.",
                                                                      "Nenhuma classificação detectada"]]
            classificacoes_str = ", ".join(classificacoes) if classificacoes else "nenhuma classificação específica"

            explicacao = (
                f"As testemunhas {nomes_testemunhas} viram {nome_denunciado} fazendo {acoes_str} com {nome_vitima}  "
                f"no dia {data_str}, portanto, pode ser que {nome_denunciado} tenha cometido {classificacoes_str}.")
            self.explicacoes.append(explicacao)

    @Rule(Denuncia(), NOT(ClassificacaoFeita()), salience=-10)
    def sem_classificacao(self):
        self.resultados.append("Nenhuma classificação detectada")
        self.explicacoes.append(
            "Nenhuma das categorias previstas foi identificada com os dados fornecidos."
        )