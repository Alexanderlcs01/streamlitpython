import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from prophet import Prophet
from datetime import date
from streamlit_option_menu import option_menu

# Configurações gerais
st.set_page_config(layout="centered", page_title="Análise do Preço do Petróleo")

#Carregando dados
dados = pd.read_excel("Base_Tech.xlsx", parse_dates=["data"])
dados.rename(columns={"data": "ds", "preco": "y"}, inplace=True)
dados["ds"] = pd.to_datetime(dados["ds"])
dados["ano"] = dados["ds"].dt.year
dados["media"] = dados.groupby("ano")["y"].transform("mean").round(2)
dados["y"] = dados["y"].round(2)
dados.sort_values(by="ds", ascending=True, inplace=True)

dados_dv = pd.read_excel("Base_Dv.xlsx", parse_dates=["ds"])
dados_dv.sort_values(by="ds", ascending=True, inplace=True)

dados_dv_ano = dados_dv.copy()
dados_dv_ano["ano"] = dados_dv["ds"].dt.year
dados_dv_ano = dados_dv_ano.drop(columns=['ds'])
dados_dv_ano["Media_Diesel"] = dados_dv_ano.groupby("ano")["Diesel"].transform("mean").round(2)
dados_dv_ano["Media_Diesel_S10"] = dados_dv_ano.groupby("ano")["Diesel S10"].transform("mean").round(2)
dados_dv_ano["Media_Etanol"] = dados_dv_ano.groupby("ano")["Etanol"].transform("mean").round(2)
dados_dv_ano["Media_Gasolina"] = dados_dv_ano.groupby("ano")["Gasolina"].transform("mean").round(2)
dados_dv_ano["Media_Gasolina_Aditivada"] = dados_dv_ano.groupby("ano")["Gasolina Aditivada"].transform("mean").round(2)
dados_dv_ano["Media_GNV"] = dados_dv_ano.groupby("ano")["GNV"].transform("mean").round(2)
dados_dv_ano = dados_dv_ano.drop(columns=["Diesel","Diesel S10","Etanol","Gasolina","Gasolina Aditivada","GNV"])
dados_dv_ano = dados_dv_ano.groupby(["ano"]).mean()

# Inicializar valores padrão no session_state
if "data_inicio" not in st.session_state:
    st.session_state.data_inicio = date(2018, 1, 1)
if "data_fim" not in st.session_state:
    st.session_state.data_fim = date(2023, 12, 31)


# Menu lateral
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Participantes", "Introdução", "Desenvolvimento", "Paineis Interativos", "Referências"],
        icons=["people-fill", "book-fill", "book-fill", "bar-chart-fill", "list-columns-reverse"],
        menu_icon="grid-fill",
        default_index=0,
    )

    # Submenu para Paineis
    if selected == "Paineis Interativos":
        submenu = option_menu(
            menu_title="SubMenu Paineis",
            options=["Apresentação Geral", "Previsão de Dados", "Derivados"],
            default_index=0,
        )


# Seção: Participantes
if selected == "Participantes":

    st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="margin-bottom: 1rem;">FIAP - PÓS TECH - DATA ANALYTICS</h1>
        <h2 style="margin-bottom: 1rem;">FASE 4 - TECH CHALLENGE</h2>
        <h3 style="margin-bottom: 1rem;">TURMA 5DTAT - GRUPO 44</h3>
        <h4 style="margin-bottom: 2rem;">INTEGRANTES</h4>
        <p style="font-size: 20px; line-height: 1.5;">
            Gabriel Silva Ferreira<br>
            Gustavo Duran Domingues<br>
            Jhonny Amorim Silva<br>
            Lucas Alexander dos Santos<br>
            Sandro Semmer
        </p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Seção: Introdução
