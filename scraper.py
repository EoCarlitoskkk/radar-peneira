import json
import requests
from bs4 import BeautifulSoup

def buscar_peneiras():
    peneiras = []
    
    # Cabeçalho para o site não bloquear o robô
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Exemplo de raspagem 1: Futebol Peneira
    url = "https://www.futebolpeneira.com.br/"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Busca os artigos/posts de peneiras recentes
            artigos = soup.find_all('article', limit=10)
            
            for artigo in artigos:
                titulo_elem = artigo.find(['h2', 'h3', 'h1'])
                link_elem = artigo.find('a')
                
                if titulo_elem and link_elem:
                    titulo = titulo_elem.get_text(strip=True)
                    link = link_elem.get('href', '')
                    
                    # Filtra apenas posts relacionados a futebol ou testes
                    peneiras.append({
                        "clube": titulo,
                        "esporte": "Futebol",
                        "cidade": "Consulte o link",
                        "estado": "BR",
                        "categoria": "Diversas",
                        "requisitos": "Acesse a publicação original para conferir datas, idades e documentos necessários.",
                        "fonte": link
                    })
    except Exception as e:
        print(f"Erro ao buscar no Futebol Peneira: {e}")

    # Garante que não salvamos um arquivo vazio se nada for encontrado
    if not peneiras:
        print("Nenhuma peneira nova capturada nesta rodada. Mantendo lista de aviso.")
        peneiras = [
            {
                "clube": "Nenhuma nova peneira encontrada hoje",
                "esporte": "Futebol",
                "cidade": "-",
                "estado": "-",
                "categoria": "-",
                "requisitos": "O robô executou com sucesso, mas não encontrou novos postos nesta checagem. Uma nova busca será feita às 06:00.",
                "fonte": "https://www.futebolpeneira.com.br/"
            }
        ]

    # Salva o resultado no arquivo peneiras.json
    with open('peneiras.json', 'w', encoding='utf-8') as f:
        json.dump(peneiras, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! {len(peneiras)} item(ns) salvo(s) em peneiras.json.")

if __name__ == "__main__":
    buscar_peneiras()
