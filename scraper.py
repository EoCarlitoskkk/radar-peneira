import json
import requests
from bs4 import BeautifulSoup

def buscar_peneiras_google():
    peneiras = []
    
    # Termo de busca no Google Notícias para peneiras de futebol
    url = "https://news.google.com/rss/search?q=peneira+futebol+quando:7d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # O Google News entrega um XML/RSS super limpo
            soup = BeautifulSoup(response.text, 'xml')
            itens = soup.find_all('item', limit=15)
            
            for item in itens:
                titulo = item.title.text if item.title else "Sem título"
                link = item.link.text if item.link else "#"
                data = item.pubDate.text[:16] if item.pubDate else "Recente"
                
                # Limpa o nome da fonte se houver
                fonte_nome = item.source.text if item.source else "Google Notícias"
                
                peneiras.append({
                    "clube": titulo,
                    "esporte": "Futebol",
                    "cidade": fonte_nome,
                    "estado": "BR",
                    "categoria": data,
                    "requisitos": "Confira os detalhes, datas de inscrição e faixas etárias clicando na matéria oficial abaixo.",
                    "fonte": link
                })
    except Exception as e:
        print(f"Erro ao buscar no Google News: {e}")

    # Garante um aviso amigável caso não haja notícias recentes na semana
    if not peneiras:
        peneiras = [
            {
                "clube": "Nenhuma nova publicação nesta semana",
                "esporte": "Futebol",
                "cidade": "-",
                "estado": "-",
                "categoria": "-",
                "requisitos": "O robô fez a busca no Google Notícias, mas não encontrou novas matérias sobre peneiras nos últimos 7 dias.",
                "fonte": "https://news.google.com"
            }
        ]

    # Salva o resultado no peneiras.json
    with open('peneiras.json', 'w', encoding='utf-8') as f:
        json.dump(peneiras, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! {len(peneiras)} oportunidade(s) capturada(s).")

if __name__ == "__main__":
    buscar_peneiras_google()