if selected == "Introdução":
    st.markdown("""


    # Análise e Previsão do Petróleo
    #### Utilizamos o modelo de Predição Prophet para tentar prever o preço diário do petróleo em (U$D)
                
    __Este projeto é para fins educativos, não recomendamos como investimento de qualquer natureza.__
    
    # O petróleo Brent 
    
    O Petróleo Brent é denominado assim por ser extraído de uma plataforma da Shell no Mar do Norte e que leva este mesmo nome.
    A Shell costumava nomear seus campos de exploração fazendo referência a aves aquáticas como o ganso-bravo (brent goose). <br>
    O barril **Brent** é o valor de referência mundial, usado, inclusive, pela política de preços da Petrobras. 
    É um tipo de petróleo bruto leve e doce e que possui baixo teor de enxofre e densidade, extraído do Mar do Norte, entre a Noruega e o Reino Unido. 
    Ele serve como referência global para precificação de mais de dois terços do petróleo comercializado no mundo, sendo fundamental para a economia global 
    e influenciando diversos setores, desde combustíveis até produtos petroquímicos. <br>
    Servindo como padrão global para precificação de outros tipos de petróleo, como o WTI (West Texas Intermediate), outro tipo de petróleo e barril, dos Estados Unidos. <br>
    O Brent é usado para calcular o valor de aproximadamente dois terços do petróleo comercializado no mundo e é conhecido por ter uma menor densidade e por ter baixo teor de enxofre, características que o tornam ideal para refino 
    de combustíveis como gasolina e diesel.
    
    """, unsafe_allow_html=True)


# Seção: Desenvolvimento
if selected == "Desenvolvimento":
    st.title("Análise do Preço do Petróleo")

    st.markdown("""
                
    Realizamos a utilizacao dos dados que foram disponibilizados pelo IPEA. <br>
    A base de dados conta com o histórico desde 1987 até os dias de hoje, tendo resultados consisos sobre o preço do petróleo.<br>
    Para avaliar o modelo de machine learning desenvolvido para prever o valor diário (utilizando séries temporais), 
    empregamos dados de 2018 a 2023. Apesar da base de dados possuir mais de 30 anos, este período foi selecionado para a análise, 
    permitindo a comparação dos resultados do modelo com os dados reais de 2024.

    A utilização do periodo de 2018 à outubro de 2024 se justifica pelos fatores da crise econômica como por exemplo, a Grande Recessão de 2008 ou geopolíticas como a Guerra do Iraque de 2003.
    Estes fatos ocorream em decadas anteriores e causaram uma grande volatilidade no preço do petróleo.

    Tendo isso em mente, Consideramos que uma analise de um curto período já surja efeito em nossa análise, visto que nos anos de  2020 ocorreu a pandemia da COVID-19 e em nossa anlise
    é possive identificar que estefator impactou no preço do petróleo e também é valido citar a guerra da Ucrania e Russia que ainda ocorre atualmente.
                            
    """, unsafe_allow_html=True)

    fig = px.line(dados, x="ds", y="y", title="Histórico do Preço do Petróleo")
    fig.update_layout(xaxis_title="Data de Referência", yaxis_title="Preço (em US$)", template="plotly_white")
    st.plotly_chart(fig)
    
    st.markdown("""

    Sobre o seguinte gráfico e análise e acompanhamento do fechamento do valor do petróleo, podemos tirar as seguintes conclusões:
    A pandemia de COVID-19, iniciada em meados de 2020, impactou fortemente nos preços. 
    O preço estava entre 70,25 dólares no início do mês de janeiro e atingiu o menor valor que ocorreu em 21 de Abril de 2020 com preço em  9,12 dólares
    
    """)



