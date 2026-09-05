import json
import requests
from bs4 import BeautifulSoup

# Lista com os portais de onde o robô vai puxar os dados
FONTES = [
    "https://www.futebolpeneira.com.br/"
]

def buscar_peneiras():
    peneiras_coletadas = []
    
    for url in FONTES:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resposta = requests.get(url, headers=headers, timeout=10)
            
            if resposta.status_code == 200:
                soup = BeautifulSoup(resposta.text, 'html.parser')
                postagens = soup.select('.post, .artigo, article')
                
                for index, post in enumerate(postagens):
                    titulo = post.select_one('.entry-title, h2, h3, a')
                    link = post.select_one('a')
                    
                    if titulo and link:
                        peneiras_coletadas.append({
                            "id": index + 1,
                            "esporte": "Futebol de Campo",
                            "clube": titulo.get_text(strip=True)[:50],
                            "estado": "BR",
                            "cidade": "A consultar no edital",
                            "endereco": "Consulte o edital oficial",
                            "categoria": "Diversas",
                            "status": "Inscrições Abertas",
                            "observacao": "Coletado automaticamente.",
                            "requisitos": "Verifique detalhes no edital oficial.",
                            "fonte": link['href']
                        })
        except Exception as e:
            print(f"Erro ao buscar em {url}: {e}")

    # Escreve os dados raspados diretamente na nossa gaveta JSON
    with open('peneiras.json', 'w', encoding='utf-8') as f:
        json.dump(peneiras_coletadas, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    buscar_peneiras()
