# 🚀 Automação de Captação de Leads & Geração de Landing Pages

Pipeline automatizada em Python puro (zero dependências externas) para prospectar estabelecimentos locais em todo o Brasil que ainda não possuem site próprio e gerar Landing Pages exclusivas, responsivas e focadas em conversão via WhatsApp utilizando a API do Google Gemini.

---

## 🎯 Como Funciona o Fluxo

1. **Captação & Filtragem Nacional (`captar_leads.py`):**
   * Consulta a base pública do **OpenStreetMap (Overpass API)** com fallback automático entre múltiplos servidores espelho.
   * Varre capitais e polos regionais do Brasil em nichos estratégicos (restaurantes, pizzarias, clínicas, dentistas, barbearias, oficinas automotivas, etc.).
   * Aplica o **Filtro de Oportunidade**: seleciona apenas empresas que possuem **WhatsApp/telefone válido** cadastrado (`+55`) e **não possuem site próprio** (ou utilizam apenas links de redes sociais).
   * Salva e formata os leads qualificados em `clientes.json`.

2. **Geração Autoral em Lote (`gerar_lote.py`):**
   * Lê os leads aprovados em `clientes.json`.
   * Aplica uma **Direção de Arte Dinâmica** sorteando arquiteturas de layout (*Split-Screen Editorial*, *Bento Grid*, *Minimalista Suíço*, *Conversão Direta*), combinações tipográficas do Google Fonts e paletas de cores sólidas adequadas ao nicho.
   * **Estética Anti-Template:** Bloqueia explicitamente o uso de gradientes artificiais (`bg-gradient-*`) e efeitos neon genéricos, priorizando contraste tipográfico, bordas nítidas e acabamento editorial.
   * Gera arquivos `index.html` autocontidos (HTML5 + Tailwind CSS via CDN + FontAwesome) organizados individualmente dentro da pasta `sites/<slug-do-cliente>/`.

---

## 📂 Estrutura de Arquivos

```text
Automacao-Sites/
├── captar_leads.py          # Script de extração e filtragem de leads no Brasil
├── gerar_lote.py            # Gerador de Landing Pages via Gemini API
├── clientes.json            # Base de leads qualificados pronta para geração
├── captar-leads.bat         # Atalho Windows: capta leads e abre clientes.json para revisão
├── rodar-lote.bat           # Atalho Windows: lê o .env e gera todas as páginas em /sites
├── pipeline-completa.bat    # Atalho Windows: executa captação + geração em sequência
├── .gitignore               # Protege a chave da API (.env) e ignora a pasta /sites
├── .env                     # (Local - Ignorado pelo Git) Armazena GEMINI_API_KEY
└── sites/                   # (Local - Ignorado pelo Git) Landing pages geradas
    └── nome-do-cliente/
        └── index.html
```

---

## ⚙️ Configuração e Instalação

### Pré-requisitos
* **Python 3.10+** instalado e adicionado ao PATH do sistema.
* Uma chave gratuita ou paga da **Google Gemini API** (obtida no Google AI Studio).
* *Nenhuma biblioteca externa (`pip install`) é necessária — o projeto utiliza 100% módulos nativos do Python.*

### Passo a Passo
1. Clone este repositório:
   ```bash
   git clone https://github.com/RaphinhaFilho/Automacao-Sites.git
   cd Automacao-Sites
   ```

2. Na raiz do projeto, crie um arquivo chamado **`.env`** e insira sua chave da API do Gemini:
   ```env
   GEMINI_API_KEY=SUA_CHAVE_AQUI
   ```
   *(Nota: O arquivo `.env` já está listado no `.gitignore` para evitar exposição acidental da chave).*

---

## 🖥️ Como Usar (Atalhos Windows)

* **Modo Revisão (Recomendado):**
  1. Dê duplo clique em **`captar-leads.bat`**. O script buscará novos leads pelo Brasil e abrirá automaticamente o arquivo `clientes.json`.
  2. Revise os dados, remova contatos indesejados ou personalize ofertas e salve (`Ctrl + S`).
  3. Dê duplo clique em **`rodar-lote.bat`** para gerar todas as Landing Pages na pasta `sites/`.

* **Modo Automático Completo:**
  * Dê duplo clique em **`pipeline-completa.bat`** para executar a captação e a geração dos sites em sequência sem interrupções.

---

## 🛡️ Segurança e Versionamento

* **Isolamento de Credenciais:** Os scripts `.bat` carregam a variável `GEMINI_API_KEY` dinamicamente a partir do arquivo local `.env` em tempo de execução.
* **Controle de Saída:** A pasta `sites/` é mantida fora do repositório remoto via `.gitignore`, mantendo o versionamento limpo e focado exclusivamente no código da automação.