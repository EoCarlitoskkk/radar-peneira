import json
import requests
from bs4 import BeautifulSoup

def buscar_peneiras_google():
    peneiras = []
    
    # Busca no Google Notícias por matérias recentes de peneiras
    url = "https://news.google.com/rss/search?q=peneira+futebol+quando:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html-parser' if 'html-parser' in str(BeautifulSoup) else 'html.parser')
            itens = soup.find_all('item')
            
            for item in itens[:15]:
                titulo = item.find('title').get_text(strip=True) if item.find('title') else "Sem título"
                link = item.find('link').next_sibling if item.find('link') else "#"
                if not isinstance(link, str):
                    link = item.find('link').get_text(strip=True) if item.find('link') else "#"
                
                data = item.find('pubdate').get_text(strip=True)[:16] if item.find('pubdate') else "Recente"
                fonte_nome = item.find('source').get_text(strip=True) if item.find('source') else "Google Notícias"
                
                peneiras.append({
                    "clube": titulo,
                    "esporte": "Futebol",
                    "cidade": fonte_nome,
                    "estado": "BR",
                    "categoria": data,
                    "requisitos": "Confira os detalhes e datas na matéria original.",
                    "fonte": link
                })
    except Exception as e:
        print(f"Erro ao buscar no Google News: {e}")

    if not peneiras:
        peneiras = [
            {
                "clube": "Nenhuma nova peneira encontrada nesta semana",
                "esporte": "Futebol",
                "cidade": "-",
                "estado": "-",
                "categoria": "-",
                "requisitos": "O robô executou, mas não encontrou publicações recentes nos últimos 7 dias.",
                "fonte": "https://news.google.com"
            }
        ]

    with open('peneiras.json', 'w', encoding='utf-8') as f:
        json.dump(peneiras, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! {len(peneiras)} item(ns) salvo(s).")

if __name__ == "__main__":
    buscar_peneiras_google()
