
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def buscar_aliexpress(termo, num_resultados=10):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    url = f"https://www.aliexpress.com/wholesale?SearchText={termo.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return pd.DataFrame([{"Erro": f"Erro ao buscar AliExpress: Status {response.status_code}"}])

    soup = BeautifulSoup(response.text, "html.parser")
    resultados = []

    for item in soup.select("a._3t7zg")[:num_resultados]:
        nome = item.get("title") or item.text.strip()
        link = "https:" + item.get("href") if item.get("href", "").startswith("//") else item.get("href")
        preco = item.select_one("div._12A8D")
        img = item.select_one("img")
        resultados.append({
            "Produto": nome,
            "Preço": preco.text.strip() if preco else "N/A",
            "Link": link,
            "Imagem": img.get("src") if img else None
        })

    return pd.DataFrame(resultados)

# Interface Streamlit
st.set_page_config(page_title="Busca AliExpress em Tempo Real", layout="wide")
st.title("🔎 Busca de Produtos - AliExpress")

termo = st.text_input("Digite o que deseja buscar:", value="boneca reborn")

if termo:
    df_resultados = buscar_aliexpress(termo)
    if 'Erro' in df_resultados.columns:
        st.error(df_resultados.iloc[0]['Erro'])
    else:
        for _, row in df_resultados.iterrows():
            st.markdown(f"### [{row['Produto']}]({row['Link']})")
            st.image(row['Imagem'], width=150)
            st.write(f"**Preço:** {row['Preço']}")
            st.markdown("---")
