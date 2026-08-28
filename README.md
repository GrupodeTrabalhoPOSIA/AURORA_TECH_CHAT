# Aurora Tech Chatbot

MVP acadêmico de um chatbot RAG para responder perguntas sobre a empresa fictícia Aurora Tech. Os documentos são transformados em embeddings locais, persistidos no ChromaDB e recuperados antes de cada resposta gerada por um modelo acessado pela API do OpenRouter.

O projeto não possui autenticação, perfis de usuário nem persistência de conversas. O histórico curto existe somente na página aberta no navegador.

## Arquitetura

```text
React + TypeScript
        │ HTTP /api/v1
        ▼
FastAPI ──► extração e chunking ──► Sentence Transformers ──► ChromaDB local
   │                                                        │
   └──────── pergunta + contexto recuperado ◄───────────────┘
                         │
                         ▼
                  OpenRouter / LLM
```

## Requisitos

- Python 3.11 a 3.14;
- Node.js 20.19+ ou 22.12+;
- uma chave da OpenRouter para gerar respostas;
- cerca de 2 GB livres para dependências e cache do modelo de embeddings.

Na primeira execução, o Sentence Transformers baixa o modelo multilíngue configurado. Depois disso, os embeddings são gerados localmente.

## Instalação do backend

No PowerShell, a partir da raiz do projeto:

```powershell
cd BACKEND
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Edite `BACKEND/.env` e preencha:

```dotenv
OPENROUTER_API_KEY=sua-chave-local
```

Não versione esse arquivo. A aplicação inicia e gerencia documentos sem a chave, mas retorna `MODEL_NOT_CONFIGURED` quando uma pergunta encontra contexto e precisa chamar o modelo.

Inicie a API:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Verificações úteis:

- saúde: `http://localhost:8000/api/v1/health`;
- Swagger: `http://localhost:8000/docs`;
- ReDoc: `http://localhost:8000/redoc`.

## Instalação do frontend

Em outro terminal, a partir da raiz:

```powershell
cd FRONTEND
npm ci
Copy-Item .env.example .env
npm run dev
```

Acesse `http://localhost:5173`. Se o backend usar outra porta, altere `VITE_API_URL` em `FRONTEND/.env`.

## Uso

1. Abra **Base de conhecimento**.
2. Adicione arquivos PDF, TXT, Markdown ou DOCX, com até 10 MB.
3. Volte ao **Chat** e faça uma pergunta contida nos documentos.
4. Confira as fontes exibidas abaixo da resposta.

Quando nenhum trecho atinge o limiar de relevância, a API recusa a pergunta sem chamar o modelo. Documentos duplicados são identificados pelo hash do conteúdo.

## Endpoints principais

| Método | Rota | Função |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Verifica a API |
| `POST` | `/api/v1/documents` | Processa e indexa um documento |
| `GET` | `/api/v1/documents` | Lista documentos indexados |
| `DELETE` | `/api/v1/documents/{id}` | Remove documento e chunks |
| `POST` | `/api/v1/chat` | Recupera contexto e responde |

## Configuração RAG adotada

- embeddings: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`;
- chunks de 700 caracteres, com sobreposição de 100;
- até 5 trechos por busca;
- relevância mínima de 0,35;
- contexto máximo de 6.000 caracteres;
- modelo OpenRouter padrão: `openai/gpt-4o-mini`.

Todos esses valores podem ser alterados em `BACKEND/.env`. A justificativa e o conjunto de perguntas estão em `BACKEND/evaluation/`.

## Testes e qualidade

Backend:

```powershell
cd BACKEND
python -m pytest -q
$env:HF_HUB_OFFLINE='1'
python evaluation/evaluate_rag.py
```

Remova `HF_HUB_OFFLINE` se o modelo ainda precisar ser baixado.

Frontend:

```powershell
cd FRONTEND
npm test
npm run lint
npm run typecheck
npm run build
```

## Dados e segurança

- `.env`, ambientes virtuais, `node_modules`, builds e banco Chroma local são ignorados pelo Git;
- a chave OpenRouter permanece apenas no backend e nunca é enviada ao React;
- logs registram método, rota, status e duração, sem corpos ou cabeçalhos;
- respostas Markdown são renderizadas com sanitização;
- documentos e embeddings ficam em `BACKEND/data/chroma` por padrão.

Consulte [ESPECIFICACAO.md](./ESPECIFICACAO.md) para o escopo e [PLANO_IMPLEMENTACAO.md](./PLANO_IMPLEMENTACAO.md) para o histórico dos ciclos.
