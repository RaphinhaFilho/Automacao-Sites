import os
import json
import time
import random
import urllib.request
import urllib.error

# Lê a chave da variável de ambiente (definida no rodar-lote.bat) para segurança no Git
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Pasta onde todos os sites gerados ficarão organizados
PASTA_DESTINO_SITES = "sites"

# Variações de arquitetura editorial/sólida (sem estética genérica de IA)
ARQUITETURAS_LAYOUT = [
    {
        "nome": "Split-Screen Editorial Assimétrico",
        "instrucao": "Hero dividido em 2 colunas com linha divisória visível (border-r) ou bloco de cor sólida contrastante à direita. Seções alternadas entre fundo base sólido e fundo secundário sólido, usando bordas finas (1px) e tipografia pesada."
    },
    {
        "nome": "Bento Grid Estrutural (Bordas Nítidas)",
        "instrucao": "Estruture os diferenciais e serviços em um Bento Grid assimétrico com cartões de fundo sólido, bordas definidas (border-2) e sombras sólidas offset (ex: shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] no light mode ou borda contrastante no dark mode)."
    },
    {
        "nome": "Suíço / Minimalista de Alto Contraste",
        "instrucao": "Layout inspirado em design editorial suíço: muito respiro, títulos gigantes, numeração destacada (01, 02, 03), linhas horizontais divisórias (border-t / border-b) e blocos de texto alinhados em grid rígido sem caixas desnecessárias."
    },
    {
        "nome": "Conversão Direta com Faixa Superior e Cards Sólidos",
        "instrucao": "Barra superior sólida de aviso/oferta, Hero com caixa de agendamento/contato rápido em destaque sólido ao lado da headline, e seção de serviços em grid limpo com tags de categoria e botões retos ou levemente arredondados (rounded-lg)."
    }
]

# Combinações de fontes do Google Fonts
TIPOGRAFIAS = [
    "Plus Jakarta Sans (títulos) e Inter (corpo)",
    "Space Grotesk (títulos) e DM Sans (corpo)",
    "Montserrat (títulos em caixa alta/negrito) e Open Sans (corpo)",
    "Playfair Display (títulos elegantes serifados) e Lato (corpo)"
]

# Padrões de textura sutil via CSS puro (substituem gradientes artificiais)
TEXTURAS_FUNDO = [
    "Fundo 100% sólido e limpo, alternando apenas entre a cor principal e a cor secundária de seção.",
    "Fundo sólido com padrão sutil de pontos (radial-gradient de 1px em opacidade 5%) apenas no Hero.",
    "Fundo sólido com linhas de grade arquitetônica muito sutis (opacidade 4%) no fundo do Hero."
]

def obter_direcao_arte(cliente):
    """Define paleta 100% sólida (sem gradientes) conforme o nicho real do cliente."""
    ramo = cliente.get("ramo", "").lower()
    
    if any(k in ramo for k in ["restaurant", "food", "pizza", "burger", "bar", "cafe"]):
        return {
            "tema": "Fundo principal escuro sólido (#121212), seções alternadas em carvão sólido (#1C1C1E), cartões em #242426 com borda #333333. Cor de destaque primária: Vermelho Sólido (#DC2626) e secundária Âmbar Sólido (#D97706).",
            "clima": "Artesanal, gastronômico, autêntico e direto"
        }
    elif any(k in ramo for k in ["clinic", "dentist", "pilates", "fisio", "saude", "veterinary", "vet"]):
        return {
            "tema": "Fundo principal Off-White/Creme limpo (#FAF9F6 ou #FFFFFF), seções alternadas em Cinza Pedra suave (#F1F5F9), cartões brancos com borda fina (#E2E8F0). Cor de destaque: Verde Esmeralda Sólido (#0F766E) ou Azul Petróleo Sólido (#0369A1).",
            "clima": "Clínico, humano, editorial, limpo e confiável"
        }
    elif any(k in ramo for k in ["car", "auto", "mecanica", "barber", "hair", "estetica"]):
        return {
            "tema": "Fundo principal Preto Fosco sólido (#0A0A0A), seções alternadas em Grafite sólido (#171717), bordas metálicas (#262626). Cor de destaque: Vermelho Corrida Sólido (#E11D48) ou Laranja Industrial Sólido (#EA580C).",
            "clima": "Técnico, robusto, masculino e de oficina/estúdio premium"
        }
    else:
        return {
            "tema": "Fundo principal Branco Puro (#FFFFFF), seções alternadas em Azul Marinho Sólido (#0F172A) com texto branco e Cinza Claro (#F8FAFC). Cor de destaque: Azul Royal Sólido (#1D4ED8).",
            "clima": "Corporativo contemporâneo, sólido e de alta credibilidade"
        }

def descobrir_modelos_disponiveis():
    """Retorna os modelos de texto mais rápidos e ativos na conta."""
    modelos_preferenciais = [
        "gemini-3.5-flash",
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3-flash-preview"
    ]
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
            modelos_conta = [m.get("name", "").replace("models/", "") for m in dados.get("models", [])]
            validos = [m for m in modelos_preferenciais if m in modelos_conta]
            return validos if validos else ["gemini-flash-latest"]
    except Exception:
        return ["gemini-flash-latest"]

def extrair_html_limpo(texto):
    """Remove blocos markdown e qualquer texto antes/depois do código HTML."""
    conteudo = texto.strip()
    if "```html" in conteudo:
        conteudo = conteudo.split("```html")[1].split("```")[0]
    elif "```" in conteudo:
        conteudo = conteudo.split("```")[1].split("```")[0]
    return conteudo.strip()

