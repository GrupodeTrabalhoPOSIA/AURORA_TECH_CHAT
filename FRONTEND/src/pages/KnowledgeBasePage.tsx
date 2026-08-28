import { useCallback, useState } from 'react';

import {
  DocumentFeedbackBanner,
  DocumentList,
  DocumentUpload,
} from '@/features/documents';
import type { DocumentFeedback, KnowledgeDocument } from '@/features/documents';

const acceptedExtensions = new Set(['pdf', 'txt', 'md', 'docx']);
const maxFileSize = 10 * 1024 * 1024;

const initialDocuments: KnowledgeDocument[] = [
  {
    id: 'mock-institucional',
    name: 'apresentacao-aurora.pdf',
    type: 'pdf',
    chunkCount: 8,
    size: 184_320,
  },
];

function getExtension(filename: string): string {
  return filename.split('.').pop()?.toLowerCase() ?? '';
}

function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<KnowledgeDocument[]>(initialDocuments);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [feedback, setFeedback] = useState<DocumentFeedback | null>(null);

  const handleSelect = useCallback((file: File | null): void => {
    setFeedback(null);
    if (!file) {
      setSelectedFile(null);
      return;
    }

    const extension = getExtension(file.name);
    if (!acceptedExtensions.has(extension)) {
      setSelectedFile(null);
      setFeedback({ kind: 'error', message: 'Formato inválido. Use PDF, TXT, MD ou DOCX.' });
      return;
    }
    if (file.size > maxFileSize) {
      setSelectedFile(null);
      setFeedback({ kind: 'error', message: 'O arquivo deve ter no máximo 10 MB.' });
      return;
    }
    setSelectedFile(file);
  }, []);

  const handleUpload = useCallback((): void => {
    if (!selectedFile) {
      return;
    }

    setIsUploading(true);
    setFeedback(null);
    window.setTimeout(() => {
      const extension = getExtension(selectedFile.name) as KnowledgeDocument['type'];
      const newDocument: KnowledgeDocument = {
        id: `${selectedFile.name}-${selectedFile.lastModified}`,
        name: selectedFile.name,
        type: extension,
        chunkCount: Math.max(1, Math.ceil(selectedFile.size / 700)),
        size: selectedFile.size,
      };
      setDocuments((current) => [newDocument, ...current]);
      setSelectedFile(null);
      setIsUploading(false);
      setFeedback({
        kind: 'success',
        message: `${newDocument.name} foi adicionado à demonstração.`,
      });
    }, 700);
  }, [selectedFile]);

  const handleRemove = useCallback((document: KnowledgeDocument): void => {
    const confirmed = window.confirm(`Remover "${document.name}" da base de conhecimento?`);
    if (!confirmed) {
      return;
    }
    setDocuments((current) => current.filter((item) => item.id !== document.id));
    setFeedback({ kind: 'success', message: `${document.name} foi removido.` });
  }, []);

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

      <div className="knowledge-workspace">
        <DocumentUpload
          selectedFile={selectedFile}
          isUploading={isUploading}
          onSelect={handleSelect}
          onUpload={handleUpload}
        />
        {feedback ? (
          <DocumentFeedbackBanner feedback={feedback} onDismiss={() => setFeedback(null)} />
        ) : null}
        <div className="document-list-heading">
          <div>
            <span className="eyebrow">Arquivos preparados</span>
            <h2>Documentos</h2>
          </div>
          <span className="document-count">{documents.length}</span>
        </div>
        <DocumentList documents={documents} onRemove={handleRemove} />
      </div>
    </section>
  );
}

export default KnowledgeBasePage;
