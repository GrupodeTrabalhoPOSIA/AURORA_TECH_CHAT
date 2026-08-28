import { useCallback, useEffect, useRef, useState } from 'react';

import { getHealth } from '@/features/health/api/healthApi';
import type { ApiAvailability } from '@/types';

interface UseApiHealthResult {
  status: ApiAvailability;
  checkAgain: () => void;
}

/** Observa a saúde da API e permite uma nova tentativa manual. */
export function useApiHealth(): UseApiHealthResult {
  const [status, setStatus] = useState<ApiAvailability>('checking');
  const controllerRef = useRef<AbortController | null>(null);

  const checkAgain = useCallback((): void => {
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;
    setStatus('checking');

    void getHealth(controller.signal)
      .then(() => setStatus('online'))
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') {
          return;
        }
        setStatus('offline');
      });
  }, []);

  useEffect(() => {
    checkAgain();
    return () => controllerRef.current?.abort();
  }, [checkAgain]);

  return { status, checkAgain };
}

