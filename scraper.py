import json
import urllib.request
import xml.etree.ElementTree as ET

def buscar_peneiras_google():
    peneiras = []
    
    # URL do feed RSS do Google Notícias pesquisando termos amplos de peneira e avaliação
    url = "https://news.google.com/rss/search?q=peneira+futebol+OR+avaliacao+futebol+base&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    # Simula um navegador real para evitar bloqueios
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        xml_data = response.read()

        # Converte o XML recebido do Google
        root = ET.fromstring(xml_data)
        
        # Encontra todos os itens/notícias
        for item in root.findall('.//item')[:15]:
            titulo = item.find('title').text if item.find('title') is not None else "Oportunidade de Futebol"
            link = item.find('link').text if item.find('link') is not None else "#"
            data = item.find('pubDate').text[:16] if item.find('pubDate') is not None else "Recente"
            
            # Pega o nome da fonte/jornal se disponível
            source_elem = item.find('source')
            fonte_nome = source_elem.text if source_elem is not None else "Google News"
            
            peneiras.append({
                "clube": titulo,
                "esporte": "Futebol",
                "cidade": fonte_nome,
                "estado": "BR",
                "categoria": data,
                "requisitos": "Confira todos os detalhes, faixa etária e local da avaliação no artigo original.",
                "fonte": link
            })

    except Exception as e:
        print(f"Erro ao processar o feed XML: {e}")

    # Mensagem de reserva caso a busca realmente não retorne nada
    if not peneiras:
        peneiras = [
            {
                "clube": "Nenhuma nova peneira encontrada no momento",
                "esporte": "Futebol",
                "cidade": "-",
                "estado": "-",
                "categoria": "-",
                "requisitos": "O robô fez a verificação completa, mas não encontrou novas publicações hoje. Uma nova checagem será feita automaticamente.",
                "fonte": "https://news.google.com"
            }
        ]

    # Salva diretamente no arquivo peneiras.json
    with open('peneiras.json', 'w', encoding='utf-8') as f:
        json.dump(peneiras, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! {len(peneiras)} oportunidade(s) salva(s) em peneiras.json.")

if __name__ == "__main__":
    buscar_peneiras_google()
