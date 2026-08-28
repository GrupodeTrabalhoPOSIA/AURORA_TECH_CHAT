# Banco Supabase

O backend usa o Postgres do Supabase com a extensão `pgvector`. O React não acessa o banco diretamente.

## Aplicar a estrutura

1. Crie um projeto no Supabase.
2. Abra **SQL Editor** no painel.
3. Copie e execute `migrations/001_aurora_vector_store.sql`.
4. Configure `SUPABASE_URL` e `SUPABASE_SECRET_KEY` no ambiente do backend.

A migração pode ser executada novamente sem recriar tabelas ou índices. Ela cria duas tabelas, a função transacional de indexação e a função de busca por similaridade cosseno.

O tipo `vector(384)` corresponde ao modelo padrão `paraphrase-multilingual-MiniLM-L12-v2`. Se o modelo de embeddings for trocado por outro com dimensão diferente, uma nova migração deverá alterar a coluna e as assinaturas das funções antes de reindexar os documentos.

## Segurança

As tabelas usam RLS e não concedem acesso aos papéis `anon` e `authenticated`. A chave secreta, que possui acesso elevado, deve existir somente no backend e nas variáveis secretas do serviço de hospedagem.

## Reversão

O script `rollback/001_aurora_vector_store.sql` remove as funções, os documentos e todos os embeddings. Use-o apenas quando a perda desses dados for intencional.
