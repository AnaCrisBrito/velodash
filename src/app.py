import streamlit as st
import pandas as pd
import plotly.express as px
import time as tp
import sqlite3

placeholder = st.empty()

try:
    conexao = sqlite3.connect('velodash.db')
except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}")

@st.cache_data
def converter_df_para_csv(dataframe):
    try:
        return dataframe.to_csv(index=False).encode('utf-8')
    except Exception:
        return b""

st.set_page_config(
    page_title="VeloDash",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        .stFileUploader {
            text-align: center;
        }
        .stFileUploader button {
            width: 100%;
            display: flex;
            justify-content: center;
        }
        
        [data-testid="stMetric"] {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        [data-testid="stSidebar"] h3 {
            color: #0f4c81 !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
            margin-top: 20px !important;
            margin-bottom: 10px !important;
        }

        [data-testid="stSidebar"] label p {
            color: #475569 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("📁 Carregar de Dados")
arquivo_carregado = st.sidebar.file_uploader(
    "Selecione uma planilha (.csv ou .xlsx)",
    type=["csv" , "xlsx"]
)

if arquivo_carregado is not None:
    df = None
    
    try:
        if arquivo_carregado.name.endswith('.csv'):
            df = pd.read_csv(arquivo_carregado)
        elif arquivo_carregado.name.endswith('.xlsx'):
            df = pd.read_excel(arquivo_carregado)
    except Exception as erro_leitura:
        st.error(f"❌ **Erro ao ler o arquivo:** O arquivo pode estar corrompido ou em um formato inválido. Detalhes: {erro_leitura}")
        st.stop()

    if df is not None:
        colunas_esperadas = ['date', 'status', 'valor_unitario', 'cliente', 'responsavel', 'quantidade', 'categoria']

        if set(colunas_esperadas).issubset(df.columns):
            
            try:
                df['status'] = df['status'].astype(str).str.strip().str.lower()
                df['cliente'] = df['cliente'].astype(str).str.strip().str.lower()
                df['responsavel'] = df['responsavel'].astype(str).str.strip().str.lower()
                df['categoria'] = df['categoria'].astype(str).str.strip().str.lower()

                for col in ['status', 'cliente', 'responsavel', 'categoria']:
                    df[col] = df[col].replace(['', 'nan', 'none'], 'não informado')
                    df[col] = df[col].fillna('não informado')

                df = df.dropna(subset=['quantidade', 'valor_unitario', 'date'])
                df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
                
                
                df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').fillna(0)
                df['valor_unitario'] = pd.to_numeric(df['valor_unitario'], errors='coerce').fillna(0.0)
                
                df['valor_total'] = df['quantidade'] * df['valor_unitario']
                
            except Exception as erro_processamento:
                st.error(f"❌ **Erro no processamento dos dados:** A estrutura interna da planilha gerou um conflito. Detalhes: {erro_processamento}")
                st.stop()
            
            placeholder.success("✅ **Importação concluída com sucesso!** Todos os registros foram processados.")
            tp.sleep(1.5)
            placeholder.empty()
            
            total_registros = len(df)
            valor_acumulado = df['valor_total'].sum()
            media_pedido = df['valor_total'].mean()
            
            valor_acumulado_formatado = f"R$ {valor_acumulado:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            media_pedido_formatado = f"R$ {media_pedido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; text-align: center;">
                        <p style="color: #1e293b; font-weight: bold; margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">TOTAL DE REGISTROS</p>
                        <h2 style="margin: 10px 0 5px 0; color: #0f4c81; font-size: 36px; font-weight: bold; white-space: nowrap;">{int(total_registros):,}</h2>
                        <small style="color: #64748b; font-size: 12px;">registros</small>
                    </div>
                """.replace(",", "."), unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; text-align: center;">
                        <p style="color: #1e293b; font-weight: bold; margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">VALOR ACUMULADO</p>
                        <h2 style="margin: 10px 0 5px 0; color: #2e7d32; font-size: 36px; font-weight: bold; white-space: nowrap;">{valor_acumulado_formatado}</h2>
                        <small style="color: #64748b; font-size: 12px;">valor total</small>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; text-align: center;">
                        <p style="color: #1e293b; font-weight: bold; margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">MÉDIA POR PEDIDO</p>
                        <h2 style="margin: 10px 0 5px 0; color: #e67e22; font-size: 36px; font-weight: bold; white-space: nowrap;">{media_pedido_formatado}</h2>
                        <small style="color: #64748b; font-size: 12px;">valor médio</small>
                    </div>
                """, unsafe_allow_html=True)
           
            st.sidebar.subheader("PERÍODO TEMPORAL")

            try:
                min_date = df['date'].min().date()
                max_date = df['date'].max().date()
            except Exception:
                min_date = pd.Timestamp.now().date()
                max_date = pd.Timestamp.now().date()

            data_inicio = st.sidebar.date_input(
                "Data início",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )

            data_fim = st.sidebar.date_input(
                "Data fim",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )

            df_base = df[(df['date'] >= pd.to_datetime(data_inicio)) & (df['date'] <= pd.to_datetime(data_fim))]
            
            st.sidebar.subheader("FILTRAR CATEGORIA")
            selecionar_todas = st.sidebar.checkbox("Todas", value=True, key="chk_todas")

            categorias = [str(cat) for cat in df_base['categoria'].dropna().unique()]
            estados_checkbox = {}

            for categoria in categorias:
                estados_checkbox[categoria] = st.sidebar.checkbox(
                    categoria,
                    value=selecionar_todas,
                    key=f"chk_{categoria}"
                )

            if selecionar_todas:
                categorias_final = categorias
            else:
                categorias_final = [cat for cat, marcado in estados_checkbox.items() if marcado]

            if categorias_final:
                df_filtrado_cat = df_base[df_base['categoria'].astype(str).isin(categorias_final)]
            else:
                df_filtrado_cat = df_base.iloc[0:0]

            st.sidebar.subheader("STATUS DO PROGRESSO")

            status_unicos = [str(status) for status in df_base['status'].dropna().unique()]
            opcoes_radio = ["todos"] + status_unicos

            status_selecionado = st.sidebar.radio(
                "Selecione o status:",
                options=opcoes_radio,
                key="rad_status"
            )

            if status_selecionado == "todos":
                df_final = df_filtrado_cat
            else:
                df_final = df_filtrado_cat[df_filtrado_cat['status'].astype(str) == status_selecionado]

            csv_exportado = converter_df_para_csv(df_final)

            st.sidebar.subheader("📥 DOWNLOAD DOS FILTROS")
            st.sidebar.download_button(
                label="📥 Exportar CSV",
                data=csv_exportado,
                file_name="dados_filtrados_velodash.csv",
                mime="text/csv",
                use_container_width=True
            )
           
            st.markdown("### ▶ SEÇÃO 2: CENTRO DE GRÁFICOS INTERATIVOS")
            
            if not df_final.empty:
                col_graf1, col_graf2 = st.columns(2)
                
                with col_graf1:
                    st.markdown("**GRÁFICO 1: EVOLUÇÃO TEMPORAL** \n*(Soma de Valores ao Longo dos Dias)*")
                    
                    try:
                        df_linha = df_final.groupby(df_final['date'].dt.date)['valor_total'].sum().reset_index()
                        fig_linha = px.line(
                            df_linha,
                            x='date',
                            y='valor_total',
                            labels={'date': 'Data', 'valor_total':'Valor Total (R$)'},
                            markers=True
                        )
                        fig_linha.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig_linha, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Não foi possível renderizar o gráfico de linha: {e}")
                    
                with col_graf2:
                    st.markdown('**GRÁFICO 2: DISTRIBUIÇÃO** \n *Porcentagem por Status*')
                    
                    try:
                        fig_rosca = px.pie(
                            df_final,
                            names='status',
                            values='valor_total',
                            hole=0.4
                        )
                        fig_rosca.update_layout(margin=dict(l=20, r=20, t=20,b=20))
                        st.plotly_chart(fig_rosca, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Não foi possível renderizar o gráfico de rosca: {e}")
            else:
                st.info("Aguardando upload de dados para renderizar os gráficos...")
                
           
            
            st.markdown("---")
            st.markdown("### ▶ SEÇÃO 3: VISUALIZAÇÃO DA BASE DE DADOS")

            if not categorias_final:
                st.info('Nenhuma categoria selecionada na barra lateral.')
            elif df_final.empty:
                st.warning('Nenhum registro encontrado para essa combinação de filtros.')
            else:
                df_visual = df_final.copy()
                df_visual['status'] = df_visual['status'].str.title()

                lista_status_tags = ["Concluído", "Pago", "Pendente", "Cancelado", "Não Informado"]

                col_esquerda, col_centro, col_direita = st.columns([0.2, 9.6, 0.2])

                with col_centro:
                    st.dataframe(
                        df_visual,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "id": st.column_config.NumberColumn("ID_PEDIDO", format="%03d"),
                            "categoria": st.column_config.TextColumn("CATEGORIA"),
                            "date": st.column_config.DatetimeColumn("DATA", format="DD/MM/YYYY"),
                            "status": st.column_config.SelectboxColumn(
                                "STATUS",
                                options=lista_status_tags,
                                required=True
                            ),
                            "valor_unitario": st.column_config.NumberColumn("VALOR", format="R$ %.2f"),
                            "cliente": st.column_config.TextColumn("CLIENTE"),
                            "responsavel": st.column_config.TextColumn("RESPONSÁVEL"),
                            "quantidade": st.column_config.NumberColumn("QTD", format="%d"),
                            "valor_total": st.column_config.NumberColumn("VALOR TOTAL", format="R$ %.2f"),
                        }
                    )  

        else:
            st.error("**Arquivo inválido!** O arquivo enviado não segue o modelo de importação. Verifique se os nomes das colunas estão exatamente iguais aos do arquivo modelo.")
            st.warning('Baixe um dos modelos abaixo para organizar seus dados no formato aceito pelo sistema.')

            try:
                with open('modelo_arquivos/modelo_importacao.csv', 'rb') as arquivo_csv:
                    dados_do_arquivo_csv = arquivo_csv.read()
                st.download_button(label='Clique aqui para baixar o arquivo modelo .csv', data=dados_do_arquivo_csv, file_name='modelo_importacao.csv', mime='text/csv')
            except Exception:
                st.info("Modelo CSV temporariamente indisponível.")

            try:
                with open('modelo_arquivos/modelo_importacao.xlsx', 'rb') as arquivo_xlsx:
                    dados_do_arquivo_xlsx = arquivo_xlsx.read()
                st.download_button(label='Clique aqui para baixar o arquivo modelo .xlsx', data=dados_do_arquivo_xlsx, file_name='modelo_importacao.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            except Exception:
                st.info("Modelo XLSX temporariamente indisponível.")
            st.stop()  

else:
    st.info("**👋 Bem-vindo(a) ao VeloDash!** Para começar, utilize a barra lateral à esquerda para enviar uma planilha no formato .CSV ou .XLSX.")

    try:
        with open('modelo_arquivos/modelo_importacao.csv', 'rb') as arquivo_csv:
            dados_do_arquivo_csv = arquivo_csv.read()
        st.download_button(label='Clique aqui para baixar o arquivo modelo .csv', data=dados_do_arquivo_csv, file_name='modelo_importacao.csv', mime='text/csv')
    except Exception:
        pass

    try:
        with open('modelo_arquivos/modelo_importacao.xlsx', 'rb') as arquivo_xlsx:
            dados_do_arquivo_xlsx = arquivo_xlsx.read()
        st.download_button(label='Clique aqui para baixar o arquivo modelo .xlsx', data=dados_do_arquivo_xlsx, file_name='modelo_importacao.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception:
        pass