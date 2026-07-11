# 🚀 VeloDash - Dashboard Operacional e de Performance

O **VeloDash** é uma aplicação web interativa desenvolvida em Python para análise de dados operacionais e gerenciamento de métricas financeiras de pedidos. 

---

## 📊 Funcionalidades Principais

*   **Carregamento Dinâmico de Dados:** Suporte para importação de planilhas nos formatos `.csv` e `.xlsx` com validação de estrutura interna à prova de falhas.
*   **Métricas em Tempo Real (KPIs):** Visualização instantânea do total de registros, valor financeiro acumulado e média de faturamento por pedido.
*   **Filtros Avançados Globais:** Filtragem dinâmica na barra lateral por período temporal, categorias de produtos e status do processo.
*   **Centro de Gráficos Interativos:** 
    *   *Gráfico de Linha:* Evolução temporal da soma de valores ao longo dos dias.
    *   *Gráfico de Rosca:* Distribuição percentual do volume financeiro por status.
*   **Tabela de Auditoria Estilizada:** Exibição centralizada dos dados brutos com pílulas e tags de status de acordo com o progresso do pedido.
*   **Exportação customizada (Etapa 6):** Botão nativo para baixar no computador um arquivo `.csv` contendo apenas os dados filtrados na tela.
*   **Resiliência a Erros (Etapa 7):** Blocos de tratamento de exceções (`try/except`) que blindam a aplicação contra planilhas corrompidas ou dados mal formatados.

---

## 🛠️ Tecnologias Utilizadas

*   **Python 3**
*   **Streamlit** (Interface e Layout do Dashboard)
*   **Pandas** (Tratamento, Higienização e Manipulação de Dados)
*   **Plotly Express** (Gráficos Interativos de Performance)
*   **SQLite3** (Estrutura de Banco de Dados)

---

## 📂 Como Rodar o Projeto Localmente

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO_AQUI/velodash.git](https://github.com/SEU_USUARIO_AQUI/velodash.git)

2. Crie e ative seu ambiente virtual (.venv).
   
3. Instale as dependências obrigatórias:
   pip install -r requirements.txt
  
4. Execute o servidor do Streamlit:
   streamlit run src/app.py
