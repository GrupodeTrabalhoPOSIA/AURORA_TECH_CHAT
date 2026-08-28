# Aurora Tech Chatbot

MVP acadêmico de um chatbot RAG para responder perguntas sobre a empresa fictícia Aurora Tech. Os documentos são transformados em embeddings locais, persistidos no Supabase com `pgvector` e recuperados antes de cada resposta gerada por um modelo acessado pela API do OpenRouter.

O projeto não possui autenticação, perfis de usuário nem persistência de conversas. O histórico curto existe somente na página aberta no navegador.

## Arquitetura

```text
React + TypeScript
        │ HTTP /api/v1
        ▼
FastAPI ──► extração e chunking ──► Sentence Transformers ──► Supabase / pgvector
   │                                                         │
   └──────── pergunta + contexto recuperado ◄────────────────┘
                         │
                         ▼
                  OpenRouter / LLM
```

## Requisitos

- Python 3.11 a 3.14;
- Node.js 20.19+ ou 22.12+;
- uma chave da OpenRouter para gerar respostas;
- um projeto Supabase para armazenar documentos e embeddings;
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

No painel do Supabase, abra **SQL Editor** e execute o arquivo `BACKEND/database/supabase/migrations/001_aurora_vector_store.sql`. Depois, edite `BACKEND/.env` e preencha:

```dotenv
OPENROUTER_API_KEY=sua-chave-local
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SECRET_KEY=sb_secret_sua-chave
```

Não versione esse arquivo. Use a chave **Secret** do Supabase, ou `SUPABASE_SERVICE_ROLE_KEY` apenas em projetos legados. Essas chaves ficam somente no backend. Sem as credenciais do banco, as rotas de documentos e chat retornam `DATABASE_NOT_CONFIGURED`; sem a chave OpenRouter, uma pergunta com contexto retorna `MODEL_NOT_CONFIGURED`.

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

## Inicialização rápida no Windows

Depois de instalar as dependências do backend e do frontend, execute na raiz:

```powershell
.\iniciar-local.bat
```

O arquivo prepara os `.env` ausentes, inicia backend e frontend em terminais separados e abre `http://localhost:5173`. Para verificar os pré-requisitos sem iniciar os servidores:

```powershell
.\iniciar-local.bat --check
```

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

O modelo padrão gera vetores com 384 dimensões, que corresponde ao tipo `vector(384)` da migração. Alterar o modelo exige uma nova migração e a reindexação dos documentos.

## Configuração em produção

No serviço que executa o FastAPI, configure como segredos:

```dotenv
OPENROUTER_API_KEY=...
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SECRET_KEY=sb_secret_...
FRONTEND_ORIGIN=https://aurora-tech-chat.vercel.app
```

Nenhuma variável do Supabase deve ser criada na Vercel do frontend. O React conversa somente com a API FastAPI.

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

- `.env`, ambientes virtuais, `node_modules` e builds são ignorados pelo Git;
- as chaves OpenRouter e Supabase permanecem apenas no backend e nunca são enviadas ao React;
- logs registram método, rota, status e duração, sem corpos ou cabeçalhos;
- respostas Markdown são renderizadas com sanitização;
- documentos e embeddings ficam no Postgres do Supabase, protegidos por RLS e sem acesso para os papéis públicos.

Consulte [ESPECIFICACAO.md](./ESPECIFICACAO.md) para o escopo e [PLANO_IMPLEMENTACAO.md](./PLANO_IMPLEMENTACAO.md) para o histórico dos ciclos.
