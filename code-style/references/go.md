# Go

Read the principles first; this file says how they look in Go and adds what is specific to Go. Go has strong, shared idioms, so write the code an experienced Go reviewer expects. Where a principle and an official Go rule disagree, the Go rule wins.

A tag in parentheses names the source a rule restates: **CRC** is [Code Review Comments](https://go.dev/wiki/CodeReviewComments), **EG** is [Effective Go](https://go.dev/doc/effective_go), **TC** is [Test Comments](https://go.dev/wiki/TestComments), **DC** is [Go Doc Comments](https://go.dev/doc/comment), **Uber** is [Uber's guide](https://github.com/uber-go/guide/blob/master/style.md). An untagged rule is a house rule. "Departs from" marks a deliberate house rule against a named source.

## Sources and versions

Rank sources in this order:

1. The toolchain: the language spec, release notes, package docs, and what `gofmt`, `go vet`, `go fix`, and gopls report.
2. The repository's conventions.
3. Current official guidance: package docs, Doc Comments, Test Comments, Code Review Comments, and the Go Blog.
4. Effective Go. It is "not actively updated" and predates modules, generics, and `errors.Is`; its core-language advice stands, but newer official sources win where they disagree.
5. The [Google Go Style Guide](https://google.github.io/styleguide/go/), which Code Review Comments names as its longer discussion, for rationale when an official rule needs explaining. Uber supplies the individual rules tagged Uber below and nothing else; its `_` prefix on unexported globals, 99-column limit, and `go.uber.org/atomic` (superseded by typed `sync/atomic` in Go 1.19) are not adopted.

When a rule here and a repository's practice differ and no source settles it, look at how [tailscale](https://github.com/tailscale/tailscale) and [litestream](https://github.com/benbjohnson/litestream) do it; both are idiomatic, current, and tested with the standard library.

The `go` directive in the main module's `go.mod` sets the language version and the [GODEBUG defaults](https://go.dev/doc/godebug), so it decides whether a version-dependent rule applies. Read it first, and do not apply a rule a newer release made unnecessary.

## Tooling

`gofmt`, `go vet`, `go fix`, gopls, and any linter the repository configures are authoritative for what they check (`go tool vet help`, `go tool fix help`). This guide does not restate their checks and MUST NOT contradict them. Do not revert their fixes or report findings they would resolve.

- Format with `gofmt` or `goimports`; rearrange code rather than working around the formatter. (CRC, EG)
- Run `go vet ./...` even when `go test` passes: `go test` runs ten of vet's checks.
- Before reporting done, run `go fix -diff` on changed packages and apply the hunks on lines you wrote. After a toolchain upgrade, run `go fix ./...` from a clean tree until it changes nothing, as its own commit. (Go 1.26 `go fix`)
- With gopls MCP tools, follow `gopls mcp -instructions`: `go_diagnostics` after each edit, a vulnerability check at the start and after dependency changes. Without them: `go build ./...` and `go vet ./...` after edits, `go test` on changed packages while iterating, `govulncheck ./...` after dependency changes if installed.
- Run `go test ./...` (with `-race` when concurrency is involved) once before reporting done, or as the repository's checks direct.
- gopls's "Add methods to T to implement an interface" action (v0.23+) generates `panic("unimplemented")` bodies; replace every one.

## Formatting and imports

- Group imports: standard library, then everything else, then the repository's own packages when its tooling does that. (CRC)
- Alias an import only to resolve a collision, renaming the most local or project-specific import (CRC), or when the package name differs from the last element of its import path (Uber).
- No dot imports except in a test that cannot live in the package it tests. Blank imports (`import _ "pkg"`) only in `main` or tests. (CRC)
- No fixed line length. Break a long line where the meaning splits, not at a column. (CRC, EG)

## Names

- Package names are short, lowercase, single words that say what the package provides. (EG) Avoid `util`, `common`, `misc`, `api`, `types`, `interfaces`, and `helpers`, and do not repeat the package name in exported names (`http.Server`, not `http.HTTPServer`). (CRC, [Package names](https://go.dev/blog/package-names))
- `MixedCaps` everywhere, including constants: `maxLength`, not `MAX_LENGTH`. (CRC) Test functions may use one underscore to group cases: `TestParse_Empty`. (Uber)
- Initialisms keep one case: `userID`, `HTTPClient`, `urlPony`, `xmlHTTPRequest`. Protobuf-generated code is exempt. (CRC)
- Name length follows scope: short in a few lines, descriptive for values that live longer. (CRC)
- Receivers are short, usually one or two letters, the same on every method, never `this` or `self`. (CRC)
- Do not shadow predeclared identifiers such as `len`, `new`, `error`, or `any`. (Uber)
- No `Get` on a plain accessor (`Owner()`); setters are `SetOwner`. (EG)
- Constructors are `New` when the package exports only that type, otherwise `NewThing`. (EG)
- Methods with a standard meaning (`Read`, `Write`, `Close`, `Flush`, `String`) keep the standard signature; call it `String`, never `ToString`. (EG)
- One-method interfaces often take the method name plus `-er`. (EG)

## Types, values, and construction

- Make the zero value useful when that is natural. (EG) When it cannot be, use unexported fields and a constructor that returns a valid value or an error.
- A constructor that acquires a resource returns something with a `Close` and says so in its doc comment.
- Accept interfaces, return concrete types. Define an interface in the package that uses it, with only the methods it calls, and only once a real consumer needs it; never on the implementing side "for mocking". (CRC) When a type exists only to implement an interface, its constructor returns the interface, as `crc32.NewIEEE` returns `hash.Hash32`. (EG)
- Add `var _ I = (*T)(nil)` only for an interface the type must satisfy by contract and nothing in the code already converts. (EG, Uber)
- Never return a nil concrete pointer through an interface; declare `error` and other interface results as the interface type. ([FAQ](https://go.dev/doc/faq#nil_error))
- Use the comma-ok form of a type assertion unless a panic on the wrong type is the intended behavior. (EG, Uber)
- Struct literals: keyed fields when positional meaning is not obvious (`go vet` checks imported types); omit zero-value fields; `var x T` for an all-zero value; `&T{}` rather than `new(T)`; `make` for a map filled later. (Uber) Tag the fields of a struct that defines a wire contract, so a rename cannot change the format. (Uber)
- Embed a type only when every promoted method belongs on the outer type and no user-facing behavior changes; put embedded fields first and never embed a mutex. Embedding in an exported struct makes the inner type part of your API, as `bufio.ReadWriter` does on purpose. (Uber, EG)
- Do not copy a value of a type whose methods are on the pointer, such as `bytes.Buffer`. (CRC)
- Do not pass pointers to save bytes: pass `string`, not `*string`, and pass small structs that will not grow by value. (CRC)
- Do not design an API that treats a nil slice and an empty slice differently; return nil by default and test emptiness with `len(s) == 0`. JSON is the known exception: nil encodes as `null`, `[]T{}` as `[]`. (CRC, Uber)
- Start an enum at one unless zero is the meaningful default. (Uber)
- Use `crypto/rand` (`rand.Text` since Go 1.24) for keys, tokens, and anything secret; never `math/rand`. (CRC)
- Package-level values are fine when they are effectively constant: lookup tables, `regexp.MustCompile` patterns, sentinel errors. Avoid mutable package state, including function variables that tests reassign (`var timeNow = time.Now`); pass the function as a field or parameter. (Uber) Prefer a library's instance API to its package-level configuration.
- Avoid `init`. When registration or deterministic precomputation requires one, it MUST be deterministic and MUST NOT perform I/O, read environment or process state, start goroutines, or depend on another `init`. (Uber's "should", made MUST; departs from EG, whose `init` depends on environment variables and calls `log.Fatal`)

## Functions and methods

- Keep decisions in functions that take values and return values; keep I/O at the edges (principle 1). Accept the narrowest input: an `io.Reader` rather than a filename, rows rather than a client.
- Pointer receivers when a method mutates, the value is large, it contains a `sync` value, or identity matters; when in doubt, use a pointer. No pointer receiver on a map, func, chan, or a slice the method does not reslice. (CRC) Do not mix pointer and value receivers on one type. (CRC, FAQ) The one exception is pointer-receiver decode methods on a value type, as `time.Time` does. (Departs from CRC.)
- A method uses its receiver, satisfies an interface, or is a deliberate extension point; otherwise write a function.
- Functional options suit constructors with several optional settings that will grow; required dependencies and small fixed sets are plain parameters. (Uber)
- Name results when two have the same type, the meaning is not clear from context, or a deferred function must change one; do not name them only to allow a bare `return`, and use bare returns only in short functions. (CRC)

## Control flow

- Handle errors and edge cases first and return early; no `else` after a branch that returns. (CRC, EG) When an `if` with an init statement would need an `else`, declare the variable on its own line instead. (CRC)
- Prefer `switch` to long `if`/`else` chains. (EG) `break` inside `switch` or `select` leaves only that statement; use a label to leave a loop. (spec, EG)
- Watch for `:=` shadowing an outer variable, especially `err`, in an inner block.
- `defer` runs when the function returns, and its arguments are evaluated when `defer` runs. (EG) Move a loop body that defers into its own function.
- Do not split a long function only because of its length. (CRC)

## Errors

- Return errors for ordinary failures. (CRC) Panic only for programmer errors, impossible states, or failed initialization such as `template.Must`. (EG, Uber) Call `os.Exit` or `log.Fatal` only in `main`, at most once; put the logic in a `run() error`. (Uber)
- Do not use Effective Go's package-internal panic and recover pattern; return errors from each level. (Departs from EG, the Go wiki, and Google.) Call `recover` only at a boundary that can restore a defined invariant or turn a panic into controlled process behavior.
- Add context as you return: `fmt.Errorf("load customer %q: %w", id, err)`. Wrapping with `%w` makes the cause part of your API; use `%v` when callers should not depend on it, and return the error unchanged when there is nothing to add. ([Go 1.13 errors](https://go.dev/blog/go1.13-errors), Uber) The verbs format identically ([fmt](https://pkg.go.dev/fmt)); remove sensitive detail explicitly.
- Error strings start lowercase unless they begin with a proper noun or acronym, have no trailing punctuation (CRC), and say what failed without "failed to" (Uber). Prefix with the package or operation when feasible: `image: unknown format`. (EG) These rules do not apply to log messages. (CRC)
- Inspect wrapped errors with the `errors` package; never compare error strings. Export a sentinel (`ErrNotFound`) when callers need identity, an error type (`NotFoundError`) when they need fields. (Uber)
- Do not signal failure in-band; return a final `bool` or `error`. `nil`, `""`, `0`, and `-1` are fine when they are valid results. (CRC)
- Handle an error once: either log it or return it. (Uber)
- Discard an error with `_` only beside a comment that says why it cannot occur or cannot change the outcome. (Departs from CRC and EG.)
- Check errors from cleanup that can lose data: `Close` on a written file, `Flush`, `Commit`. Combine a cleanup error with the primary one rather than replacing it.

## Resources

- Close what you open on every path: response bodies, `*sql.Rows`, files. Defer the close after checking the error that would leave the value nil, so the close sits beside the open. (EG)
- Stop a ticker or timer that is still referenced or long-lived. In a module on `go 1.23` or later, an unreferenced one is collected without `Stop`. ([Go 1.23](https://go.dev/doc/go1.23))

## Context

- A request-scoped `ctx context.Context` is the first parameter, never a struct field. (CRC, [context](https://pkg.go.dev/context)) A type that owns a long-lived goroutine may hold the context and cancel func that bound that goroutine's life, set in `Start` and canceled in `Close`; so may a method whose signature must match an existing interface. (Departs from CRC's wording; matches tailscale and litestream.)
- Never pass `nil`; use `context.TODO()` while plumbing is unfinished. Default to passing a context; use `context.Background()` directly only when the alternative is a mistake. (context, CRC)
- Do not swap in `context.Background()` to escape cancellation. When work must outlive the request, derive from `context.WithoutCancel` (Go 1.21) and say why in a comment.
- No custom `Context` types and no substitute interfaces in signatures. (CRC)
- Context values carry request-scoped data across API boundaries, keyed by an unexported package type and read through a typed accessor; never use them as a parameter bag. (context)
- The code that owns a latency budget sets the timeout.

## Slices, maps, and strings

- `append` may share the backing array with its input; copy before storing or returning a slice a caller can still mutate, and do not retain a caller's slice or map unless that is the contract. (Uber)
- `range` copies each element; mutate through the index or a pointer.
- Index a string by bytes, range over it by runes. `TrimRight` trims a set of characters; `TrimSuffix` removes a suffix.
- Decoding JSON into `map[string]any` turns every number into `float64`; decode into a struct, or use `json.Number`.

## Time

- Store durations as `time.Duration`. When a wire format forces a number, put the unit in the field name. (Uber)
- Build a wall-clock time on a date with `time.Date` in the right location; adding a duration to midnight is wrong across daylight-saving changes, so test such logic on a transition date.
- Pass a clock to code whose behavior depends on the time rather than reading `time.Now` inside it.

## Concurrency

- Prefer synchronous functions; let the caller add concurrency. (CRC)
- Every goroutine has an owner, a way to stop, and a way to report its error (Uber); make clear when or whether it exits (CRC). Bound how many goroutines a loop or server can start. (EG)
- Use `errgroup` for goroutines that can fail together.
- Share memory by communicating where it fits, but a mutex beside the fields it guards is often simpler. (EG) A zero-value mutex is valid; keep it a plain field. (Uber)
- The sender closes a channel. Give a channel a buffer only when the protocol fixes its size. (Uber)
- In a module on `go 1.25` or later, do not set `GOMAXPROCS` or import `automaxprocs`: on Linux the runtime follows the container's CPU limit, and setting it by hand turns that off. Reading `runtime.GOMAXPROCS(0)` to size a pool is fine. ([Go 1.25](https://go.dev/doc/go1.25))

## HTTP

- Never call external services with `http.DefaultClient` or `http.Get`, which have no timeout. Build a client with a `Timeout` once and reuse it.
- Servers set read, write, and idle timeouts.
- `return` after `http.Error`; it does not stop the handler.

## Comments and documentation

Go reads its documentation from the source, so doc comments are part of the API, but not everything needs a comment.

- Every package and exported name has a doc comment, and so do non-trivial unexported types and functions. (CRC) Write full sentences ending in a period that begin with the name. (CRC, DC)
- A package comment begins "Package x", sits directly above the package clause with no blank line, and appears in one file; a command's begins with the program name or "Command name". (CRC, DC)
- A type's comment says what an instance represents; document exported struct fields. (DC) A function returning a boolean "reports whether". (DC) Mark deprecation with a `Deprecated:` paragraph that names the replacement. (DC)
- Document what a caller cannot see: special cases, zero-value behavior, and concurrency safety where it differs from the default (a type is assumed safe for one goroutine at a time, a top-level function for concurrent use), per method if the type comment does not cover it. Keep implementation details out. (DC) Also state units, ownership and mutation, blocking, cleanup duties, and the errors returned.
- Comment unexported code when it holds a reason, a constraint, or an invariant. The principles' rule against history in comments applies.
- A new package includes an example of intended use, or a test showing a complete call sequence. (CRC)

## Tests

- Follow the repository's assertion style and do not convert a file between styles in an unrelated change. (Uber, "Be Consistent")
- In a repository without an assertion library, use `testing` with `cmp.Diff` for structured values, and do not add `testify`. (TC) Where the repository already uses `testify`, keep it: `require` when the rest of the test cannot run, `assert` for independent checks, `cmp.Diff` for structs, no `testify/suite`, and `testifylint` when golangci-lint runs. (Departs from TC for existing suites; 15 of 20 large Go projects depend on testify.)
- Prefer `cmp.Equal` and `cmp.Diff` to `reflect.DeepEqual`. (TC)
- Table-driven tests with `t.Run` for cases that share testing logic; separate test functions when the logic differs, and one table for success and one for errors when that is clearer. (TC) No branching on mock expectations or functions inside the table. (Uber) Name cases for the condition, never by index, and keep names readable after escaping. (TC)
- Keep going after a failure: `t.Error` plus `continue` outside `t.Run`, `t.Fatal` inside a subtest or when setup fails. (TC)
- Failure messages name the function and show input, got, then want: `Parse(%q) = %v, want %v`; label diffs `(-want +got)` and pass `cmp.Diff(want, got)` in that order. Compare whole structs at once, and do not compare exact `json.Marshal` output or anything else a dependency may change. (TC)
- Use `t.Helper()` in helpers that fail the test (TC), and `t.Cleanup`, `t.TempDir`, `t.Setenv`, and `t.Context()`. `t.Context()` is canceled before cleanup functions run, so do not use it inside `t.Cleanup` ([Go 1.24](https://go.dev/doc/go1.24)); `t.Setenv` cannot be used with `t.Parallel`. ([testing](https://pkg.go.dev/testing))
- Prefer real implementations and small hand-written fakes. Give fakes a failure mode and test the failures the code promises to handle. Do not define an interface on the implementing side only to mock it. (CRC) Use `testify/mock` or a generated mock only when the interaction itself is the behavior under test.
- Never synchronize with `time.Sleep`; wait on a channel or inject the clock. Use `httptest` for HTTP, and `t.Parallel` only for tests that share no state.
- Fuzz parsers and decoders; benchmark only work tied to a real workload, with `b.Loop` (Go 1.24).
