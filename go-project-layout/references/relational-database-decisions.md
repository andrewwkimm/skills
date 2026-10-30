## Contents

- [Scope](#scope)
- [Framing](#framing)
- [Default decisions](#default-decisions)
- [Transaction ownership](#transaction-ownership)
- [Required method](#required-method)
- [Review standard](#review-standard)
- [Evidence](#evidence)

## Scope

This reference governs the choice between handwritten and generated query code, generated-code ownership, SQL asset placement, migration boundaries, and CI verification. `database/sql` correctness mechanics belong to the Go Database Guide in the Code Style skill.

Enforcement follows the scheme in the Go Project Layout entry point.

## Framing

sqlc is a generator, not a runtime. It can target `database/sql`, `pgx/v4`, or `pgx/v5`, and `database/sql` is its default. Under this skill, generated Go code targets `database/sql`.

The question is never which library to use. It is where the generated boundary stops, and the answer may be nowhere, part of the query set, or nearly all of it.

## Default decisions

In a greenfield repository, or a repository with no established relational database runtime, new relational database code MUST use `database/sql` as its runtime boundary and MUST NOT add `sqlx`. This is a house rule and does not depend on upstream maintenance activity.

An existing repository that already standardizes on another runtime such as `pgx` MUST NOT have a second runtime introduced by new code during unrelated work. Preserve the established runtime. A runtime migration requires an explicit request.

Handwritten queries are the evaluation baseline. A project SHOULD begin there and adopt generation only when the required method demonstrates net benefit.

When sqlc is adopted, its configuration MUST set `sql_package` to `database/sql` explicitly. This is the tool default; declaring it makes the runtime policy visible and resistant to configuration drift.

The sqlc version MUST be pinned.

Generated code MUST remain internal. Generated row and parameter types MUST NOT be exposed as public domain contracts by default.

Generated files MUST NOT be edited by hand.

Organize persistence by capability or database ownership rather than a generic layer. Do not create one package per table, and do not create a global repository, models, or database catchall.

Keep authored queries near the package owning their semantics. Keep generated output in an unmistakable internal package such as `dbsqlc`. Consult the SQL and workflow evidence before fixing SQL asset placement: adjacency and a dedicated asset boundary are alternatives to compare, not a settled default.

Keep migrations in a versioned deployment boundary expected by the migration tool, with stated database ownership.

Split a large capability store across files in one package before adding another layer.

One reasonable shape, offered as an option rather than a prescription:

```
internal/
  orders/
    store.go
    queries.sql
    dbsqlc/
      db.go
      models.go
      queries.sql.go
migrations/
  0001_create_orders.sql
sqlc.yaml
```

## Transaction ownership

Use this chain unless project constraints require another:

```
composition root owns *sql.DB
workflow owns *sql.Tx
capability store accepts a transaction-bound handle
store functions never commit a caller-owned transaction
```

Generated and handwritten queries in one transaction MUST execute through the same transaction-bound connection. A shared `DBTX` parameter, a direct `*sql.Tx`, a generated `Queries.WithTx(tx)` wrapper, or an equivalent transaction-bound wrapper all satisfy this. The invariant is the shared connection, not a particular API shape.

## Required method

1. Inventory the candidate query set. Record which queries have static shapes and which vary at runtime through optional predicates, dynamic `IN` lists, dynamic projections, or dynamic ordering.

2. Verify prerequisites. Every one MUST hold for the queries proposed for generation:
   - The schema is reproducible as generator input.
   - The dialect and required SQL features are supported.
   - Each query proposed for generation is supported and static enough for reliable analysis.
   - Generated code can remain internal.
   - Generated rows can be mapped to domain types where semantics differ.
   - CI can regenerate and reject drift.
   - The tool version is pinned.

   A failed prerequisite blocks adoption for the affected queries. Do not weigh a failed prerequisite against payoff.

3. Assess demonstrated payoff. Cite concrete pressure rather than project size: repeated manual `Scan` and parameter-struct mapping; wide or heavily nullable result sets where scan arity is a recurring review hazard; prior defects from column order, scan misalignment, or schema drift; frequent coordinated schema and query changes; a substantial stable query corpus; existing deterministic generation and CI verification lowering marginal cost.

   Project size and query count alone MUST NOT decide adoption.

4. Record coverage separately from adoption. Adopting sqlc does not mean generating every query. The decision record MUST name which queries are generated, which stay handwritten, why the boundary sits there, and what conditions would move a query across it.

5. Inspect adoption cost. Count type overrides, rename mappings, dialect workarounds, generated-to-domain conversion code, and duplicate configuration across engines. A project SHOULD narrow or reject adoption when override and conversion complexity approaches the manual mapping complexity it replaces.

6. Define CI verification. Generated code committed to the repository MUST be verified by:

```
sqlc generate
git diff --exit-code -- <generated paths>
go build ./...
go test ./...
go vet ./...
```

   Add `sqlc vet` when the pinned version and configuration support the required checks.

7. State the validation limit. sqlc validates queries against its declared schema inputs. It does not prove that a deployed database matches those inputs. Migration verification remains a separate obligation.

## Review standard

- `sqlx` added to a new project (MUST).
- A second runtime introduced into an established single-runtime repository during unrelated work (MUST).
- sqlc adopted with an unmet prerequisite (MUST).
- sqlc adopted on query count or project size alone (MUST).
- Generated code committed without a CI drift check (MUST).
- Generated files edited by hand (MUST).
- An unpinned sqlc version (MUST).
- A claim that generation proves the deployed schema matches (MUST).
- Related statements in one transaction executed through different connections (MUST).
- Generated row types exposed as public domain contracts without a stated reason (SHOULD).
- Dynamic SQL distorted into large `CASE` expressions or combinatorial generated methods to claim full adoption (SHOULD).
- Coverage undocumented after adoption (SHOULD).

## Evidence

- [sqlc configuration reference](https://docs.sqlc.dev/en/stable/reference/config.html) documents the `database/sql`, `pgx/v4`, and `pgx/v5` targets and the default.
- [River](https://github.com/riverqueue/river/blob/v0.40.0/riverdriver/riverdatabasesql/internal/dbsqlc/sqlc.yaml) declares its `sql_package` explicitly and documents four type overrides, including `jsonb` mapped to `string` because `database/sql` rejects byte slices for that type.
- [Inngest](https://github.com/inngest/inngest/blob/697184d4c86c750834f47e697d6384f4467cb2ba/sqlc.yaml) shows adoption cost at scale: dual PostgreSQL and SQLite configuration with dozens of per-column overrides and two documented generator workarounds.
- [Miniflux](https://github.com/miniflux/v2/blob/2.3.2/internal/storage/entry_query_builder.go) keeps handwritten `database/sql` with a purpose-built builder because filtering, sorting, projection, and pagination vary at runtime.
- [ZITADEL](https://github.com/zitadel/zitadel/blob/v4.16.2/internal/database/database.go) defines small capabilities implemented by both pool and transaction types and keeps transaction ownership explicit. It also carries `pgxpool`, so use it as evidence for interface and transaction ownership, not runtime selection.
