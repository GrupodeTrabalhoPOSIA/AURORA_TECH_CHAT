# Plano de Implementação — Aurora Tech Chatbot

**Base:** [ESPECIFICACAO.md](./ESPECIFICACAO.md)  
**Status geral:** Em andamento — ciclos 01 e 02 concluídos  
**Estratégia:** ciclos curtos alternando entre backend e frontend

## 1. Objetivo do plano

Implementar o MVP do Aurora Tech Chatbot de forma incremental. Cada ciclo deverá entregar uma pequena parte funcional, validada e registrada antes do início do próximo ciclo.

A ordem alterna entre backend e frontend para evitar que uma das camadas seja construída integralmente sem integração com a outra.

## 2. Regras obrigatórias para o agente

Ao executar este plano, o agente deverá:

1. trabalhar em apenas um ciclo por vez, salvo instrução diferente do usuário;
2. ler a especificação e este plano antes de alterar o código;
3. marcar cada tarefa concluída trocando `[ ]` por `[x]`;
4. marcar uma tarefa somente após implementar e validar o resultado;
5. não marcar tarefas que tenham sido apenas iniciadas;
6. marcar o ciclo no “Resumo dos ciclos” somente quando todos os itens obrigatórios e o critério de conclusão estiverem atendidos;
7. registrar, no “Diário de execução”, a data, o ciclo, um resumo e os comandos de validação executados;
8. registrar impedimentos sem marcar a tarefa como concluída;
9. preservar alterações existentes que não façam parte do ciclo;
10. manter os contratos entre frontend e backend compatíveis;
11. atualizar a documentação sempre que uma decisão técnica mudar;
12. encerrar cada ciclo informando claramente o que foi concluído e qual será o próximo ciclo.

### Formato para registrar um impedimento

```markdown
- Ciclo: 00
- Tarefa bloqueada: descrição
- Motivo: descrição objetiva
- Ação necessária: decisão, acesso ou recurso necessário
```

## 3. Resumo dos ciclos

- [x] Ciclo 01 — Backend: fundação da API
- [x] Ciclo 02 — Frontend: fundação da interface
- [x] Ciclo 03 — Backend: contratos e configurações
- [x] Ciclo 04 — Frontend: estrutura visual e comunicação com a API
- [ ] Ciclo 05 — Backend: leitura e divisão de documentos
- [ ] Ciclo 06 — Frontend: tela da base de conhecimento
- [ ] Ciclo 07 — Backend: embeddings, ChromaDB e endpoints de documentos
- [ ] Ciclo 08 — Frontend: integração da base de conhecimento
- [ ] Ciclo 09 — Backend: recuperação RAG e OpenRouter
- [ ] Ciclo 10 — Frontend: chat integrado
- [ ] Ciclo 11 — Backend: robustez, testes e avaliação RAG
- [ ] Ciclo 12 — Frontend: testes, responsividade e acabamento
- [ ] Validação final do MVP

## 4. Ciclos de implementação

## Ciclo 01 — Backend: fundação da API

**Objetivo:** criar uma API FastAPI mínima, executável localmente e pronta para receber os próximos módulos.

### Implementação

- [x] Criar a pasta `backend/` e a estrutura inicial de `backend/app/`.
- [x] Definir o gerenciamento de dependências Python em `pyproject.toml` ou `requirements.txt`.
- [x] Criar a aplicação FastAPI em `backend/app/main.py`.
- [x] Criar o endpoint `GET /api/v1/health` com resposta `{"status": "ok"}`.
- [x] Configurar CORS para o endereço local do frontend.
- [x] Criar `backend/.env.example` sem segredos reais.
- [x] Criar `.gitignore` para ambiente virtual, cache, `.env`, ChromaDB local e arquivos temporários.

### Validação

- [x] Iniciar o backend localmente sem erros.
- [x] Confirmar resposta HTTP 200 no endpoint de saúde.
- [x] Confirmar acesso à documentação Swagger.
- [x] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando uma instalação limpa conseguir iniciar a API e consultar o endpoint de saúde.

---

## Ciclo 02 — Frontend: fundação da interface

**Objetivo:** criar a aplicação React e confirmar sua execução local.

### Implementação

- [x] Criar `frontend/` com React, TypeScript e Vite.
- [x] Remover conteúdos de demonstração que não serão utilizados.
- [x] Criar a estrutura inicial de `components/`, `pages/`, `services/` e `types/`.
- [x] Criar o layout base da aplicação.
- [x] Adicionar navegação simples entre “Chat” e “Base de conhecimento”.
- [x] Criar `frontend/.env.example` com a URL pública da API.
- [x] Definir estilos globais mínimos e identidade inicial da Aurora Tech.

