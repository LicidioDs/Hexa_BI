import streamlit as st
import pandas as pd

# Carregar dados
@st.cache_data
def load_data():
    data = pd.read_excel(r'C:\Caminhodoarquivo\Dadosextraidos_.xlsx')
    if 'OrderDate' not in data.columns or 'Valor_total' not in data.columns:
        st.error("As colunas 'OrderDate' e 'Valor_total' devem estar presentes no arquivo.")
        return None

    data['data'] = pd.to_datetime(data['OrderDate'], errors='coerce')
    return data

# Função principal do app
def main():
    st.title("Dashboard de Vendas")

    # Carregar dados
    data = load_data()
    if data is None:
        return

    # Exibir os nomes das colunas para depuração
    st.write("Colunas disponíveis:", data.columns.tolist())

    # Filtrar dados com base em um intervalo de datas
    st.sidebar.header("Filtros")
    start_date = st.sidebar.date_input("Data de Início", value=data['data'].min())
    end_date = st.sidebar.date_input("Data de Fim", value=data['data'].max())

    # Filtrar os dados
    filtered_data = data[(data['data'] >= pd.Timestamp(start_date)) & (data['data'] <= pd.Timestamp(end_date))]

    # Calcular KPI
    total_vendas = filtered_data['Valor_total'].sum()
    st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")

    # Exibir os dados filtrados
    st.subheader("Dados Filtrados")
    st.write(filtered_data)

    # Exibir gráfico de vendas
    st.subheader("Gráfico de Vendas")
    st.line_chart(filtered_data.set_index('data')['Valor_total'])

if __name__ == "__main__":
    main()
