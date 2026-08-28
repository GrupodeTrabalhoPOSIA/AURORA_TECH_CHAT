import { act, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import KnowledgeBasePage from './KnowledgeBasePage';

function getFileInput(container: HTMLElement): HTMLInputElement {
  const input = container.querySelector<HTMLInputElement>('input[type="file"]');
  if (!input) {
    throw new Error('Input de arquivo não encontrado.');
  }
  return input;
}

describe('KnowledgeBasePage', () => {
  beforeEach(() => {
    vi.spyOn(window, 'confirm').mockReturnValue(true);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it('aceita um formato suportado e inicia o processamento', async () => {
    vi.useFakeTimers();
    const { container } = render(<KnowledgeBasePage />);
    const file = new File(['Aurora Tech'], 'empresa.txt', { type: 'text/plain' });

    fireEvent.change(getFileInput(container), { target: { files: [file] } });
    fireEvent.click(screen.getByRole('button', { name: 'Adicionar à base' }));

    expect(screen.getByRole('button', { name: 'Processando…' })).toBeDisabled();
    await act(async () => vi.runAllTimersAsync());
    expect(screen.getAllByText('empresa.txt')).toHaveLength(1);
    expect(screen.getByText(/foi adicionado à demonstração/)).toBeInTheDocument();
  });

  it('rejeita um formato não suportado', () => {
    const { container } = render(<KnowledgeBasePage />);
    const file = new File(['a,b'], 'dados.csv', { type: 'text/csv' });

    fireEvent.change(getFileInput(container), { target: { files: [file] } });

    expect(screen.getByText('Formato inválido. Use PDF, TXT, MD ou DOCX.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Adicionar à base' })).toBeDisabled();
  });

  it('remove o último documento e apresenta o estado vazio', async () => {
    const user = userEvent.setup();
    render(<KnowledgeBasePage />);

    await user.click(screen.getByRole('button', { name: 'Remover apresentacao-aurora.pdf' }));

    expect(window.confirm).toHaveBeenCalledOnce();
    expect(screen.getByText('Nenhum documento adicionado')).toBeInTheDocument();
    expect(screen.getByText('apresentacao-aurora.pdf foi removido.')).toBeInTheDocument();
  });
});