### Validação

- [x] Iniciar o frontend localmente sem erros.
- [x] Confirmar que as duas páginas podem ser acessadas.
- [x] Confirmar que o build de produção é gerado.
- [x] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando a aplicação React abrir no navegador, navegar entre as páginas e gerar um build válido.

---

## Ciclo 03 — Backend: contratos e configurações

**Objetivo:** definir os modelos e configurações compartilhados pelos recursos futuros.

### Implementação

- [x] Criar o módulo central de configurações do backend.
- [x] Ler configurações por variáveis de ambiente.
- [x] Validar a presença das configurações obrigatórias no momento apropriado.
- [x] Criar os modelos de requisição do chat: mensagem e histórico.
- [x] Criar os modelos de resposta: resposta, fonte e indicação de contexto.
- [x] Criar o formato padronizado de erro da API.
- [x] Definir limites de tamanho para mensagem, histórico e upload.
- [x] Documentar os contratos no Swagger com exemplos.

### Validação

- [x] Criar testes para validação dos modelos.
- [x] Confirmar rejeição de mensagem vazia e entrada acima do limite.
- [x] Confirmar que segredos não aparecem nos logs ou no Swagger.
- [x] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando os contratos do chat e as configurações estiverem tipados, documentados e testados.

---

## Ciclo 04 — Frontend: estrutura visual e comunicação com a API

**Objetivo:** preparar a interface para consumir o backend e representar os estados principais.

### Implementação

- [x] Criar os tipos TypeScript equivalentes aos contratos públicos da API.
- [x] Criar um cliente HTTP centralizado usando a URL definida no ambiente.
- [x] Criar um componente de estado da API na interface.
- [x] Consultar `GET /api/v1/health` ao carregar a aplicação ou quando solicitado.
- [x] Exibir estados de API disponível e indisponível.
- [x] Criar componentes visuais iniciais de mensagem, campo de texto, carregamento e erro.
- [x] Criar dados simulados somente para visualizar a conversa antes da integração real.

### Validação

- [x] Confirmar comunicação entre React e FastAPI.
- [x] Confirmar tratamento visual quando o backend estiver desligado.
- [x] Confirmar que a aplicação continua gerando build válido.
- [x] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando o frontend detectar a disponibilidade do backend e possuir os componentes básicos do chat.

---

## Ciclo 05 — Backend: leitura e divisão de documentos

**Objetivo:** transformar arquivos suportados em trechos prontos para receber embeddings.

### Implementação

- [ ] Criar uma interface comum para extração de texto.
- [ ] Implementar extração de TXT e Markdown.
- [ ] Implementar extração de PDF com preservação do número da página.
- [ ] Implementar extração de DOCX.
- [ ] Validar extensão, MIME type e tamanho do arquivo.
- [ ] Calcular hash do conteúdo para identificar duplicidade.
- [ ] Implementar normalização do texto.
- [ ] Implementar divisão em trechos com tamanho e sobreposição configuráveis.
- [ ] Preservar metadados de nome, página, posição e tipo de arquivo.
- [ ] Rejeitar documentos vazios ou sem texto extraível.

### Validação

- [ ] Testar extração de cada formato suportado.
- [ ] Testar chunking, sobreposição e metadados.
- [ ] Testar arquivo inválido, vazio e duplicado.
- [ ] Adicionar arquivos pequenos de teste sem dados sensíveis.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando todos os formatos suportados forem convertidos de maneira previsível em trechos testados.

---

## Ciclo 06 — Frontend: tela da base de conhecimento

**Objetivo:** construir a interface de documentos de acordo com o contrato planejado.

### Implementação

- [ ] Criar o seletor de arquivos com formatos aceitos visíveis.
- [ ] Criar o botão de envio e seu estado de carregamento.
- [ ] Criar a lista visual de documentos.
- [ ] Exibir nome, tipo e quantidade de trechos.
- [ ] Criar a ação de remoção com confirmação.
- [ ] Criar estados de lista vazia, sucesso e erro.
- [ ] Usar respostas simuladas compatíveis com o contrato enquanto os endpoints ainda não estiverem disponíveis.

### Validação

- [ ] Testar seleção de formato aceito e rejeitado.
- [ ] Testar estados de carregamento, lista vazia e erro.
- [ ] Testar visualmente em largura de celular e desktop.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando todos os estados da base de conhecimento puderem ser demonstrados com dados simulados.

