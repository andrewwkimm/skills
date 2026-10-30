## Purpose

Use this reference only when a repository has independently versioned APIs, many production binaries, generated public APIs, plugins, cross-platform implementations, or system-level test infrastructure. Kubernetes and containerd are controls against overgeneralization, not general templates.

## Audit set

|Repository|Audited revision|Date|Product shape|Corpus role|
|---|---|---|---|---|
|[Kubernetes](https://github.com/kubernetes/kubernetes/tree/b037c6852709aa22e06432a1bf90275ea510467f)|[`b037c68`](https://github.com/kubernetes/kubernetes/commit/b037c6852709aa22e06432a1bf90275ea510467f)|2026-08-03|Distributed-system monorepo with many binaries, staged public modules, generated APIs, plugins, and large test suites|Specialized precedent|
|[containerd](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234)|[`1a34bf3`](https://github.com/containerd/containerd/commit/1a34bf320a4fd858c9987b4a8d9fdca22adf4234)|2026-08-03|Cross-platform runtime with daemon, tools, shims, public client and RPC APIs, plugins, and privileged integration tests|Specialized precedent|

## Legitimately reusable findings

### Multiple real binaries justify `cmd/<binary>`

Kubernetes keeps separate thin entry points for production components such as [`kube-apiserver`](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/cmd/kube-apiserver/apiserver.go#L13-L29) and [`kube-controller-manager`](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/cmd/kube-controller-manager/controller-manager.go#L13-L32). containerd's build identifies several distinct executables under [`cmd`](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/cmd).

Use this pattern for independently built or deployed programs. Do not create a directory per subcommand.

### Separate modules require independent lifecycle or support reasons

Kubernetes stages authoritative modules for coordinated publication and binds them through its workspace and replacement machinery ([staging policy](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/staging/README.md#L1-L48)). containerd separates its supported RPC API into an independently versioned [`api` module](https://github.com/containerd/containerd/blob/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/api/go.mod).

Create another module only for a concrete release, versioning, dependency, or compatibility boundary. Repository size alone is insufficient.

### Support policy, not directory name, defines public API

Kubernetes documents external consumption and compatibility for [`client-go`](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/staging/src/k8s.io/client-go/README.md#L5-L59). containerd documents stability for its client, API module, and selected packages while excluding other prominent directories in [`RELEASES.md`](https://github.com/containerd/containerd/blob/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/RELEASES.md).

A `pkg` directory does not create visibility or compatibility. An explicit support contract does.

### Generated public APIs need ownership and reproducibility

Kubernetes gives staged APIs explicit ownership and code-generation contracts ([API ownership](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/staging/src/k8s.io/api/OWNERS), [code generator](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/staging/src/k8s.io/code-generator/README.md#L5-L22)). containerd keeps protocol sources and generated bindings inside its separately versioned [`api`](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/api) boundary.

Commit generated code when distribution, compatibility, consumer builds, bootstrap constraints, generator availability, or reviewability requires it. Require deterministic generation where feasible, clear ownership, documented regeneration, and CI freshness checks.

### Extra dependency controls are justified only beyond Go visibility

Kubernetes applies repository-specific import allowlists to staged modules where `internal` cannot express the cross-module policy ([restrictions](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/staging/publishing/import-restrictions.yaml#L36-L88)). Ordinary repositories should rely on package design and `internal` before inventing policy machinery.

### Platform and test structure should follow materially different behavior

Kubernetes isolates Linux and Windows implementations behind build constraints ([Linux](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/pkg/kubelet/kubelet_server_journal_linux.go#L1-L28), [Windows](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/pkg/kubelet/kubelet_server_journal_windows.go#L1-L28)). containerd separates platform build concerns and privileged integration suites because the runtime requires them ([integration](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/integration)).

Add platform files, integration binaries, or privileged suites only when behavior and execution requirements differ.

## Patterns to ignore for ordinary projects

- Kubernetes' broad [`pkg`](https://github.com/kubernetes/kubernetes/tree/b037c6852709aa22e06432a1bf90275ea510467f/pkg) tree is historical implementation organization, not a public API marker.

- containerd's [`pkg`](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/pkg), [`core`](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/core), and [`plugins`](https://github.com/containerd/containerd/tree/1a34bf320a4fd858c9987b4a8d9fdca22adf4234/plugins) reflect a mature runtime architecture and written compatibility obligations.

- Kubernetes staging, publishing bots, generated workspaces, and replacement files serve coordinated multi-repository publication.

- Large generated-code volume is justified by public API distribution, not repository size.

- Kubernetes' reusable E2E framework explicitly carries historical baggage and discourages downstream use ([warning](https://github.com/kubernetes/kubernetes/blob/b037c6852709aa22e06432a1bf90275ea510467f/test/e2e/framework/README.md#L1-L30)).

- containerd's failpoint shims, root-required suites, CRI harnesses, and cleanup machinery are runtime-specific.

## Required use

Consult this reference only after confirming that the target project has a matching exceptional constraint. Prefer focused application and library evidence for ordinary projects. Never cite Kubernetes or containerd merely because a repository is expected to become large.
