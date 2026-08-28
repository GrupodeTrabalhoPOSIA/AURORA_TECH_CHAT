const suggestions = [
  'O que é a Aurora Tech?',
  'Quais serviços a empresa oferece?',
  'Como posso entrar em contato?',
];

function ChatPage() {
  return (
    <section className="chat-page" aria-labelledby="chat-title">
      <div className="chat-welcome">
        <span className="eyebrow">Conhecimento que conversa</span>
        <h1 id="chat-title">Olá! Sou o assistente da Aurora Tech.</h1>
        <p>
          Faça uma pergunta sobre a empresa. Minhas respostas serão baseadas nos
          documentos cadastrados na base de conhecimento.
        </p>

        <div className="suggestion-list" aria-label="Sugestões de perguntas">
          {suggestions.map((suggestion) => (
            <button className="suggestion-card" type="button" key={suggestion} disabled>
              <span>{suggestion}</span>
              <span aria-hidden="true">↗</span>
            </button>
          ))}
        </div>
      </div>

      <form className="composer" aria-label="Enviar uma pergunta">
        <label className="sr-only" htmlFor="chat-message">
          Sua pergunta
        </label>
        <textarea
          id="chat-message"
          name="message"
          rows={1}
          placeholder="Digite sua pergunta sobre a Aurora Tech…"
          disabled
        />
        <button type="submit" disabled>
          Enviar
        </button>
      </form>

      <p className="development-note">
        A interação do chat será habilitada nos próximos ciclos.
      </p>
    </section>
  );
}

export default ChatPage;

