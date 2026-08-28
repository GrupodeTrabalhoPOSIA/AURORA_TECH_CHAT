# Avaliação RAG do MVP

Esta avaliação verifica a recuperação de fontes antes da chamada ao modelo. Ela usa o modelo real de embeddings configurado, uma coleção Chroma temporária, três perguntas respondíveis e uma pergunta sem relação com a base.

## Resultado de referência

Em 27/08/2026, `python evaluation/evaluate_rag.py` aprovou 4 de 4 casos:

- serviços oferecidos → `servicos.txt`;
- horário comercial → `servicos.txt`;
- missão da empresa → `empresa.txt`;
- previsão do tempo em Marte → recusada sem contexto.

## Parâmetros finais

- modelo: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`;
- tamanho do chunk: 700 caracteres;
- sobreposição: 100 caracteres;
- `top_k`: 5;
- relevância mínima: 0,35;
- contexto máximo: 6.000 caracteres.

O limiar 0,35 preservou a pergunta conhecida com menor pontuação observada (0,38) e rejeitou o caso negativo. A base é deliberadamente pequena e acadêmica; uma implantação real exigiria um conjunto de avaliação maior e revisão periódica desses valores.

## Execução

```powershell
$env:HF_HUB_OFFLINE='1'
python evaluation/evaluate_rag.py
```

Remova `HF_HUB_OFFLINE` na primeira execução caso o modelo ainda não esteja no cache local.
