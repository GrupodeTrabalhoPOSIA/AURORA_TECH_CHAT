/** Documento apresentado na base de conhecimento. */
export interface KnowledgeDocument {
  id: string;
  name: string;
  type: 'pdf' | 'txt' | 'md' | 'docx';
  chunkCount: number;
  size: number;
}

/** Mensagem transitória exibida após uma ação. */
export interface DocumentFeedback {
  kind: 'success' | 'error';
  message: string;
}

