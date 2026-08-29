# Banco Supabase

O backend usa o Postgres do Supabase com a extensão `pgvector`. O React não acessa o banco diretamente.

## Aplicar a estrutura

1. Crie um projeto no Supabase.
2. Abra **SQL Editor** no painel.
3. Copie e execute `migrations/001_aurora_vector_store.sql`.
4. Abra **Connect**, selecione **Session pooler** e copie a URI PostgreSQL.
5. Substitua `[YOUR-PASSWORD]` pela senha do banco e configure a URI como `SUPABASE_DB_URL` no backend.

A URI de Session Pooler usa o formato abaixo e a porta `5432`:

```dotenv
SUPABASE_DB_URL=postgresql://postgres.PROJECT_REF:SENHA@aws-0-REGIAO.pooler.supabase.com:5432/postgres
```

Se a senha tiver caracteres reservados de URL, codifique-os antes de montar a URI. `SUPABASE_POOL_MIN_SIZE` e `SUPABASE_POOL_MAX_SIZE` controlam quantas sessões o processo mantém; os padrões acadêmicos são 1 e 5.

A migração pode ser executada novamente sem recriar tabelas ou índices. Ela cria duas tabelas, a função transacional de indexação e a função de busca por similaridade cosseno.

O tipo `vector(384)` corresponde à dimensão solicitada ao modelo padrão `openai/text-embedding-3-small` via OpenRouter. Trocar o modelo exige reindexar os documentos, mesmo mantendo 384 dimensões. Se a dimensão também mudar, uma nova migração deverá alterar a coluna e as assinaturas das funções antes da reindexação.

## Segurança

As tabelas usam RLS e não concedem acesso aos papéis `anon` e `authenticated`. A URI contém a senha do Postgres e deve existir somente no backend e nas variáveis secretas do serviço de hospedagem. O frontend não usa credenciais Supabase.

## Reversão

O script `rollback/001_aurora_vector_store.sql` remove as funções, os documentos e todos os embeddings. Use-o apenas quando a perda desses dados for intencional.
