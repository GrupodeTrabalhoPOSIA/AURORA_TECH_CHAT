import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { sendChat } from '@/features/chat/api/chatApi';
import { ApiError } from '@/services/apiClient';
import type { ChatResponse } from '@/types';
import ChatPage from './ChatPage';

vi.mock('@/features/chat/api/chatApi', () => ({
  sendChat: vi.fn(),
}));

const contextualResponse: ChatResponse = {
  answer: 'A Aurora Tech oferece consultoria em transformação digital.',
  sources: [
    {
      document_id: 'document-1',
      document_name: 'servicos.pdf',
      page: 2,
    },
  ],
  has_context: true,
};

async function ask(question: string) {
  const user = userEvent.setup();
  await user.type(screen.getByLabelText('Sua pergunta'), question);
  await user.click(screen.getByRole('button', { name: 'Enviar' }));
  return user;
}

describe('ChatPage integrada', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('mostra a pergunta imediatamente e depois renderiza resposta e fonte', async () => {
    let resolveResponse: (response: ChatResponse) => void = () => undefined;
    vi.mocked(sendChat).mockReturnValue(
      new Promise((resolve) => {
        resolveResponse = resolve;
      }),
    );
    render(<ChatPage />);

    await ask('Quais serviços são oferecidos?');

    expect(screen.getByText('Quais serviços são oferecidos?')).toBeInTheDocument();
    expect(screen.getByText('Aurora está preparando uma resposta')).toBeInTheDocument();
    resolveResponse(contextualResponse);

    expect(await screen.findByText(contextualResponse.answer)).toBeInTheDocument();
    expect(screen.getByText('servicos.pdf · pág. 2')).toBeInTheDocument();
    expect(vi.mocked(sendChat).mock.calls[0]?.[0]).toEqual({
      message: 'Quais serviços são oferecidos?',
      history: [],
    });
  });

  it('envia apenas o histórico local anterior na pergunta seguinte', async () => {
    vi.mocked(sendChat).mockResolvedValue(contextualResponse);
    render(<ChatPage />);

    await ask('Primeira pergunta');
    await screen.findByText(contextualResponse.answer);
    await ask('Segunda pergunta');

    await waitFor(() => expect(sendChat).toHaveBeenCalledTimes(2));
    expect(vi.mocked(sendChat).mock.calls[1]?.[0]).toEqual({
      message: 'Segunda pergunta',
      history: [
        { role: 'user', content: 'Primeira pergunta' },
        { role: 'assistant', content: contextualResponse.answer },
      ],
    });
  });

  it('identifica visualmente uma resposta sem contexto', async () => {
    vi.mocked(sendChat).mockResolvedValue({
      answer: 'Não encontrei informações suficientes na base de conhecimento.',
      sources: [],
      has_context: false,
    });
    render(<ChatPage />);

    await ask('Qual é a cotação do dólar?');

    expect(await screen.findByText('Sem contexto suficiente')).toBeInTheDocument();
    expect(screen.queryByLabelText('Fontes da resposta')).not.toBeInTheDocument();
  });

  it('apresenta um erro compreensível retornado pela API', async () => {
    vi.mocked(sendChat).mockRejectedValue(
      new ApiError('O modelo demorou demais para responder. Tente novamente.', 504, 'MODEL_TIMEOUT'),
    );
    render(<ChatPage />);

    await ask('Pergunta lenta');

    expect(
      await screen.findByText('O modelo demorou demais para responder. Tente novamente.'),
    ).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Tentar novamente' })).toBeInTheDocument();
  });

  it('limpa todas as mensagens visíveis sem chamar o backend', async () => {
    vi.mocked(sendChat).mockResolvedValue(contextualResponse);
    render(<ChatPage />);
    const user = await ask('Pergunta temporária');
    await screen.findByText(contextualResponse.answer);

    await user.click(screen.getByRole('button', { name: 'Limpar conversa' }));

    expect(screen.queryByText('Pergunta temporária')).not.toBeInTheDocument();
    expect(screen.queryByText(contextualResponse.answer)).not.toBeInTheDocument();
    expect(screen.getByText('Nova conversa')).toBeInTheDocument();
    expect(sendChat).toHaveBeenCalledOnce();
  });
});