---

## Ciclo 07 — Backend: embeddings, ChromaDB e endpoints de documentos

**Objetivo:** indexar, consultar administrativamente e remover documentos da base vetorial.

### Implementação

- [ ] Configurar o modelo local de embeddings.
- [ ] Criar um serviço de embeddings isolado das rotas HTTP.
- [ ] Configurar persistência local do ChromaDB.
- [ ] Criar uma coleção para os documentos da Aurora Tech.
- [ ] Salvar texto, embedding e metadados de cada trecho.
- [ ] Evitar indexação duplicada pelo hash do documento.
- [ ] Implementar `POST /api/v1/documents`.
- [ ] Implementar `GET /api/v1/documents`.
- [ ] Implementar `DELETE /api/v1/documents/{document_id}`.
- [ ] Garantir que a remoção exclua todos os trechos do documento.

### Validação

- [ ] Testar upload e indexação de um documento válido.
- [ ] Reiniciar o backend e confirmar a persistência dos vetores.
- [ ] Testar listagem e rejeição de duplicidade.
- [ ] Testar remoção completa do documento.
- [ ] Confirmar os contratos no Swagger.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando um documento puder ser indexado, listado e removido por meio da API, com persistência após reinício.

---

## Ciclo 08 — Frontend: integração da base de conhecimento

**Objetivo:** substituir os dados simulados da tela de documentos pela API real.

### Implementação

- [ ] Criar funções do cliente para enviar, listar e remover documentos.
- [ ] Integrar o formulário de upload com `POST /api/v1/documents`.
- [ ] Integrar a lista com `GET /api/v1/documents`.
- [ ] Integrar a remoção com `DELETE /api/v1/documents/{document_id}`.
- [ ] Atualizar a lista após envio ou remoção.
- [ ] Exibir mensagens retornadas pelo backend.
- [ ] Remover os dados simulados da tela de documentos.

### Validação

- [ ] Executar o fluxo completo de upload pela interface.
- [ ] Confirmar que o documento continua listado após recarregar a página.
- [ ] Executar o fluxo completo de remoção.
- [ ] Confirmar tratamento de arquivo inválido e duplicado.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando a base vetorial puder ser gerenciada integralmente pelo frontend.

---

## Ciclo 09 — Backend: recuperação RAG e OpenRouter

**Objetivo:** responder perguntas usando os documentos indexados e o modelo configurado na OpenRouter.

### Implementação

- [ ] Gerar o embedding da pergunta com o mesmo modelo usado na indexação.
- [ ] Consultar no ChromaDB a quantidade configurada de trechos.
- [ ] Aplicar limiar de relevância e limitar o contexto.
- [ ] Criar o prompt de sistema da Aurora Tech.
- [ ] Incluir contexto, pergunta e histórico curto no prompt.
- [ ] Criar um cliente isolado para a OpenRouter usando `httpx`.
- [ ] Configurar modelo, chave, timeout e cabeçalhos necessários.
- [ ] Implementar `POST /api/v1/chat`.
- [ ] Retornar resposta, fontes e `has_context`.
- [ ] Responder sem chamar o modelo quando não houver contexto suficiente, se essa for a estratégia escolhida.
- [ ] Tratar chave inválida, timeout, limite e modelo indisponível.

### Validação

- [ ] Testar a recuperação de um trecho conhecido.
- [ ] Testar a montagem do prompt sem expor instruções ou segredos.
- [ ] Testar o endpoint com cliente OpenRouter simulado.
- [ ] Executar ao menos uma consulta real com uma chave fornecida pelo ambiente.
- [ ] Testar pergunta sem contexto e fontes vazias.
- [ ] Registrar os comandos executados no diário sem registrar a chave.

### Critério de conclusão

O ciclo estará concluído quando o endpoint responder uma pergunta fundamentada, citar fontes e recusar adequadamente uma pergunta sem contexto.

---

## Ciclo 10 — Frontend: chat integrado

**Objetivo:** substituir os dados simulados pelo fluxo real do chatbot.

### Implementação

- [ ] Criar a função do cliente para `POST /api/v1/chat`.
- [ ] Enviar mensagem e histórico curto ao backend.
- [ ] Adicionar imediatamente a mensagem do usuário à conversa.
- [ ] Exibir carregamento enquanto aguarda a resposta.
- [ ] Exibir a resposta do assistente.
- [ ] Exibir as fontes associadas à resposta.
- [ ] Exibir o estado de ausência de contexto.
- [ ] Implementar ação para limpar a conversa.
- [ ] Limitar o histórico enviado conforme a especificação.
- [ ] Remover os dados simulados do chat.

