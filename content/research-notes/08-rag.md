---
title: "Retrieval-augmented generation: the reliability story"
date: 2026-02-15
draft: false
tags: ["llm", "rag", "reliability", "methodology"]
---

# Retrieval-augmented generation: the reliability story

> Retrieval-augmented generation (RAG), pairing a language model with an external retriever that fetches relevant documents to ground the model's output, is the dominant architecture for factual question answering in production LLM systems. The 2020 paper that named the approach (Lewis et al.) is one of the most-cited NLP papers of the decade. We cover the basic architecture, the three primary failure modes you will hit in deployment, and why "just add RAG" is a more honest sentence when you understand what it doesn't fix.

## 1. The architecture

![RAG pipeline with three failure-mode annotations](/research-notes/figures/rag-fig1-architecture.svg)

The pipeline has four components:

1. **Query** $q$, the user's question.
2. **Retriever** $R(q)$, returns top-$k$ passages from a document corpus, ranked by semantic similarity (dense vectors via sentence encoders) or lexical match (BM25) or both.
3. **Generator LLM**, conditions on $q$ plus the retrieved passages and produces an answer.
4. **Optional reranker**, a second-stage model that re-scores the top-$k$ passages for tighter relevance before feeding them to the generator.

Lewis et al. (2020) formalized the setup with a differentiable retriever (DPR) and a seq2seq generator, trained end-to-end on knowledge-intensive NLP tasks. Modern production RAG decouples the components: the retriever is trained separately (or a pretrained sentence encoder is used off-the-shelf), and the generator is a general-purpose LLM that takes retrieved text in its prompt.

## 2. Why RAG works, and when it does not

