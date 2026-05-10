# 10 May 2026

- Modifiers are now split into flags (presence carries meaning) and parameterised modifiers (carry a value in $V$). The entity type modifiers function $M_E$ now maps to $\mathcal{P}(\mathit{ModKey})$ instead of $\mathcal{P}(M)$, making clear that the set contains keys, not modifier values.
- The per-entity modifier component is renamed from $m_e$ to $\mu_e$ and redefined as a partial function $\mu_e : \mathit{ModKey} \rightharpoonup V$ (instead of a set), with $\mathrm{dom}(\mu_e) \subseteq M_E(t_e)$.

# 5 May 2026

# Todo:

- generic attribute predicate
- maybe we can completely remove the idea of the entity types
