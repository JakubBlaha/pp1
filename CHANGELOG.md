# 10 May 2026

## Changes

- Modifiers are now split into flags (presence carries meaning) and parameterised modifiers (carry a value in $V$). The entity type modifiers function $M_E$ now maps to $\mathcal{P}(\mathit{ModKey})$ instead of $\mathcal{P}(M)$, making clear that the set contains keys, not modifier values.
- The per-entity modifier component is renamed from $m_e$ to $\mu_e$ and redefined as a partial function $\mu_e : \mathit{ModKey} \rightharpoonup V$ (instead of a set), with $\mathrm{dom}(\mu_e) \subseteq M_E(t_e)$.
- Entity values can now be undefined: `Valuation` is redefined as a partial function $\sigma : E \rightharpoonup V$. Event entities are always defined. `Val_\rho` is correspondingly partial ($E \times T \rightharpoonup V$), undefined when $e \notin \mathrm{dom}(\rho(t))$.
- Removed entity name set

## Fixes

- defined the entity set $E$
- formally define $t_\text{next}$
- define if sets are finite or infinite
- seaparate operator definition in expressions from constants definition

# 5 May 2026

# Todo:

- generic attribute predicate
- need to extend value domain with addresses at least
- add isUndefined predicate
- setup and stimuli can use greek letters
