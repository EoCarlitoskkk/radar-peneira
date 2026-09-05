import json
import urllib.request
import xml.etree.ElementTree as ET

def buscar_peneiras():
    peneiras = []
    
    # Busca expandida para vários esportes
    url = "https://news.google.com/rss/search?q=peneira+OR+selecao+OR+avaliacao+(futebol+OR+futsal+OR+basquete+OR+volei+OR+handebol)+base&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        
        for item in root.findall('.//item')[:20]:
            titulo = item.find('title').text if item.find('title') is not None else "Oportunidade Esportiva"
            link = item.find('link').text if item.find('link') is not None else "#"
            data = item.find('pubDate').text[:16] if item.find('pubDate') is not None else "Recente"
            
            source_elem = item.find('source')
            fonte_nome = source_elem.text if source_elem is not None else "Portal Notícias"
            
            # 1. Identifica o Esporte
         # Mude a ordem de checagem para evitar que vôlei/basquete caiam em Futebol por engano:
titulo_lower = titulo.lower()

if "futsal" in titulo_lower:
    esporte = "Futsal"
elif "volei" in titulo_lower or "vôlei" in titulo_lower:
    esporte = "Vôlei"
elif "basquete" in titulo_lower or "basquetebol" in titulo_lower:
    esporte = "Basquete"
elif "handebol" in titulo_lower:
    esporte = "Handebol"
elif "futebol" in titulo_lower or "campo" in titulo_lower:
    esporte = "Futebol"
else:
    esporte = "Outros"

# Corta nomes de fontes muito longos para não quebrar o layout
fonte_limpa = fonte_nome[:25] + "..." if len(fonte_nome) > 25 else fonte_nome

            

            # 2. Monta os dados de forma organizada
            peneiras.append({
                "clube": titulo,
                "esporte": esporte,
                "cidade": fonte_nome, # Nome do jornal/site responsável
                "estado": "BR",
                "categoria": f"Publicado em: {data}", # Exibe como data de publicação
                "requisitos": "Confira os detalhes completos (datas, locais e categorias) acessando a matéria oficial.",
                "fonte": link
            })

    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")

    if not peneiras:
        peneiras = [
            {
                "clube": "Nenhuma nova peneira encontrada no momento",
                "esporte": "Geral",
                "cidade": "-",
                "estado": "-",
                "categoria": "-",
                "requisitos": "Uma nova verificação será feita automaticamente às 06:00.",
                "fonte": "https://news.google.com"
            }
        ]

    with open('peneiras.json', 'w', encoding='utf-8') as f:
        json.dump(peneiras, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! {len(peneiras)} item(ns) salvo(s).")

if __name__ == "__main__":
    buscar_peneiras()