The success story is easy to tell. Pre-trained LLMs store factual knowledge in weights, but their knowledge is (a) frozen at training cutoff, (b) lossy (they hallucinate low-frequency facts), and (c) opaque (you can't audit which fact was used). RAG externalizes the knowledge source. The LLM becomes a *composer* of retrieved facts rather than an *owner* of them. Updates require only re-indexing the corpus, not retraining the model.

The failure story is more interesting and less told.

### 2.1 Failure mode (a): retrieval miss

The retriever returns passages that are semantically similar to the query but **not informative for the answer**. Two subcases:

**Lexical-semantic mismatch.** The query uses one vocabulary; the relevant passage uses another. A query about "heart attack" may miss a passage about "myocardial infarction" if the embedding model wasn't trained on enough medical overlap. Dense retrievers handle this better than sparse (BM25), but not perfectly.

**Multi-hop queries.** The answer requires chaining facts from multiple passages. Top-$k$ retrieval selects passages independently; nothing ensures they jointly cover the reasoning path. Asai et al. (2023) show that standard RAG misses a large fraction of multi-hop answers that a human with the corpus could easily solve.

### 2.2 Failure mode (b): index staleness

The index was built on a corpus snapshot at time $t_0$. Facts change. Corporate acquisitions, policy updates, version numbers, prices, all drift. If the index is not continuously refreshed, the system confidently returns outdated information.

This is an operational failure rather than a scientific one, but it is the most common cause of "production RAG gives the wrong answer" in real deployments. Most teams underestimate the refresh frequency needed for business-critical knowledge bases.

### 2.3 Failure mode (c): context pollution

Here is the most subtle problem and the one best-documented in recent research.

**Xu et al. (2024)** and **Liu et al. (2024)** show that LLMs are surprisingly poor at ignoring irrelevant context. When retrieved passages contain even a few sentences tangentially related to the query but not actually informative, model answers drift systematically toward whatever appears in the context, even when the model's internal knowledge would have produced a correct answer without retrieval.

This inverts the naive intuition: the retriever increases context *size*, which means it increases the attack surface for distractor content. A high-recall retriever that returns more weakly-relevant passages may *hurt* end-to-end accuracy compared to a lower-recall retriever that returns fewer but sharper results.

**Shi et al. (2023)** quantify this: injecting a single irrelevant sentence into the context of a math word-problem reduces GPT-3.5's accuracy by 8–10 percentage points. The model is not robustly filtering context.

## 3. The RAG reliability toolkit

Recent work has converged on a set of practical improvements that mitigate the failure modes above.

### 3.1 Better retrieval

- **Hybrid retrieval** (dense + BM25) dominates either alone on most benchmarks.
- **Rerankers** (cross-encoders that jointly score $(q, p)$ pairs) substantially improve precision at top-$k$. The two-stage retrieve-then-rerank pipeline is the current production default.
- **Query rewriting** (Ma et al. 2023): use the LLM to rewrite $q$ into a more retrieval-friendly form before hitting the retriever. Particularly effective for conversational multi-turn queries where the retrieval target is implicit.

### 3.2 Adaptive retrieval

Rather than always retrieving top-$k$ regardless of query, **Self-RAG** (Asai et al. 2023) trains the model to emit special tokens that trigger retrieval only when needed, and to score the relevance of retrieved passages before using them. This reduces context pollution at the cost of a more complex training pipeline.

### 3.3 Citation and verification

Production systems increasingly require the generator to produce answers with **inline citations** linking claims to retrieved passages. The citation is both a UX feature (users can verify) and an internal consistency check (if the model cannot cite, it should not assert).

Recent work on **grounded generation** formalizes this: the model is trained or instructed to emit only claims directly supported by the retrieved passages. Menick et al. (2022) and the Sparrow line of work from DeepMind are representative. The trade-off is that strict grounding can cause the model to refuse to answer questions where the retrieval is incomplete, a real-usability regression.

### 3.4 Conformal wrapping

As discussed in the [conformal prediction note](/research-notes/06-conformal), conformal sets can wrap RAG outputs to provide calibrated abstention. If the conformal set is small, the model answers; if the set is large, the system defers. This is the cleanest principled approach to knowing when RAG is reliable.

## 4. RAG ≠ agent

An important conceptual point that is routinely muddled in industry: **RAG is not an agent**. RAG is a prompting pattern with one retrieval call per query. An agent (see [note 5](/research-notes/05-llm-agents)) may make multiple retrieval calls, interleave them with reasoning, take external actions, and adapt its strategy based on observations.

Agentic RAG, where the agent decides when to retrieve, what to query, and how to compose multiple retrievals, is more powerful but also more expensive, slower, and less reliable. Most production "RAG" systems are single-shot; the design space between single-shot RAG and full agent is where much current engineering effort lives.

## 5. Open questions

**Long-context vs. retrieval.** As LLM context windows grow to 1M+ tokens, a natural question is whether retrieval is still needed. Empirically, models with large context windows still benefit from *good* retrieval, stuffing the whole corpus into context degrades accuracy, probably due to attention dilution. But the optimal retrieval strategy and the right window size are under active study.

**Structured retrieval.** Most RAG systems treat the corpus as a bag of paragraphs. Corpora with structure (code repositories with dependency graphs, knowledge bases with typed relations, scientific literature with citation networks) offer richer retrieval signals that flat embedding-based retrieval ignores.

**Evaluation.** RAG evaluation is hard because the ground truth depends on the corpus, which changes. Benchmarks like KILT (Petroni et al. 2021) provide held-out test sets with known provenance, but generalizing to production corpora is an open problem.

**Retrieval-time vs. training-time knowledge.** There is a spectrum between storing knowledge in weights (high recall, low freshness, high hallucination) and storing it externally (high freshness, bounded by retriever, better provenance). The *optimal allocation* between the two is application-dependent and poorly understood.

## 6. References

- **Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Kuttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D.** (2020). *Retrieval-augmented generation for knowledge-intensive NLP tasks*. NeurIPS. [S.S. `659bf9ce`]
- **Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W.** (2020). *Dense passage retrieval for open-domain question answering*. EMNLP.
- **Asai, A., Wu, Z., Wang, Y., Sil, A., & Hajishirzi, H.** (2023). *Self-RAG: learning to retrieve, generate, and critique through self-reflection*. ICLR.
- **Xu, Z., et al.** (2024). *Retrieval meets long context large language models*. ICLR.
- **Liu, N. F., Lin, K., Hewitt, J., et al.** (2024). *Lost in the middle: how language models use long contexts*. TACL.
- **Shi, F., Chen, X., Misra, K., et al.** (2023). *Large language models can be easily distracted by irrelevant context*. ICML.
- **Ma, X., Gong, Y., He, P., Zhao, H., & Duan, N.** (2023). *Query rewriting for retrieval-augmented large language models*. EMNLP.
- **Menick, J., Trebacz, M., Mikulik, V., et al.** (2022). *Teaching language models to support answers with verified quotes*. arXiv.
- **Petroni, F., Piktus, A., Fan, A., et al.** (2021). *KILT: a benchmark for knowledge-intensive language tasks*. NAACL.
