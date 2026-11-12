import json
import time
import urllib.request
import urllib.parse
import urllib.error
import re
import unicodedata

CIDADES_BRASIL = [
    ("João Pessoa", "PB"),
    ("Recife", "PE"),
    ("Natal", "RN"),
    ("Fortaleza", "CE"),
    ("Salvador", "BA"),
    ("São Paulo", "SP"),
    ("Rio de Janeiro", "RJ"),
    ("Belo Horizonte", "MG"),
    ("Curitiba", "PR"),
    ("Goiânia", "GO"),
    ("Brasília", "DF"),
    ("Campina Grande", "PB")
]

NICHOS_ALVO = [
    "restaurant",
    "fast_food",
    "car_repair",
    "beauty",
    "hairdresser",
    "clinic",
    "dentist",
    "veterinary"
]

# Servidores espelho da Overpass API (fallback automático se um der timeout)
SERVIDORES_OVERPASS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

def gerar_slug(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s-]', '', texto.lower())
    return re.sub(r'[-\s]+', '-', texto).strip('-')

def limpar_whatsapp(telefone):
    if not telefone:
        return ""
    primeiro_tel = re.split(r'[;/]', telefone)[0]
    numeros = re.sub(r'\D', '', primeiro_tel)
    
    if numeros.startswith("55") and len(numeros) in (12, 13):
        return numeros
    if len(numeros) in (10, 11):
        return "55" + numeros
    return ""

def consultar_overpass_com_fallback(query):
    headers = {
        "User-Agent": "LeadFinderBrasil/1.0 (contato@prospect-local.com.br)",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    dados = urllib.parse.urlencode({"data": query}).encode("utf-8")

    for servidor in SERVIDORES_OVERPASS:
        try:
            req = urllib.request.Request(servidor, data=dados, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=35) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"    [Troca de servidor] {servidor.split('/')[2]} falhou ({e})...")
            time.sleep(1)

    return None

def buscar_leads_cidade(cidade, uf, nichos, limite_por_cidade=4):
    print(f"Buscando leads em {cidade} - {uf}...")
    
    blocos_nicho = ""
    for n in nichos:
        blocos_nicho += f'node["amenity"="{n}"](area.searchArea);\n'
        blocos_nicho += f'way["amenity"="{n}"](area.searchArea);\n'
        blocos_nicho += f'node["shop"="{n}"](area.searchArea);\n'
        blocos_nicho += f'way["shop"="{n}"](area.searchArea);\n'

    query = f"""
    [out:json][timeout:30];
    area["name"="{cidade}"]["admin_level"="8"]->.searchArea;
    (
      {blocos_nicho}
    );
    out center tags;
    """

    resultado = consultar_overpass_com_fallback(query)
    if not resultado:
        print(f"  [Aviso] Nao foi possivel obter resposta para {cidade}-{uf}. Pulando...")
        return []

    elementos = resultado.get("elements", [])
    leads_cidade = []
    nomes_vistos = set()

    for item in elementos:
        if len(leads_cidade) >= limite_por_cidade:
            break

        tags = item.get("tags", {})
        nome = tags.get("name", "").strip()
        if not nome or nome.lower() in nomes_vistos:
            continue

        telefone_bruto = (
            tags.get("contact:whatsapp")
            or tags.get("phone")
            or tags.get("contact:phone")
            or ""
        )
        whatsapp_limpo = limpar_whatsapp(telefone_bruto)

        if not whatsapp_limpo:
            continue

        site = (tags.get("website") or tags.get("contact:website") or "").strip()
        tem_site_proprio = bool(site) and ("instagram.com" not in site.lower()) and ("facebook.com" not in site.lower())
        if tem_site_proprio:
            continue

        nicho_encontrado = tags.get("amenity") or tags.get("shop") or "Negócio Local"
        bairro = tags.get("addr:suburb") or tags.get("addr:neighbourhood") or "Centro"
        rua = tags.get("addr:street") or ""

        nomes_vistos.add(nome.lower())

        lead = {
            "slug": gerar_slug(f"{nome}-{uf}"),
            "nome": nome,
            "ramo": nicho_encontrado.replace("_", " ").title(),
            "cidade": f"{cidade} - {uf}",
            "bairro": bairro,
            "endereco": rua,
            "whatsapp": whatsapp_limpo,
            "instagram_atual": site if "instagram.com" in site.lower() else "",
            "cor_tema": "Vermelho e Dourado" if nicho_encontrado in ("restaurant", "fast_food") else "Azul Moderno e Branco",
            "estilo_visual": "Dark Mode moderno, visual profissional focado em conversao pelo WhatsApp",
            "headline": f"A melhor experiencia em {nome} em {cidade}",
            "subheadline": f"Atendimento especializado, agilidade e qualidade comprovada em {cidade} - {uf}.",
            "oferta": "Agende ou faca seu pedido agora mesmo pelo WhatsApp com atendimento prioritario!"
        }
        leads_cidade.append(lead)

    print(f"  -> {len(leads_cidade)} leads qualificados (com WhatsApp e sem site) encontrados.")
    return leads_cidade

def main():
    print("=" * 65)
    print(" CAPTADOR NACIONAL DE LEADS QUALIFICADOS (COM WHATSAPP / SEM SITE)")
    print("=" * 65)

    todos_leads = []
    meta_total_lote = 20

    for cidade, uf in CIDADES_BRASIL:
        if len(todos_leads) >= meta_total_lote:
            break
            
        encontrados = buscar_leads_cidade(
            cidade=cidade,
            uf=uf,
            nichos=NICHOS_ALVO,
            limite_por_cidade=4
        )
        todos_leads.extend(encontrados)
        time.sleep(2)

    lote_final = todos_leads[:meta_total_lote]

    with open("clientes.json", "w", encoding="utf-8") as f:
        json.dump(lote_final, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print(f" CONCLUIDO! {len(lote_final)} leads reais de todo o Brasil salvos em 'clientes.json'.")
    print(" Revise o arquivo e execute o 'rodar-lote.bat' para produzir os sites.")
    print("=" * 65)

if __name__ == "__main__":
    main()