# Seção: Paineis
if selected == "Paineis Interativos":
    if submenu == "Apresentação Geral":
        st.title("Visualização dos Dados")

        # Intervalo de datas
        st.write("### Selecione um intervalo de datas:")
        intervalo_datas = st.date_input(
            "Intervalo de datas",
            value=(st.session_state.data_inicio, st.session_state.data_fim)
        )
        
        st.session_state.data_inicio, st.session_state.data_fim = intervalo_datas

        # Filtrar os dados com base no intervalo
        df_filtrado = dados[
            (dados["ds"] >= pd.to_datetime(st.session_state.data_inicio)) &
            (dados["ds"] <= pd.to_datetime(st.session_state.data_fim))
        ]

        # Gerar o gráfico de preço
        fig_preco = px.line(df_filtrado, x="ds", y="y", title="Variação do Preço do Petróleo")
        fig_preco.update_layout(
            xaxis_title="Data de Referência",
            yaxis_title="Preço (em US$)",
            template="plotly_white"
        )

        #Intervalo de anos
        df_filtrado_ano = dados[
            (dados["ds"] >= pd.to_datetime(st.session_state.data_inicio)) &
            (dados["ds"] <= pd.to_datetime(st.session_state.data_fim))
        ]

        # Gerar o gráfico de média anual
        fig_media = px.bar(df_filtrado_ano, x="ano", y="media", title="Média Anual do Preço do Petróleo")
        fig_media.update_layout(
            xaxis_title="Ano",
            yaxis_title="Média de Preço (em US$)",
            template="plotly_white"
        )
        fig_media.update_traces(text=dados["media"], textposition="outside")

        # Armazenar o gráfico no session_state
        st.session_state.grafico_preco = fig_preco
        st.session_state.grafico_media = fig_media

        # Mostrar o gráfico de preço se disponível
        if st.session_state.grafico_preco:
            st.plotly_chart(st.session_state.grafico_preco)

        # Mostrar o gráfico de média anual se disponível
        if st.session_state.grafico_media:
            st.plotly_chart(st.session_state.grafico_media)
            

    if submenu == "Previsão de Dados":
        st.title("Previsão dos Dados")

        # Gráfico histórico de preços
        fig = px.line(dados, x="ds", y="y", title="Histórico do Preço do Petróleo")
        fig.update_layout(xaxis_title="Data de Referência", yaxis_title="Preço (em US$)", template="plotly_white")
        st.plotly_chart(fig)

        # Remover colunas desnecessárias (como 'ano' e 'media', se existirem)
        df_1 = dados.copy().drop(columns=["ano", "media"], errors='ignore')
        
        # Treinamento do Modelo Prophet
        model = Prophet()
        model.fit(df_1)

        # Previsão do Modelo - cria 10 dias futuros
        future_p = model.make_future_dataframe(periods=120, freq='B')  # Frequência diária (10 dias de previsão)
        forecast_p = model.predict(future_p)

        # Dividir os dados em históricos e futuros
        historical_forecast = forecast_p[forecast_p['ds'] <= df_1['ds'].max()]
        future_forecast = forecast_p[forecast_p['ds'] > df_1['ds'].max()]

        # Gráfico com cores distintas
        fig_colored = go.Figure()

        # Dados históricos
        fig_colored.add_trace(go.Scatter(
            x=historical_forecast['ds'], y=historical_forecast['yhat'], 
            mode='lines', name='Histórico', 
            line=dict(color='blue')
        ))

        # Dados de previsão
        fig_colored.add_trace(go.Scatter(
            x=future_forecast['ds'], y=future_forecast['yhat'], 
            mode='lines', name='Previsão', 
            line=dict(color='orange')
        ))

        # Configuração final do gráfico
        fig_colored.update_layout(
            title="Previsão do Preço do Petróleo",
            xaxis_title="Data",
            yaxis_title="Preço (em US$)",
            template="plotly_white"
        )

        # Intervalo de datas
        st.write("### Selecione uma data:")

        data_ref = st.date_input("Intervalo de datas")

        # Filtrar os dados com base no intervalo
        prev = future_forecast[
            future_forecast["ds"] == pd.to_datetime(data_ref)
        ]

        grafico = future_forecast[
            (future_forecast["ds"] >= pd.to_datetime('01/11/2024')) &
            (future_forecast["ds"] <= pd.to_datetime(data_ref))
        ]

        # Gráfico com cores distintas
        grafico_1 = go.Figure()

        # Dados históricos
        grafico_1.add_trace(go.Scatter(
            x=grafico['ds'], y=grafico['yhat'], 
            mode='lines', name='Histórico', 
            line=dict(color='green')
        ))

        st.plotly_chart(grafico_1)
        
    # Seção: Desenvolvimento
    if submenu == "Derivados":
        st.title("Derivados")
        st.write("Produtos Derivados do Petróleo.")

        # Inicializar valores padrão no session_state
        if "data_inicio_ano" not in st.session_state:
            st.session_state.data_inicio_ano = date(2019, 1, 1)
        if "data_fim_ano" not in st.session_state:
            st.session_state.data_fim_ano = date(2024, 12, 31)

        

        intervalo_datas = st.date_input(
            "Intervalo de datas",
            value=(st.session_state.data_inicio_ano, st.session_state.data_fim_ano)
        )

        lista = ["Diesel","Diesel S10","Etanol","Gasolina","Gasolina Aditivada","GNV"]

        input_dv = st.multiselect(
            "Selecione os derivados:",  # Rótulo do campo
            options=lista,             # Opções disponíveis
            default=["Diesel","Diesel S10","Etanol","Gasolina","Gasolina Aditivada","GNV"]  # Valor(es) padrão
        )


        st.session_state.data_inicio_ano, st.session_state.data_fim_ano = intervalo_datas

        # Filtrar os dados com base no intervalo
        df_dv_filtrado = dados_dv[
            (dados_dv["ds"] >= pd.to_datetime(st.session_state.data_inicio_ano)) &
            (dados_dv["ds"] <= pd.to_datetime(st.session_state.data_fim_ano))
        ]

        # Gerar o gráfico de preço
        fig_preco_dv = px.line(df_dv_filtrado, x="ds", y=input_dv, title="Variação do Preço dos Derivados do Petróleo")
        st.plotly_chart(fig_preco_dv)

        fig_preco_dv.update_layout(
            xaxis_title="Data de Referência",
            yaxis_title="Preço (em US$)",
            template="plotly_white"
        )

        lista = ["Media_Diesel", "Media_Diesel_S10", "Media_Etanol", "Media_Gasolina", "Media_Gasolina_Aditivada", "Media_GNV"]

        input_dv_ano = st.multiselect(
            "Selecione os derivados:",  # Rótulo do campo
            options=lista,             # Opções disponíveis
            default=["Media_Diesel", "Media_Diesel_S10", "Media_Etanol", "Media_Gasolina", "Media_Gasolina_Aditivada", "Media_GNV"]  # Valor(es) padrão
        )


        # Garantir que a coluna 'ano' seja criada corretamente
        dados_dv_ano["ano"] = dados_dv_ano.index

        # Filtrar os dados com base no intervalo de anos
        df_dv_filtrado_ano = dados_dv_ano[
            (dados_dv_ano["ano"] >= st.session_state.data_inicio_ano.year) &
            (dados_dv_ano["ano"] <= st.session_state.data_fim_ano.year)
        ]

        # Gráfico de barras para os derivados
        fig_preco_dv_ano = px.bar(
            df_dv_filtrado_ano, 
            x="ano", 
            y=input_dv_ano, 
            title="Variação do Preço dos Derivados do Petróleo"
        )

        # Atualizando o layout do gráfico
        fig_preco_dv_ano.update_layout(
            xaxis_title="Ano",
            yaxis_title="Média de Preço (em US$)",
            template="plotly_white"
        )

        # Adicionando os valores sobre as barras
        fig_preco_dv_ano.update_traces(
            texttemplate='%{y}', 
            textposition='outside'
        )

        # Exibir o gráfico
        st.plotly_chart(fig_preco_dv_ano)

# Seção: Referências
if selected == "Referências":
    st.write('Teste')

   
