import type { ChatMessageView } from '@/features/chat/types/chat';

interface ChatMessageProps {
  message: ChatMessageView;
}

function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === 'assistant';

  return (
    <article className={`chat-message chat-message--${message.role}`}>
      <div className="chat-message__avatar" aria-hidden="true">
        {isAssistant ? 'A' : 'Você'}
      </div>
      <div className="chat-message__body">
        <strong>{isAssistant ? 'Aurora' : 'Você'}</strong>
        <p>{message.content}</p>
        {message.sources && message.sources.length > 0 ? (
          <div className="source-list" aria-label="Fontes da resposta">
            {message.sources.map((source) => (
              <span className="source-chip" key={`${source.document_id}-${source.page ?? 0}`}>
                {source.document_name}
                {source.page ? ` · pág. ${source.page}` : ''}
              </span>
            ))}
          </div>
        ) : null}
      </div>
    </article>
  );
}

export default ChatMessage;

