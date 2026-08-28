function KnowledgeBasePage() {
  return (
    <section className="knowledge-page" aria-labelledby="knowledge-title">
      <div className="page-heading">
        <span className="eyebrow">Conteúdo do assistente</span>
        <h1 id="knowledge-title">Base de conhecimento</h1>
        <p>
          Aqui serão adicionados os documentos usados pelo chatbot para responder às
          perguntas sobre a Aurora Tech.
        </p>
      </div>

      <div className="empty-state">
        <span className="empty-state__icon" aria-hidden="true">
          +
        </span>
        <h2>Nenhum documento adicionado</h2>
        <p>O envio e a listagem de documentos serão implementados nos próximos ciclos.</p>
        <button type="button" disabled>
          Adicionar documento
        </button>
      </div>
    </section>
  );
}

export default KnowledgeBasePage;

