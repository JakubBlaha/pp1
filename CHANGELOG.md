# 6 Jun 2026

## Changes

- Fixed Stimulus definition: `op` was described as "an operation name from the operations table"; changed to `op ∈ O is an operation`, consistent with Definition [Operation].
- Added `register : B` and `non_volatile : B` as modifier keys for `Storage` entities to the $M_E$ table, which were used in examples but missing from the table.
- Added a Meaning column to the $M_E$ modifier table with a brief natural-language description of each modifier key.
- Renamed the "Value type" column in the $M_E$ table to "Type".
- Replaced the standalone `Addr` definition with a unified Definition [Modifier accessors] covering all five modifier keys: `Addr`, `IsReg`, `IsNonVol`, `EvtTarget`, `EvtType`.
- Simplified operation argument types from `A_i ⊆ V ∪ E` to `A_i ⊆ V` in both the Operation definition and the Stimulus definition, since $E \subset V$ via $V_{\text{nonset}}$.
- Fixed "the following two functions are defined for discrete time only" to "three" (`Prev`, `Next`, `RelTime`).
- Added footnote to `Now` clarifying what "ambient time point" means.
- Added footnote to `Size` explaining $\mathcal{P}_{\text{fin}}(S)$ notation.
- Added footnote to `Filter` noting that `Pred` is defined formally in the Predicates subsection (forward reference).
- Added a List of Symbols section at the end of the document — a two-column table mapping mathematical symbols to their natural-language names.

# 20 May 2026 (session 2)

## Changes

- Removed the `PE` (predefined events function) and the `EventType` concept entirely — predefined events are now expressed through the modifier system instead.
- Added `EventTypeLabel` as a new primitive set of abstract symbols: $\{\mathit{generic}, \mathit{calculated}, \mathit{written}, \mathit{read}, \mathit{entered}, \mathit{transmitted}, \mathit{received}, \mathit{inserted}, \mathit{removed}, \mathit{cleared}\}$.
- Introduced `ModVal = V_base ∪ ID_E ∪ EventTypeLabel` as the codomain of the modifier assignment function $\mu_e$, replacing the previous `V_base`. This allows modifiers to carry entity identifiers and event type labels.
- Extended the $M_E$ modifier table with two new keys for `Event` entities: `target : ID_E` (the entity this event is associated with) and `kind : EventTypeLabel` (the predefined event type). Every `Event` entity is expected to carry both modifiers — user-declared events link to an `EventTrigger` with `kind = generic`, predefined events link to their parent entity with the appropriate kind. A uniqueness note states that at most one `Event` entity with a given `(target, kind)` pair should exist in $E$.
- Added `EventTrigger` to $T_E$ for user-declared named events. Users now declare `EventTrigger` entities instead of plain `Event` entities when they want to express a named firable event.
- Updated `fire(t, e)` to target `EventTrigger` entities (previously `Event`); its effect is now `EvtPred(e, generic, t)`, making the operations table fully uniform.
- Introduced `EvtPred(e, ek, t)` as a shorthand local to the operations section, defined as $\forall\, ev \in E : (t_{ev} = \text{Event} \land \mu_{ev}(\mathit{belongs\_to}) = id_e \land \mu_{ev}(\mathit{type}) = ek) \Rightarrow \mathit{Val}_\rho(ev, t) = \mathit{true}$. A note clarifies that this causes $\mathit{Happening}(ev, t)$ to hold. All operation effect entries now use `EvtPred` instead of the old `Happening(ek(e), t)` form.
- `Happening(ev, t)` remains a single clean definition in the predicates section ($\Leftrightarrow \mathit{Val}_\rho(ev, t) = \mathit{true}$), used directly in requirement constraints with named `Event` entities.
- Updated examples: predefined-event usages now declare named `Event` entities with `target` and `type` modifiers and reference them via `Happening` directly; `EventTrigger` entities replace plain `Event` entities for user-declared events; companion `Event` entities with `kind = generic` are declared alongside each `EventTrigger`.

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