def chamar_gemini_nativo(prompt, modelo):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9
        }
    }
    dados_json = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=dados_json,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        resultado = json.loads(resp.read().decode("utf-8"))
        return resultado["candidates"][0]["content"]["parts"][0]["text"]

def gerar_landing_page(cliente, modelos):
    nome_pasta = cliente.get("slug", cliente.get("nome", "cliente").lower().replace(" ", "-"))
    
    arquitetura = random.choice(ARQUITETURAS_LAYOUT)
    fonte = random.choice(TIPOGRAFIAS)
    textura = random.choice(TEXTURAS_FUNDO)
    direcao_arte = obter_direcao_arte(cliente)

    prompt = f"""
Você é um Diretor de Arte e Web Designer Sênior especializado em sites autorais de alta conversão.
Crie uma Landing Page ÚNICA, com aparência de agência boutique humana (ZERO cara de template genérico de IA) para o cliente abaixo:

DADOS DO CLIENTE:
{json.dumps(cliente, indent=2, ensure_ascii=False)}

DIREÇÃO DE ARTE OBRIGATÓRIA:
- Arquitetura de Layout: {arquitetura['nome']} -> {arquitetura['instrucao']}
- Paleta de Cores Sólidas: {direcao_arte['tema']}
- Acabamento de Fundo: {textura}
- Atmosfera Visual: {direcao_arte['clima']}
- Tipografia (importe via Google Fonts no <head>): {fonte}

REGRAS VISUAIS ESTRITAS (PROIBIÇÕES):
1. PROIBIDO USAR GRADIENTES DE FUNDO OU DE TEXTO: NÃO use classes como `bg-gradient-to-r`, `bg-gradient-to-b`, `from-*`, `via-*`, `to-*` ou `bg-clip-text`. Todo fundo de seção, botão, card e badge DEVE ser cor sólida hexadecimal/Tailwind puro.
2. PROIBIDO EFEITOS NEON / GLOW ARTIFICIAL: Não use sombras coloridas brilhantes (`shadow-purple-500/50`, `blur-3xl` decorativo flutuante, etc.). Use contraste tipográfico, espaçamento generoso e bordas nítidas (`border`).
3. Botões devem ter cor sólida de alto contraste com hover sólido (ex: escurecer ligeiramente a cor no hover), sem degradês.

REQUISITOS TÉCNICOS:
1. HTML5 semântico com Tailwind CSS via CDN (<script src="https://cdn.tailwindcss.com"></script>).
2. Importe as fontes do Google Fonts escolhidas e aplique-as nos títulos e textos.
3. Use FontAwesome via CDN para ícones e botões de WhatsApp funcionais (link https://wa.me/{cliente.get('whatsapp', '')}).
4. Crie uma copy persuasiva adaptada especificamente à cidade ({cliente.get('cidade', '')}) e ao ramo do negócio, evitando clichês genéricos.
5. Inclua botão flutuante sólido de WhatsApp no canto inferior direito e FAQ (Perguntas Frequentes) interativo usando tags <details>/<summary>.

ATENÇÃO EXTREMA:
Retorne EXCLUSIVAMENTE o código HTML5 puro.
NÃO escreva nenhuma introdução, explicação ou blocos ```html.
Comece exatamente com <!DOCTYPE html> e termine com </html>.
"""

    for modelo in modelos:
        for tentativa in range(1, 4):
            try:
                print(f"  -> [{arquitetura['nome']}] Gerando '{nome_pasta}' via {modelo}...")
                texto_bruto = chamar_gemini_nativo(prompt, modelo)
                html_limpo = extrair_html_limpo(texto_bruto)
                
                pasta_saida = os.path.join(PASTA_DESTINO_SITES, nome_pasta)
                os.makedirs(pasta_saida, exist_ok=True)
                caminho_final = os.path.join(pasta_saida, "index.html")
                
                with open(caminho_final, "w", encoding="utf-8") as f:
                    f.write(html_limpo)
                
                print(f"  [OK] {caminho_final} salvo com sucesso!")
                return True
                
            except urllib.error.HTTPError as e:
                erro_detalhe = e.read().decode("utf-8", errors="ignore")
                print(f"  [AVISO HTTP {e.code}] {erro_detalhe[:120]}")
                if e.code in (400, 401, 403, 404):
                    break
                time.sleep(5)
            except Exception as e:
                print(f"  [AVISO] {e} - Retentando em 5s...")
                time.sleep(5)

    print(f"  [ERRO] Falha ao gerar '{nome_pasta}'.")
    return False

def main():
    print("=" * 65)
    print(" GERADOR DE LANDING PAGES EM LOTE (DESIGN EDITORIAL SÓLIDO)")
    print("=" * 65)

    if not API_KEY:
        print("ERRO: A variavel GEMINI_API_KEY nao foi encontrada!")
        print("Defina a chave no 'rodar-lote.bat' antes de executar.")
        return

    modelos = descobrir_modelos_disponiveis()
    print(f"Modelos ativos selecionados: {modelos}\n")

    if not os.path.exists("clientes.json"):
        print("ERRO: Arquivo 'clientes.json' nao encontrado!")
        return

    with open("clientes.json", "r", encoding="utf-8") as f:
        clientes = json.load(f)

    os.makedirs(PASTA_DESTINO_SITES, exist_ok=True)

    for i, cliente in enumerate(clientes, start=1):
        print(f"[{i}/{len(clientes)}] Processando: {cliente.get('nome', 'Cliente')}")
        gerar_landing_page(cliente, modelos)
        time.sleep(2)

    print("\n" + "=" * 65)
    print(f" PROCESSO CONCLUIDO! Sites salvos na pasta '{PASTA_DESTINO_SITES}/'.")
    print("=" * 65)

if __name__ == "__main__":
    main()