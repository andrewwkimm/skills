## Purpose

Use this reference for single-product CLIs, servers, and focused applications. It supplies application evidence for executable placement, package visibility, interfaces, and contextual filenames.

## Audit set

|Repository|Audited revision|Date|Product shape|Corpus role|
|---|---|---|---|---|
|[Miniflux](https://github.com/miniflux/v2/tree/681b00f6130a9379d33b1920f1bfe52b6494270a)|[`681b00f`](https://github.com/miniflux/v2/commit/681b00f6130a9379d33b1920f1bfe52b6494270a)|2026-08-02|Single-binary PostgreSQL-backed web application with one public client package|Focused precedent|
|[restic](https://github.com/restic/restic/tree/a80be1478a4c537f8396e0db2b05120aa78f11e0)|[`a80be14`](https://github.com/restic/restic/commit/a80be1478a4c537f8396e0db2b05120aa78f11e0)|2026-08-01|Mature integration-heavy backup CLI|Specialized precedent|
|[GitHub CLI](https://github.com/cli/cli/tree/e83adbc0642994fae7c39a9a012eb34b8c81f4f1)|[`e83adbc`](https://github.com/cli/cli/commit/e83adbc0642994fae7c39a9a012eb34b8c81f4f1)|2026-08-01|Large single-product CLI plus repository tooling|Specialized precedent|
|[Caddy](https://github.com/caddyserver/caddy/tree/e096ca9503188f057c69a049f709fdade6077631)|[`e096ca9`](https://github.com/caddyserver/caddy/commit/e096ca9503188f057c69a049f709fdade6077631)|2026-08-01|Server and public module platform supporting custom binaries|Specialized precedent|
|[NATS Server](https://github.com/nats-io/nats-server/tree/ccd898ea86accf40861f1dd651df8e7fb9c0e5f3)|[`ccd898e`](https://github.com/nats-io/nats-server/commit/ccd898ea86accf40861f1dd651df8e7fb9c0e5f3)|2026-07-30|Single-binary high-performance messaging server|Specialized precedent|

## Corroborated findings

### One executable does not determine entry-point placement

Miniflux and NATS Server keep root entry points: [`Miniflux main.go`](https://github.com/miniflux/v2/blob/681b00f6130a9379d33b1920f1bfe52b6494270a/main.go) and [`NATS main.go`](https://github.com/nats-io/nats-server/blob/ccd898ea86accf40861f1dd651df8e7fb9c0e5f3/main.go#L16-L134). restic and GitHub CLI place their product entry points under [`cmd/restic`](https://github.com/restic/restic/tree/a80be1478a4c537f8396e0db2b05120aa78f11e0/cmd/restic) and [`cmd/gh`](https://github.com/cli/cli/blob/e83adbc0642994fae7c39a9a012eb34b8c81f4f1/cmd/gh/main.go). Caddy uses [`cmd/caddy`](https://github.com/caddyserver/caddy/blob/e096ca9503188f057c69a049f709fdade6077631/cmd/caddy/main.go) because the root is an importable product package and custom builds reuse its command behavior.

Choose between root `main.go` and `cmd/<binary>` by examining current and committed binaries, whether the root must remain importable, customization requirements, repository tools, and command complexity. Do not use executable count as the sole rule.

### Product binaries, repository tools, and subcommands are different

GitHub CLI's `cmd` includes product `gh` and tooling-only `gen-docs`, while user-facing subcommands live under command packages ([layout](https://github.com/cli/cli/blob/e83adbc0642994fae7c39a9a012eb34b8c81f4f1/docs/project-layout.md)). restic keeps release helpers outside its product command tree ([helpers](https://github.com/restic/restic/tree/a80be1478a4c537f8396e0db2b05120aa78f11e0/helpers)).

Classify build outputs before recommending directories. Subcommands do not justify separate `cmd/<name>` binaries.

### `internal` and public packages should match support intent

Miniflux exposes a top-level [`client`](https://github.com/miniflux/v2/tree/681b00f6130a9379d33b1920f1bfe52b6494270a/client) while keeping application implementation under [`internal`](https://github.com/miniflux/v2/tree/681b00f6130a9379d33b1920f1bfe52b6494270a/internal). restic documents that almost all reusable code is internal because the product is not a supported library ([root documentation](https://github.com/restic/restic/blob/a80be1478a4c537f8396e0db2b05120aa78f11e0/doc.go)). Caddy intentionally exposes many packages because custom binaries and modules import them ([root package](https://github.com/caddyserver/caddy/blob/e096ca9503188f057c69a049f709fdade6077631/caddy.go)).

Package location should reflect a support commitment. Directory names such as `pkg` or `lib` do not create one.

### Interfaces follow concrete semantic seams

Miniflux usually exposes concrete application types and uses sparse interfaces, including a local storage scanner ([storage](https://github.com/miniflux/v2/blob/681b00f6130a9379d33b1920f1bfe52b6494270a/internal/storage/web_session.go)). restic defines real backend, filesystem, and repository capability seams ([backend](https://github.com/restic/restic/blob/a80be1478a4c537f8396e0db2b05120aa78f11e0/internal/backend/backend.go), [filesystem](https://github.com/restic/restic/blob/a80be1478a4c537f8396e0db2b05120aa78f11e0/internal/fs/interface.go)). NATS keeps storage interfaces beside storage-domain types in [`server/store.go`](https://github.com/nats-io/nats-server/blob/ccd898ea86accf40861f1dd651df8e7fb9c0e5f3/server/store.go#L83-L128).

Consumer ownership remains a good default, but domain or extension ownership is valid when that package carries the compatibility obligation.

### Generic filenames are valid inside precise packages

The audit includes `model.go`, `storage.go`, `provider.go`, `interface.go`, `config.go`, `store.go`, and `util.go`. NATS's [`server/store.go`](https://github.com/nats-io/nats-server/blob/ccd898ea86accf40861f1dd651df8e7fb9c0e5f3/server/store.go#L83-L128) owns storage types and interfaces. Miniflux's [`internal/database/migrations.go`](https://github.com/miniflux/v2/blob/681b00f6130a9379d33b1920f1bfe52b6494270a/internal/database/migrations.go) owns its in-process migration sequence.

Judge file names using package context, declarations, and navigation value. Do not use a filename blacklist.

## Specialized cautions

- restic's command and internal package depth reflect a mature cross-platform backup application.

- GitHub CLI's `pkg`, root packages, and deprecated `utils` carry historical constraints; its own layout document identifies some of them.

- Caddy's public command package and module interfaces support custom builds and a plugin platform.

- NATS's large `server` package is a performance-sensitive historical design, not a greenfield package-size recommendation.

- Miniflux's inline PostgreSQL queries and in-process migrations reflect one database and one deployment model.

## Required decision procedure

For a focused application:

1. Separate product binaries, subcommands, tools, generators, and test fixtures.

2. Determine whether the module root is an application entry point or a supported importable package.

3. State the external Go API commitment explicitly.

4. Trace one real operation through command or HTTP input, domain behavior, integrations, and output.

5. Add interfaces only for real seams with known semantics.

6. Review broad file names in their package context.

7. Prefer the layout that most clearly supports current and committed near-term requirements without speculative boundaries.
