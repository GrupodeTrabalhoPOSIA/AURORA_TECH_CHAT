interface ChatComposerProps {
  disabled?: boolean;
}

function ChatComposer({ disabled = false }: ChatComposerProps) {
  return (
    <form className="composer" aria-label="Enviar uma pergunta">
      <label className="sr-only" htmlFor="chat-message">
        Sua pergunta
      </label>
      <textarea
        id="chat-message"
        name="message"
        rows={1}
        placeholder="Digite sua pergunta sobre a Aurora Tech…"
        disabled={disabled}
      />
      <button type="submit" disabled={disabled}>
        Enviar
      </button>
    </form>
  );
}

export default ChatComposer;

