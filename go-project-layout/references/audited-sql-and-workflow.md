## Contents

- [Purpose](#purpose)
- [Audit set](#audit-set)
- [Corroborated findings](#corroborated-findings)
- [Focused findings](#focused-findings)
- [Specialized cautions](#specialized-cautions)
- [Required decision procedure](#required-decision-procedure)
- [What this category does not establish](#what-this-category-does-not-establish)

## Purpose

This reference records pinned evidence from selected SQL, migration, workflow, and storage repositories. Use it for SQL ownership, migration placement, persistence boundaries, and names such as `query.go`, `store.go`, `run.go`, and `execution.go`. Do not treat these repositories as complete application templates.

## Audit set

|Repository|Audited revision|Date|Product shape|Corpus role|
|---|---|---|---|---|
|[ZITADEL](https://github.com/zitadel/zitadel/tree/917ade35af9c51e4b57ca8e57488ae95928182ad)|[`917ade3`](https://github.com/zitadel/zitadel/commit/917ade35af9c51e4b57ca8e57488ae95928182ad)|2026-07-29|Identity platform with event sourcing, SQL projections, workers, and migrations|Specialized precedent|
|[sqlc](https://github.com/sqlc-dev/sqlc/tree/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5)|[`a95e91d`](https://github.com/sqlc-dev/sqlc/commit/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5)|2026-04-22|SQL compiler and typed code generator|Focused precedent|
|[Goose](https://github.com/pressly/goose/tree/520411a16119bd3b332613d1ff8312c4cc249673)|[`520411a`](https://github.com/pressly/goose/commit/520411a16119bd3b332613d1ff8312c4cc249673)|2026-07-22|SQL and Go migration library and CLI|Focused precedent|
|[Temporal](https://github.com/temporalio/temporal/tree/e015b7a8c24d327a72e9dab8526966f4f58ba501)|[`e015b7a`](https://github.com/temporalio/temporal/commit/e015b7a8c24d327a72e9dab8526966f4f58ba501)|2026-06-10|Durable workflow server with several persistence backends and schema tooling|Focused precedent; architecture is specialized|
|[Prometheus](https://github.com/prometheus/prometheus/tree/bb5dff00cf8fdfbf5c65e0531aa835fa238a43a2)|[`bb5dff0`](https://github.com/prometheus/prometheus/commit/bb5dff00cf8fdfbf5c65e0531aa835fa238a43a2)|2026-07-30|Monitoring server with a custom TSDB and query language|Specialized non-SQL counterexample|

## Corroborated findings

### SQL placement follows ownership

No audited repository establishes a universal `queries/` directory.

ZITADEL colocates static SQL with the Go code that binds parameters, scans rows, and owns the result. [`internal/query/user.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/query/user.go) embeds adjacent [`user_by_id.sql`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/query/user_by_id.sql). Its PostgreSQL event-store adapter keeps provider-specific query construction in [`internal/v2/eventstore/postgres/query.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/v2/eventstore/postgres/query.go).

Goose keeps database-specific version-table SQL with dialect implementations under [`internal/dialects`](https://github.com/pressly/goose/tree/520411a16119bd3b332613d1ff8312c4cc249673/internal/dialects). User schema history remains in versioned migration files, illustrated by [`examples/sql-migrations`](https://github.com/pressly/goose/tree/520411a16119bd3b332613d1ff8312c4cc249673/examples/sql-migrations).

Temporal keeps runtime SQL beside dialect-specific methods, as in [`sqlplugin/mysql/execution.go`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/common/persistence/sql/sqlplugin/mysql/execution.go), while deploy-time schema history lives under [`schema`](https://github.com/temporalio/temporal/tree/e015b7a8c24d327a72e9dab8526966f4f58ba501/schema).

Use a `queries/` subdirectory when a coherent group of SQL assets benefits from separate navigation, generation, ownership, or tooling. For one or a few queries, compare adjacency with a dedicated asset boundary rather than assuming either is clearer. Treat generated SQL, migration SQL, provider SQL, and application read SQL as different ownership cases.

### Persistence boundaries should describe capabilities

ZITADEL separates connection and transaction mechanics in [`internal/database/database.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/database/database.go), application read behavior in `internal/query`, and provider-specific event persistence in PostgreSQL packages.

Goose's [`database.Store`](https://github.com/pressly/goose/blob/520411a16119bd3b332613d1ff8312c4cc249673/database/store.go) owns the narrow behavior needed to create, inspect, and update migration-version state. The name is coherent because the package and interface form `database.Store`.

Temporal defines backend-neutral capability interfaces such as `ExecutionStore`, `TaskStore`, and `ShardStore` in [`common/persistence/persistence_interface.go`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/common/persistence/persistence_interface.go). SQL and Cassandra adapters implement them. This abstraction depth follows a real multi-backend requirement and should not be copied into a single-database service.

Prometheus provides a non-relational example. [`storage/interface.go`](https://github.com/prometheus/prometheus/blob/bb5dff00cf8fdfbf5c65e0531aa835fa238a43a2/storage/interface.go) defines capabilities needed by query evaluation and ingestion, while [`tsdb`](https://github.com/prometheus/prometheus/tree/bb5dff00cf8fdfbf5c65e0531aa835fa238a43a2/tsdb) owns its concrete format, recovery, compaction, and retrieval behavior.

The durable rule is to define persistence abstractions around behavior required by consumers. Use a concrete technology package when there is one implementation and no supported abstraction boundary.

### Generic filenames are contextual, not defective

The audited repositories use generic words successfully when package context supplies precision:

- ZITADEL [`internal/query/query.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/query/query.go) owns the `Queries` facade and shared query behavior.

- ZITADEL [`internal/v2/eventstore/postgres/storage.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/v2/eventstore/postgres/storage.go) defines the PostgreSQL event-store adapter.

- Goose [`database/store.go`](https://github.com/pressly/goose/blob/520411a16119bd3b332613d1ff8312c4cc249673/database/store.go) defines migration-state persistence.

- Goose [`provider_run.go`](https://github.com/pressly/goose/blob/520411a16119bd3b332613d1ff8312c4cc249673/provider_run.go) orchestrates preparing and applying migrations.

- Temporal [`common/persistence/sql/store.go`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/common/persistence/sql/store.go) owns SQL plugin registration and database construction.

- Temporal [`common/persistence/sql/execution.go`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/common/persistence/sql/execution.go) implements persistence for the workflow-execution aggregate.

- Prometheus [`cmd/promtool/query.go`](https://github.com/prometheus/prometheus/blob/bb5dff00cf8fdfbf5c65e0531aa835fa238a43a2/cmd/promtool/query.go) implements promtool query commands.

Review the package path, declarations, and responsibility together. Do not rename a clear `run.go`, `store.go`, `query.go`, or `execution.go` merely because the filename is broad in isolation.

### `run` and `execution` are domain terms

Goose uses `run` for migration orchestration in [`provider_run.go`](https://github.com/pressly/goose/blob/520411a16119bd3b332613d1ff8312c4cc249673/provider_run.go).

Temporal uses `execution` for a persisted workflow aggregate and distinguishes a workflow identifier from each concrete run identifier. The schema records both in [`schema/postgresql/v12/temporal/schema.sql`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/schema/postgresql/v12/temporal/schema.sql).

ZITADEL's [`internal/execution/execution.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/internal/execution/execution.go) uses `execution` for configurable action targets.

Choose the term already used by the product domain. Do not replace `run` with `execution` to sound more formal. Define the distinction explicitly if both exist.

### Migration history is not ordinary application SQL

Goose uses numbered or timestamped migration files with explicit Up and optional Down sections. [`migration.go`](https://github.com/pressly/goose/blob/520411a16119bd3b332613d1ff8312c4cc249673/migration.go) validates and dispatches them.

Temporal maintains complete baseline schemas plus ordered version directories with manifests, compatibility information, and statement lists. See [`v1.19/manifest.json`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/schema/postgresql/v12/temporal/versioned/v1.19/manifest.json) and [`tools/common/schema/updatetask.go`](https://github.com/temporalio/temporal/blob/e015b7a8c24d327a72e9dab8526966f4f58ba501/tools/common/schema/updatetask.go).

ZITADEL uses explicitly ordered setup steps that may embed adjacent SQL, such as [`cmd/setup/73.go`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/cmd/setup/73.go) and [`73.sql`](https://github.com/zitadel/zitadel/blob/917ade35af9c51e4b57ca8e57488ae95928182ad/cmd/setup/73.sql). Its migration history includes event-store and projection concerns and is specialized.

Keep migrations in a clearly versioned schema-history boundary. Choose its exact placement based on the migration tool, deployment process, database count, and whether assets must be embedded.

## Focused findings

### sqlc separates source SQL, generated code, and database capabilities

The [`examples/authors`](https://github.com/sqlc-dev/sqlc/tree/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5/examples/authors) fixture binds authored schema and query files to generated packages through [`sqlc.yaml`](https://github.com/sqlc-dev/sqlc/blob/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5/examples/authors/sqlc.yaml). [`query.sql`](https://github.com/sqlc-dev/sqlc/blob/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5/examples/authors/postgresql/query.sql) produces [`query.sql.go`](https://github.com/sqlc-dev/sqlc/blob/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5/examples/authors/postgresql/query.sql.go), preserving source identity.

Generated [`db.go`](https://github.com/sqlc-dev/sqlc/blob/a95e91d70ad9e1181253c333a1cfdd75ae4b95a5/examples/authors/postgresql/db.go) owns the narrow `DBTX` capability used by generated queries. This is evidence for consumer-specific database capabilities and deterministic generated-code ownership. It is not a universal application layout.

### A `query` package may represent a query language, not stored SQL

Temporal's [`visibility/store/query`](https://github.com/temporalio/temporal/tree/e015b7a8c24d327a72e9dab8526966f4f58ba501/common/persistence/visibility/store/query) parses and converts a SQL-like visibility language. Prometheus separates PromQL evaluation in [`promql`](https://github.com/prometheus/prometheus/tree/bb5dff00cf8fdfbf5c65e0531aa835fa238a43a2/promql) from physical retrieval in `storage` and `tsdb`.

Do not infer that a directory named `query` contains SQL files. Read its responsibility.

## Specialized cautions

- ZITADEL's event sourcing, projections, and coexisting persistence generations make its package depth unsuitable as a default service layout.

- sqlc is a compiler and generator; generated filenames and example colocation are tool conventions.

- Goose is a migration framework. Its migration abstractions are the product, not ordinary application structure.

- Temporal supports several persistence engines and durable workflow semantics. Its abstraction count and workflow vocabulary are specialized.

- Prometheus has no relational schema or SQL migration corpus. Use it only as a counterexample for persistence capability ownership and query separation.

## Required decision procedure

For SQL and persistence layout decisions:

1. Classify the asset as application query, provider-specific query, generated source, migration history, fixture, query-language implementation, or schema baseline.

2. Identify the Go package or deployment tool that owns its semantics.

3. Determine whether SQL is static, generated, composed, or dialect-specific.

4. Determine whether it must be embedded, deployed independently, or consumed by external tools.

5. Inspect the code that binds parameters, executes statements, scans results, and handles transactions.

6. Compare adjacency with a dedicated SQL asset boundary using ownership, navigation, generation, and tooling constraints.

7. Keep migrations in a versioned boundary understood by the selected migration tooling.

8. Use `store`, `query`, `run`, or `execution` only when package context and product language make the concept clear.

9. Require a demonstrated consumer seam, committed alternative, or compatibility obligation before creating a backend-neutral persistence layer. A second implementation is strong evidence, not a prerequisite.

10. Cite a pinned analogous file and a credible counterexample for disputed decisions.

## What this category does not establish

These repositories do not settle:

- Root `main.go` versus `cmd/<binary>` for ordinary applications

- HTTP handler organization

- Embedded frontend structure

- Scheduled-job deployment

- Generic domain-package layout

- Cloud-provider adapter boundaries

Use application and integration-service audits for those decisions.
