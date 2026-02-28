import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Motor de Background Check", page_icon="🔍")

st.title("🔍 Motor de Background Check - SuaQuadra")
st.write("Consulta automatizada de dados societários via BrasilAPI.")

# Campo para digitar o CNPJ
cnpj_input = st.text_input("Digite o CNPJ do locatário (com ou sem pontuação):")

# Botão para iniciar a busca
if st.button("Analisar CNPJ"):
    if cnpj_input:
        # 1. Limpeza de dados: tira pontos, barras e traços e deixa só os números
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj_input))
        
        if len(cnpj_limpo) != 14:
            st.warning("⚠️ Um CNPJ válido deve ter exatamente 14 números.")
        else:
            with st.spinner("Consultando as bases da Receita Federal..."):
                # 2. Faz a requisição na API gratuita
                url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
                response = requests.get(url)
                
                # 3. Analisa a resposta e monta a tela
                if response.status_code == 200:
                    dados = response.json()
                    st.success("✅ Dados extraídos com sucesso!")
                    
                    # Exibe os dados principais
                    st.subheader(f"🏢 {dados.get('razao_social', 'N/A')}")
                    
                    # Divide em duas colunas para ficar bonito
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome Fantasia:** {dados.get('nome_fantasia', 'N/A')}")
                        st.write(f"**Situação:** {dados.get('descricao_situacao_cadastral', 'N/A')}")
                        st.write(f"**Abertura:** {dados.get('data_inicio_atividade', 'N/A')}")
                        
                    with col2:
                        st.write(f"**Atividade (CNAE):** {dados.get('cnae_fiscal_descricao', 'N/A')}")
                        st.write(f"**Capital Social:** R$ {dados.get('capital_social', 0):,.2f}")
                        st.write(f"**Local:** {dados.get('municipio', 'N/A')} - {dados.get('uf', 'N/A')}")
                    
                    st.markdown("---")
                    
                    # Exibe o Quadro Societário (quem são os donos)
                    st.write("**👥 Quadro Societário (QSA):**")
                    qsa = dados.get('qsa', [])
                    if qsa:
                        for socio in qsa:
                            st.write(f"- {socio.get('nome_socio')} ({socio.get('qualificacao_socio')})")
                    else:
                        st.write("Nenhum sócio listado na base.")
                        
                else:
                    st.error("❌ CNPJ não encontrado. Verifique o número digitado.")
    else:
        st.info("Por favor, insira um CNPJ para começar.")