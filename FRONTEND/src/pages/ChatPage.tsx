import { ChatComposer, ChatLoading, ChatMessage } from '@/features/chat';
import type { ChatMessageView } from '@/features/chat';

const mockMessages: ChatMessageView[] = [
  {
    id: 'mock-user',
    role: 'user',
    content: 'Quais serviços a Aurora Tech oferece?',
  },
  {
    id: 'mock-assistant',
    role: 'assistant',
    content:
      'Quando a base estiver conectada, apresentarei aqui uma resposta fundamentada nos documentos da empresa.',
    sources: [
      {
        document_id: 'mock-source',
        document_name: 'apresentacao-aurora.pdf',
        page: 3,
      },
    ],
  },
];

function ChatPage() {
  return (
    <section className="chat-page" aria-labelledby="chat-title">
      <div className="chat-welcome chat-welcome--compact">
        <span className="eyebrow">Conhecimento que conversa</span>
        <h1 id="chat-title">Olá! Sou o assistente da Aurora Tech.</h1>
        <p>
          Faça uma pergunta sobre a empresa. Minhas respostas serão baseadas nos
          documentos cadastrados na base de conhecimento.
        </p>

      </div>

      <div className="chat-thread" aria-label="Prévia da conversa">
        {mockMessages.map((message) => (
          <ChatMessage message={message} key={message.id} />
        ))}
        <ChatLoading />
      </div>

      <ChatComposer disabled />

      <p className="development-note">
        A interação do chat será habilitada nos próximos ciclos.
      </p>
    </section>
  );
}

export default ChatPage;
