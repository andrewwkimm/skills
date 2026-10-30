## Contents

- [Purpose](#purpose)
- [Audit set](#audit-set)
- [Corroborated findings](#corroborated-findings)
- [Specialized cautions](#specialized-cautions)
- [Required decision procedure](#required-decision-procedure)
- [What this category does not establish](#what-this-category-does-not-establish)

## Purpose

Use this reference for repositories that combine substantial command surfaces, servers, frontends, multiple build targets, public SDKs, generated code, or long-lived migrations. These repositories are evidence for matching constraints, not greenfield templates.

## Audit set

|Repository|Audited revision|Date|Product shape|Corpus role|
|---|---|---|---|---|
|[Syncthing](https://github.com/syncthing/syncthing/tree/946e2b83a1f6c6ae119427c09e0a5802940b82ff)|[`946e2b8`](https://github.com/syncthing/syncthing/commit/946e2b83a1f6c6ae119427c09e0a5802940b82ff)|2026-08-03|Cross-platform synchronization product with several shipped servers, tools, embedded GUI, and SQLite|Specialized precedent|
|[Gitea](https://github.com/go-gitea/gitea/tree/6347a33b34f501ef5f788948cb9742fb046f6af5)|[`6347a33`](https://github.com/go-gitea/gitea/commit/6347a33b34f501ef5f788948cb9742fb046f6af5)|2026-08-03|Single-binary development platform with web UI, persistence, migrations, packages, and CI/CD|Specialized precedent|
|[Grafana](https://github.com/grafana/grafana/tree/a20530df7c32a7752a5e8cd0c765f812651eab73)|[`a20530d`](https://github.com/grafana/grafana/commit/a20530df7c32a7752a5e8cd0c765f812651eab73)|2026-08-04|Large Go and TypeScript monorepo with feature modules, plugins, generated APIs, and one unified executable|Specialized precedent|
|[k6](https://github.com/grafana/k6/tree/53b5727d893d30a5c73e5b1a9891283786e0ec44)|[`53b5727`](https://github.com/grafana/k6/commit/53b5727d893d30a5c73e5b1a9891283786e0ec44)|2026-08-03|Extensible single-binary load-testing product with public extension APIs and internal command composition|Specialized precedent|
|[Helm](https://github.com/helm/helm/tree/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56)|[`ae877c8`](https://github.com/helm/helm/commit/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56)|2026-08-03|One CLI plus deliberately supported SDK packages and compatibility-sensitive storage and plugin behavior|Focused precedent|

## Corroborated findings

### Executable placement follows repository shape

The audited repositories support several legitimate arrangements:

- Syncthing places shipped programs and tools under [`cmd`](https://github.com/syncthing/syncthing/tree/946e2b83a1f6c6ae119427c09e0a5802940b82ff/cmd), while its build definitions distinguish release targets from every executable utility in the tree ([build targets](https://github.com/syncthing/syncthing/blob/946e2b83a1f6c6ae119427c09e0a5802940b82ff/build.go#L67-L209)).

- Helm ships one executable from [`cmd/helm`](https://github.com/helm/helm/tree/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/cmd/helm) because the repository also supports importable SDK packages; its entry point is thin ([main](https://github.com/helm/helm/blob/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/cmd/helm/helm.go#L13-L41)).

- Gitea and k6 ship one executable from a root [`main.go`](https://github.com/go-gitea/gitea/blob/6347a33b34f501ef5f788948cb9742fb046f6af5/main.go) and [`main.go`](https://github.com/grafana/k6/blob/53b5727d893d30a5c73e5b1a9891283786e0ec44/main.go#L1-L10). Their `cmd` packages implement subcommands rather than separate binaries.

- Grafana ships one executable from [`pkg/cmd/grafana`](https://github.com/grafana/grafana/blob/a20530df7c32a7752a5e8cd0c765f812651eab73/pkg/cmd/grafana/main.go#L1-L43), a repository-specific historical arrangement.

Count current and committed binaries, then inspect whether the root is importable, whether custom binaries or SDKs are supported, and whether executable composition needs an explicit boundary. Do not infer the answer from executable count alone.

### Production binaries, tools, fixtures, and subcommands are different

Syncthing contains many `package main` directories but identifies a smaller set of named release targets ([targets](https://github.com/syncthing/syncthing/blob/946e2b83a1f6c6ae119427c09e0a5802940b82ff/build.go#L67-L195)). Helm contains a `package main` fixture that is not a shipped executable ([fixture](https://github.com/helm/helm/blob/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/internal/plugin/testdata/src/extismv1-test/main.go)). Gitea's `cmd` tree is command implementation under one root binary ([registration](https://github.com/go-gitea/gitea/blob/6347a33b34f501ef5f788948cb9742fb046f6af5/cmd/main.go#L116-L180)).

Inventory build and deployment outputs rather than counting `main` packages or `cmd` directories mechanically.

### Frontend placement follows the frontend build and delivery model

No universal frontend directory appears:

- Gitea keeps source under [`web_src`](https://github.com/go-gitea/gitea/tree/6347a33b34f501ef5f788948cb9742fb046f6af5/web_src) and builds it into application assets ([build rules](https://github.com/go-gitea/gitea/blob/6347a33b34f501ef5f788948cb9742fb046f6af5/Makefile#L118-L129)).

- Grafana keeps application source under [`public/app`](https://github.com/grafana/grafana/tree/a20530df7c32a7752a5e8cd0c765f812651eab73/public/app) and reusable frontend workspaces under [`packages`](https://github.com/grafana/grafana/tree/a20530df7c32a7752a5e8cd0c765f812651eab73/packages).

- Syncthing keeps its embedded GUI under [`gui`](https://github.com/syncthing/syncthing/tree/946e2b83a1f6c6ae119427c09e0a5802940b82ff/gui), then generates compiled asset packages ([generation](https://github.com/syncthing/syncthing/blob/946e2b83a1f6c6ae119427c09e0a5802940b82ff/build.go#L1124-L1155)).

- k6 loads dashboard assets from a separate module rather than maintaining frontend source in the server repository ([assets](https://github.com/grafana/k6/blob/53b5727d893d30a5c73e5b1a9891283786e0ec44/internal/dashboard/assets.go#L17-L31)).

Choose `ui`, `web`, `frontend`, or another directory from toolchain ownership, publication boundaries, and embedding behavior. A nested frontend `src` is unrelated to redundant Go `src` layouts.

### Compatibility commitments justify otherwise unusual boundaries

Helm explicitly separates supported packages under [`pkg`](https://github.com/helm/helm/tree/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/pkg) from developing implementations under [`internal`](https://github.com/helm/helm/tree/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/internal) and documents the compatibility consequence ([guidance](https://github.com/helm/helm/blob/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/AGENTS.md#L17-L40)). k6 retains a public `cmd.Execute` wrapper for backward compatibility and extension builds while new command composition lives under `internal/cmd` ([wrapper](https://github.com/grafana/k6/blob/53b5727d893d30a5c73e5b1a9891283786e0ec44/cmd/execute.go#L1-L17)).

Treat these as compatibility designs. Do not reproduce them without the same public API or customization obligation.

### Generated code and migrations stay with an explicit owner

Syncthing commits protobuf and other generated files under the package that consumes them and keeps SQLite SQL under its SQLite adapter ([generated code](https://github.com/syncthing/syncthing/tree/946e2b83a1f6c6ae119427c09e0a5802940b82ff/internal/gen), [SQLite SQL](https://github.com/syncthing/syncthing/tree/946e2b83a1f6c6ae119427c09e0a5802940b82ff/internal/db/sqlite/sql)). Gitea and Grafana implement ordered migrations in Go under dedicated migration capabilities ([Gitea migrations](https://github.com/go-gitea/gitea/blob/6347a33b34f501ef5f788948cb9742fb046f6af5/modelmigration/migrations.go), [Grafana migrations](https://github.com/grafana/grafana/blob/a20530df7c32a7752a5e8cd0c765f812651eab73/pkg/services/sqlstore/migrations/migrations.go)). Helm embeds PostgreSQL migration statements inside its concrete driver ([SQL driver](https://github.com/helm/helm/blob/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/pkg/storage/driver/sql.go#L113-L220)).

These are tool- and product-specific strategies. Require deterministic generation or migration order, clear ownership, and tests; do not impose one asset directory.

### Generic names remain contextual

The audited repositories contain names such as `model`, `store.go`, `helpers.go`, `types.go`, `util.go`, and `common.go`. Some own clear concepts; others are historical residue. For example, Helm's [`storage/driver/util.go`](https://github.com/helm/helm/blob/ae877c8bfb943d2cc1aa10b34f0c4fada55e6f56/pkg/storage/driver/util.go#L22-L103) owns release encoding and driver-label helpers inside a precise package, while Gitea's broad [`modules/util`](https://github.com/go-gitea/gitea/tree/6347a33b34f501ef5f788948cb9742fb046f6af5/modules/util) is weak greenfield precedent.

Read declarations and package responsibility before judging a file. Repository existence proves legitimacy under that repository's constraints, not quality as a general default.

## Specialized cautions

- Syncthing's `lib`, custom build tool, generated GUI, multiple servers, protocol compatibility, and platform-specific code are specialized.

- Gitea's `models`, `modules`, `routers`, `services`, and generic helper packages reflect a large inherited application and should not become a stock layer scheme.

- Grafana's `pkg/cmd`, `apps`, `public/app`, Go workspace, and generated platform APIs reflect a large hybrid monorepo.

- k6's broad importable surface and public command wrapper support an extension ecosystem and compatibility history.

- Helm's `pkg` boundary, action configuration, chart-version adapters, plugins, and storage drivers reflect a supported SDK and Kubernetes compatibility obligations.

## Required decision procedure

For full-stack or multi-binary layout decisions:

1. List shipped binaries, deployment units, repository tools, generators, fixtures, and subcommands separately.

2. Identify supported importable APIs and custom-binary or plugin commitments.

3. Identify each non-Go toolchain and its source, generated output, and embedding or deployment owner.

4. Locate composition roots and record which dependencies they assemble.

5. Separate compatibility-preserving structure from recommended greenfield structure.

6. Treat `pkg`, `lib`, `apps`, `modules`, and similar directories as repository-specific until their support contract is documented.

7. Keep generated code and migrations with a named owner and deterministic verification path.

8. Cite analogous pinned files and at least one credible alternative before settling a disputed boundary.

## What this category does not establish

This category does not establish one preferred layer architecture, frontend directory, migration system, public-package directory, or executable placement. Use it only after matching the target project's product shape and compatibility obligations.
