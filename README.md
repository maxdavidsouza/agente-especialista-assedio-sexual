# Sistema Especialista - Guia de Bolso sobre Assédio Sexual

## Descrição

Este projeto tem como propósito oferecer uma ferramenta interativa e acessível para auxiliar vítimas, testemunhas ou interessadas(os) em identificar, compreender e classificar situações potencialmente configuradas como assédio sexual, importunação ou conduta inadequada. Através da simulação de um sistema especialista, baseado em regras jurídicas e normativas institucionais, o sistema atua como um guia de bolso informativo, promovendo a conscientização e incentivando a tomada de decisão fundamentada..

---

## Objetivos

- Criar um sistema especialista que utilize lógica baseada em regras para classificar denúncias conforme o contexto e as ações relatadas;
- Permitir o preenchimento anônimo ou por terceiros de denúncias com dados relevantes (ações, local, datas, hierarquia, consentimento, etc.);
- Identificar e justificar, com base em inferência automatizada, casos de assédio sexual, importunação, conduta sexual ou ausência de infração;
- Fornecer orientações claras e referências que ajudem a vítima ou a testemunha a entender seus direitos e caminhos de denúncia;
- Possibilitar a geração de relatórios em PDF com os resultados e orientações emitidas pelo sistema;
- Servir como recurso educativo e de apoio institucional no combate ao assédio e à violência de gênero.

---

## Tecnologias Utilizadas

- Python 3.9.13 (use esta versão ou inferior para ter suporte ao experta)
- Streamlit
- Experta
- FPDF
- datetime
- os

Utilize o comando: pip install fpdf2 streamlit experta 

para instalar as dependências necessárias

---

## Funcionamento

Fluxo geral da aplicação:

![Arquitetura-Agente-Especialista](https://github.com/user-attachments/assets/beac07b6-adc4-404e-bfd7-9e315a22ce03)

1. Coleta de informações sobre a denúncia;
2. Análise por motor de inferência baseado em regras;
3. Exibição dos resultados:
   - Classificações (assédio, importunação, etc.);
   - Justificativas e orientações;
4. Geração de relatório em PDF (opcional).

---

