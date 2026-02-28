import streamlit as st
import requests
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Motor de Background Check", page_icon="🔍")

st.title("🔍Background Check - SuaQuadra")
st.write("Consulta automatizada de dados societários e geração de Dossiê de Risco.")

# Campo para digitar o CNPJ
cnpj_input = st.text_input("Digite o CNPJ do locatário (com ou sem pontuação):")

if st.button("Analisar CNPJ e Gerar Dossiê"):
    if cnpj_input:
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj_input))
        
        if len(cnpj_limpo) != 14:
            st.warning("⚠️ Um CNPJ válido deve ter exatamente 14 números.")
        else:
            with st.spinner("Consultando as bases da Receita Federal..."):
                url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    dados = response.json()
                    razao_social = dados.get('razao_social', 'N/A')
                    
                    st.success("✅ Dados extraídos com sucesso!")
                    
                    # --- SEÇÃO 1: DADOS DA EMPRESA ---
                    st.subheader(f"🏢 {razao_social}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome Fantasia:** {dados.get('nome_fantasia', 'N/A')}")
                        st.write(f"**Situação:** {dados.get('descricao_situacao_cadastral', 'N/A')}")
                        st.write(f"**Abertura:** {dados.get('data_inicio_atividade', 'N/A')}")
                        
                    with col2:
                        st.write(f"**Atividade (CNAE):** {dados.get('cnae_fiscal_descricao', 'N/A')}")
                        st.write(f"**Capital Social:** R$ {dados.get('capital_social', 0):,.2f}")
                        st.write(f"**Local:** {dados.get('municipio', 'N/A')} - {dados.get('uf', 'N/A')}")
                    
                    # --- SEÇÃO 2: RADAR DE RISCO (A NOVA FUNÇÃO) ---
                    st.markdown("---")
                    st.subheader("🚨 Radar de Risco (Pesquisa a 1 Clique)")
                    st.caption("Links gerados automaticamente para investigação de Mídia Negativa e Processos.")
                    
                    # Função interna para criar os links
                    def gerar_links_investigacao(nome):
                        # Link do Jusbrasil
                        query_jusbrasil = urllib.parse.quote(nome)
                        url_jusbrasil = f"https://www.jusbrasil.com.br/busca?q={query_jusbrasil}"
                        
                        # Link do Google com operadores avançados (Mídia Negativa)
                        query_google = urllib.parse.quote(f'"{nome}" AND ("fraude" OR "lavagem" OR "corrupção" OR "condenação" OR "golpe")')
                        url_google = f"https://www.google.com/search?q={query_google}"
                        
                        return f"[⚖️ Jusbrasil]({url_jusbrasil}) | [📰 Mídia Negativa]({url_google})"

                    # Mostra os links da Empresa
                    st.write(f"**Empresa:** {razao_social}  \n" + gerar_links_investigacao(razao_social))
                    
                    st.write("**👥 Quadro Societário (QSA):**")
                    qsa = dados.get('qsa', [])
                    if qsa:
                        for socio in qsa:
                            nome_socio = socio.get('nome_socio')
                            qualificacao = socio.get('qualificacao_socio')
                            links = gerar_links_investigacao(nome_socio)
                            
                            # Exibe o nome do sócio e os links clicáveis do lado
                            st.markdown(f"- **{nome_socio}** ({qualificacao})  \n  ↳ {links}")
                    else:
                        st.write("Nenhum sócio listado na base.")
                        
                else:
                    st.error("❌ CNPJ não encontrado. Verifique o número digitado.")
    else:
        st.info("Por favor, insira um CNPJ para começar.")