### Validação

- [ ] Testar uma pergunta com resposta presente na base.
- [ ] Testar uma pergunta sem resposta na base.
- [ ] Testar erro e timeout do backend.
- [ ] Confirmar que o histórico permanece apenas no frontend.
- [ ] Confirmar que limpar a conversa remove o histórico visível.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando o usuário puder conversar com o chatbot real, visualizar fontes e receber erros compreensíveis.

---

## Ciclo 11 — Backend: robustez, testes e avaliação RAG

**Objetivo:** consolidar a qualidade do backend e medir o comportamento do RAG.

### Implementação

- [ ] Revisar validação de todas as entradas.
- [ ] Garantir que a chave da OpenRouter nunca seja registrada.
- [ ] Padronizar os erros retornados pela API.
- [ ] Adicionar logs essenciais sem conteúdo sensível.
- [ ] Completar os testes unitários dos serviços.
- [ ] Completar os testes dos endpoints.
- [ ] Criar uma pequena base de perguntas esperadas.
- [ ] Avaliar recuperação de fontes e recusa sem contexto.
- [ ] Ajustar tamanho dos trechos, sobreposição, `top_k` e limiar com base nos resultados.
- [ ] Documentar os valores finais escolhidos.

### Validação

- [ ] Executar toda a suíte do backend sem falhas.
- [ ] Executar a avaliação RAG e registrar os resultados.
- [ ] Confirmar que nenhum segredo está versionado.
- [ ] Confirmar inicialização com base vetorial vazia.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando os testes passarem, os erros estiverem padronizados e o RAG tiver sido avaliado com perguntas conhecidas.

---

## Ciclo 12 — Frontend: testes, responsividade e acabamento

**Objetivo:** finalizar a experiência do usuário e garantir estabilidade da interface.

### Implementação

- [ ] Revisar a identidade visual da Aurora Tech.
- [ ] Ajustar o layout para celular e desktop.
- [ ] Garantir navegação por teclado nos controles principais.
- [ ] Adicionar rótulos acessíveis aos campos e botões.
- [ ] Sanitizar qualquer Markdown renderizado.
- [ ] Completar testes dos componentes do chat.
- [ ] Completar testes da tela de documentos.
- [ ] Completar testes de integração com API simulada.
- [ ] Remover código, estilos e dependências não utilizados.

### Validação

- [ ] Executar todos os testes do frontend sem falhas.
- [ ] Executar lint e verificação de tipos.
- [ ] Gerar o build de produção.
- [ ] Verificar manualmente as principais larguras de tela.
- [ ] Registrar os comandos executados no diário.

### Critério de conclusão

O ciclo estará concluído quando testes, tipagem e build passarem e os fluxos principais funcionarem em celular e desktop.

## 5. Validação final do MVP

Esta etapa somente poderá ser marcada após a conclusão dos 12 ciclos.

- [ ] Preparar uma instalação limpa do projeto.
- [ ] Seguir o README sem usar configurações não documentadas.
- [ ] Iniciar backend e frontend.
- [ ] Confirmar o endpoint de saúde.
- [ ] Enviar um documento de cada formato suportado.
- [ ] Confirmar persistência dos documentos após reinício.
- [ ] Fazer uma pergunta respondida pela base.
- [ ] Confirmar a apresentação das fontes corretas.
- [ ] Fazer uma pergunta sem resposta na base.
- [ ] Confirmar que o chatbot não inventa uma resposta.
- [ ] Remover um documento e confirmar que ele deixa de ser consultado.
- [ ] Executar testes, lint, tipagem e builds.
- [ ] Revisar `.gitignore`, `.env.example`, README e especificação.
- [ ] Confirmar que nenhuma chave ou dado sensível está versionado.
- [ ] Marcar “Validação final do MVP” no resumo dos ciclos.

## 6. Definição geral de pronto

Uma tarefa somente pode ser marcada como concluída quando:

- o código correspondente foi implementado;
- o comportamento foi testado;
- os testes relacionados passam;
- não existem erros conhecidos ocultados;
- os contratos continuam compatíveis;
- a documentação afetada foi atualizada;
- a alteração não incluiu segredos;
- o resultado foi registrado no diário.

## 7. Diário de execução

O agente deverá acrescentar uma entrada ao final desta seção depois de cada ciclo.

