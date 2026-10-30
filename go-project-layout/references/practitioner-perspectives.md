## Purpose

Use practitioner writing to expose trade-offs, test a tentative recommendation, or identify failure modes. Do not treat agreement among essays as a Go rule or as a substitute for current official behavior and closely analogous inspected repositories.

## Active perspectives

### Rakyll: package responsibility and discoverability

[Style guideline for Go packages](https://rakyll.org/style-packages/) contributes a caller-facing lens: keep types near their use, organize packages by responsibility, test names through client expressions and documentation, and add examples when package relationships are unclear.

Keep it because it connects layout to discoverability and API consumption. Treat its pluralization, vanity import, `src`, and `pkg` statements as historical or contextual because parts reflect GOPATH-era practice.

### Laurent Schwartz: adversarial simplicity check

[No nonsense guide to Go projects layout](https://laurentsv.com/blog/2024/10/19/no-nonsense-go-package-layout.html) challenges unnecessary `internal`, `cmd`, `pkg`, utility packages, and premature splitting.

Keep it as a counterweight to over-structuring. Do not use its numerical or categorical claims as evidence. Use it to ask whether a boundary solves a current problem or merely follows convention.

### Ben Johnson: dependency-oriented structure

[Standard Package Layout](https://www.gobeyond.dev/standard-package-layout/) presents domain types, adapters, explicit wiring, and a small composition root. Use it when dependency isolation is required. Do not treat root-domain purity or adapter direction as universal Go policy.

### Dave Cheney: cohesion and process state

[Avoid package names like base, util, or common](https://dave.cheney.net/2019/01/08/avoid-package-names-like-base-util-or-common) supplies a caller-oriented cohesion test.

[Go, without package scoped variables](https://dave.cheney.net/2017/06/11/go-without-package-scoped-variables) exposes hidden registries, import-time effects, lifecycle coupling, and test contamination. Use it to trigger review, not to ban every package variable.

### Mat Ryer: optional process seam

[Why you should not use func main in Go](https://pace.dev/blog/2020/02/12/why-you-shouldnt-use-func-main-in-golang-by-mat-ryer.html) demonstrates a same-package `run` function that accepts process inputs and returns errors. Use it when that seam improves testing. Do not infer that every command needs `run.go`, `cmd`, or `app`.

### Redowan Delowar: domain-oriented alternative

[Let the domain guide your application structure](https://rednafi.com/go/app-structure/) provides a domain-oriented alternative to technology-layer buckets. Its dependency direction is an architectural preference, not a Go rule.

### Alex Edwards: incremental growth

[Eleven tips for structuring your Go projects](https://www.alexedwards.net/blog/11-tips-for-structuring-your-go-projects) supports starting small and adding boundaries as requirements emerge. Use it as corroboration, not proof.

### Jeremy Bowers: cycle diagnosis and persistent diagrams

[Go layered design](https://jerf.org/iri/post/2025/go_layered_design/), published 2025-04-14, contributes a fine-grained cycle diagnosis and a rough preference order for six remedies. Use it as a practitioner heuristic after establishing the specification's acyclic-import rule. Let current ownership, package depth, copy size, and resulting merge size select the remedy.

Bowers partly justifies single-type packages through predicted growth. Apply this guide's active-horizon rule instead: current project-specific evidence must establish the boundary.

[On layers and boxes and lines](https://jerf.org/iri/post/2025/on_layers_and_boxes_and_lines/), published 2025-05-06, recommends spatial order with defined meaning and diagrams that lead readers into prose and code. Use that advice for persistent architecture documentation. Treat its entity-count ranges as practitioner judgment without measured support.

## Historical context

[Five suggestions for setting up a Go project](https://dave.cheney.net/2014/12/01/five-suggestions-for-setting-up-a-go-project) remains useful for caller-oriented naming and historical entry-point alternatives. Do not present its GOPATH-era advice as current module guidance.

## Use rule

1. Establish Go-enforced behavior and current official guidance first.
2. Use practitioner sources to identify trade-offs and challenge assumptions.
3. Use inspected pinned repositories to test patterns under analogous constraints.
4. Label the final choice as style guidance, contextual precedent, project judgment, or unresolved.
