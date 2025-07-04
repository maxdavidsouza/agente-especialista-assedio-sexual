from experta import *
from datetime import datetime
from base_de_conhecimento import *

class Denuncia(Fact):
    """Trata-se de um fato declarado pelo usuário, baseado na estrutura
     de uma denúncia feita à instituição deferida pelo guia de bolso"""
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

class AgenteAssedio(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.justificativas = []
        self.resultados = set()
        self.explicacoes = []
        self.orientacoes = []
        self.fatos_gerados = []

    #################### PARTE DE CLASSIFICAÇÃO DE AÇÕES ####################
    @Rule(Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consentimento, hierarquia_maior=True))
    def classificar_assedio_sexual_vertical(self, acoes, consentimento):
        for acao in acoes:
            if acao in ACOES_ASSEDIO:
                if not consentimento.get(acao, True):
                    motivo_de_ser_assedio = f"sem consentimento"
                    self.declare(Classificacao(tipo="Assédio Sexual", subtipo="Vertical",
                                               acao=acao, motivo=motivo_de_ser_assedio))
                    self.resultados.add(f"Assédio Sexual (Vertical)")

    @Rule(Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consentimento, hierarquia_maior=False))
    def classificar_assedio_sexual_horizontal(self, acoes, consentimento):
        for acao in acoes:
            if acao in ACOES_ASSEDIO:
                if not consentimento.get(acao, True):
                    motivo_de_ser_assedio = f"sem consentimento"
                    self.declare(Classificacao(tipo="Assédio Sexual", subtipo="Horizontal",
                                               acao=acao, motivo=motivo_de_ser_assedio))
                    self.resultados.add(f"Assédio Sexual (Horizontal)")

    @Rule(Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consentimento))
    def classificar_importunacao_sexual(self, acoes, consentimento):
        for acao in acoes:
            if acao in ACOES_IMPORTUNACAO:
                if not consentimento.get(acao, True):
                    motivo_de_ser_assedio = f"sem consentimento"
                    self.declare(Classificacao(tipo="Importunação Sexual", subtipo="",
                                               acao=acao, motivo=motivo_de_ser_assedio))
                    self.resultados.add(f"Importunação Sexual")

    @Rule(Denuncia(acoes_realizadas=MATCH.acoes, consentimento=MATCH.consentimento))
    def classificar_conduta_sexual_inadequada(self, acoes, consentimento):
        for acao in acoes:
            if acao in ACOES_CONDUTA:
                if not consentimento.get(acao, True):
                    motivo_de_ser_assedio = f"sem consentimento"
                    self.declare(Classificacao(tipo="Conduta Sexual", subtipo="",
                                               acao=acao, motivo=motivo_de_ser_assedio))
                    self.resultados.add(f"Conduta Sexual Inadequada")

    #################### PARTE DE EXPLICAÇÃO PARA O USUÁRIO ####################

    @Rule(Classificacao(tipo="Assédio Sexual",subtipo="Horizontal",acao=MATCH.acao, motivo=MATCH.motivo))
    def explicar_assedio_sexual_horizontal(self, acao, motivo):
        self.explicacoes.append(f"SE houve {acao} por colega ou desconhecido {motivo}, ENTÃO pode haver Assédio Sexual (Horizontal).")

    @Rule(Classificacao(tipo="Assédio Sexual",subtipo="Vertical",acao=MATCH.acao, motivo=MATCH.motivo))
    def explicar_assedio_sexual_vertical(self, acao, motivo):
        self.explicacoes.append(f"SE houve {acao} por superior hierárquico {motivo}, ENTÃO pode haver Assédio Sexual (Vertical).")

    @Rule(Classificacao(tipo="Importunação Sexual", acao=MATCH.acao, motivo=MATCH.motivo))
    def explicar_importunacao_sexual(self, acao, motivo):
        self.explicacoes.append(f"SE houve {acao} {motivo} independente de hierarquia profissional, ENTÃO pode haver Importunação Sexual.")

    @Rule(Classificacao(tipo="Conduta Sexual Inadequada", acao=MATCH.acao, motivo=MATCH.motivo))
    def explicar_conduta_sexual_inadequada(self, acao, motivo):
        self.explicacoes.append(f"SE houve {acao} {motivo} independente de hierarquia profissional, ENTÃO pode haver Conduta Sexual Inadequada.")

    #################### PARTE DE ORIENTAÇÃO PARA O USUÁRIO ####################
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
    @Rule(Classificacao(tipo="Assédio Sexual", subtipo=MATCH.subtipo, acao=MATCH.acao, motivo=MATCH.motivo))
    def orientar_boletim_ocorrencia(self, subtipo, acao, motivo):
        if(subtipo == "Vertical"):
            self.declare(Orientacao(
                mensagem=f"Recomendamos que você registre um boletim de ocorrência por conta de {acao} {motivo} por conhecido ou colega de trabalho."))
        elif(subtipo == "Horizontal"):
            self.declare(Orientacao(
                mensagem=f"Recomendamos que você registre um boletim de ocorrência por conta de {acao} {motivo} por superior hierárquico."))

    # Orientação para casos de Importunação Sexual
    @Rule(Classificacao(tipo="Importunação Sexual", acao=MATCH.acao))
    def orientar_importunacao(self, acao):
        self.declare(
            Orientacao(mensagem=f"Recomendamos comunicar o ato de {acao} à ouvidoria da UFAPE."))

    # Orientação para casos de Conduta Sexual
    @Rule(Classificacao(tipo="Conduta Sexual", acao=MATCH.acao))
    def orientar_conduta(self, acao):
        self.declare(Orientacao(
            mensagem=f"Sugerimos que relate a situação de '{acao}' à diretoria da UFAPE, pois ainda que não seja crime, é inadequado para o ambiente acadêmico."))

    # Registro da Orientação no conjunto de orientações
    @Rule(Orientacao(mensagem=MATCH.msg))
    def registrar_orientacao(self, msg):
        self.orientacoes.append(msg)

    #################### PARTE DE REFERÊNCIAS AO GUIA ####################
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