### Modelo de entrada

```markdown
### AAAA-MM-DD — Ciclo 00

- Status: concluído | parcial | bloqueado
- Implementado: resumo curto
- Arquivos principais: lista de caminhos
- Validações: comandos executados e resultados
- Pendências: nenhuma ou lista objetiva
- Próximo ciclo: Ciclo 00 — Nome
```

<!-- Acrescentar novas entradas abaixo desta linha. -->

### 2026-08-27 — Ciclo 01

- Status: concluído
- Implementado: fundação FastAPI, roteamento versionado, endpoint de saúde, CORS, configuração de ambiente, dependências e teste do endpoint.
- Arquivos principais: `.gitignore`, `backend/pyproject.toml`, `backend/.env.example`, `backend/app/main.py`, `backend/app/api/v1/router.py`, `backend/app/api/v1/routes/health.py`, `backend/tests/test_health.py`.
- Validações: `python -m pytest -q` — 1 teste aprovado; Uvicorn iniciado em `127.0.0.1:8000`; `GET /api/v1/health` — HTTP 200; `GET /docs` — HTTP 200; OpenAPI carregado com o título esperado.
- Pendências: nenhuma no Ciclo 01. O comando global `python` aponta para uma instalação ausente; foi usado o runtime Python fornecido pelo ambiente para criar `backend/.venv`.
- Próximo ciclo: Ciclo 02 — Frontend: fundação da interface

### 2026-08-27 — Ciclo 02

- Status: concluído
- Implementado: fundação React 19 com TypeScript e Vite, carregamento sob demanda das páginas, navegação entre Chat e Base de conhecimento, layout responsivo, identidade visual inicial e configurações de ambiente.
- Arquivos principais: `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.app.json`, `frontend/src/App.tsx`, `frontend/src/components/AppShell.tsx`, `frontend/src/pages/ChatPage.tsx`, `frontend/src/pages/KnowledgeBasePage.tsx`, `frontend/src/styles/global.css`.
- Validações: `npm run typecheck` — aprovado; `npm run build` — aprovado, 34 módulos transformados; Vite iniciado em `127.0.0.1:5173`; página inicial — HTTP 200 e título correto; navegação de Chat e Base de conhecimento confirmada na composição da aplicação.
- Pendências: nenhuma no Ciclo 02. A interação dos controles permanece desabilitada intencionalmente até os ciclos de integração correspondentes.
- Próximo ciclo: Ciclo 03 — Backend: contratos e configurações

### 2026-08-27 — Ciclo 03

- Status: concluído
- Implementado: configurações tipadas com Pydantic Settings, chave OpenRouter protegida e validada sob demanda, limites do MVP, contratos do chat, erros padronizados e endpoint provisório documentado no OpenAPI.
- Arquivos principais: `BACKEND/app/core/config.py`, `BACKEND/app/core/errors.py`, `BACKEND/app/models/chat.py`, `BACKEND/app/models/errors.py`, `BACKEND/app/api/v1/routes/chat.py`, `BACKEND/tests/test_chat_contract.py`, `BACKEND/tests/test_config.py`.
- Validações: `python -m pytest -q` — 10 testes aprovados; validação de mensagem vazia, mensagem longa, histórico longo, proteção do segredo e schemas do chat no OpenAPI.
- Pendências: o endpoint `/chat` retorna `CHAT_NOT_IMPLEMENTED` intencionalmente até o Ciclo 09.
- Próximo ciclo: Ciclo 04 — Frontend: estrutura visual e comunicação com a API

### 2026-08-27 — Ciclo 04

- Status: concluído
- Implementado: contratos TypeScript, cliente HTTP centralizado, configuração pública da API, monitor de saúde com nova tentativa, estados online/offline e componentes visuais reutilizáveis do chat com dados simulados.
- Arquivos principais: `FRONTEND/src/types/api.ts`, `FRONTEND/src/services/apiClient.ts`, `FRONTEND/src/features/health/`, `FRONTEND/src/features/chat/`, `FRONTEND/src/pages/ChatPage.tsx`, `FRONTEND/src/styles/global.css`.
- Validações: `npm run typecheck` — aprovado; `npm run build` — aprovado com 46 módulos; chamada no formato do frontend para `/api/v1/health` — HTTP 200; preflight CORS — HTTP 200 com origem `http://localhost:5173`.
- Pendências: dados do chat permanecem simulados por desenho do plano até o Ciclo 10.
- Próximo ciclo: Ciclo 05 — Backend: leitura e divisão de documentos
