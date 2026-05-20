# 20 May 2026

## Changes

- Added `Set` entity type to $T_E$, with predefined events $PE(\text{Set}) = \{\mathit{inserted}, \mathit{removed}, \mathit{cleared}\}$.
- Added set operations `insert(t, e, v)`, `remove(t, e, v)`, `clear(t, e)` to the operations table.
- Added `ValBefore_\rho(e, t)` trace function, defined as the left limit $\lim_{t' \to t^-} \mathit{Val}_\rho(e, t')$, used in set operation effect predicates.
- Added `Size(s)` function and `Filter(s, P)` expression in a new Set functions subsection.
- Added `Contains(v, s)` membership predicate.
- Introduced $\mathit{ID}_E$ as a primitive set of unique abstract tokens (entity identifiers).
- Split the Values definition into three layers: $V_{\text{base}} = \mathbb{B} \cup \mathbb{R} \cup T \cup \mathcal{I}$ (defined in §2); $V_{\text{nonset}} = V_{\text{base}} \cup E$ and $V = V_{\text{nonset}} \cup \mathcal{P}_{\text{fin}}(V_{\text{nonset}})$ (defined in §3 after entities). Set values are flat: elements are drawn from $V_{\text{nonset}}$ only.
- Entity tuple changed from $(n_e, t_e, \mu_e, d_e)$ to $(id_e, t_e, \mu_e)$: the name and description fields are removed; the identifier field $id_e \in \mathit{ID}_E$ is added with a uniqueness constraint across $E$.
- Narrowed $\mu_e$ codomain from $V$ to $V_{\text{base}}$: modifiers are static entity properties and do not require the full value set.
- Entities are now elements of $V$ (via $V_{\text{nonset}}$), enabling sets of entities as first-class values.
- Updated `insert`/`remove` argument type, `Size`, `Contains`, `Filter`, and the Set valuation constraint to use $V_{\text{nonset}}$.

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
