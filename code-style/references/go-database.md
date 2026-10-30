# Go and database/sql

These rules prevent real bugs (leaked connections, lost errors, SQL injection), so they are **MUST** unless marked otherwise. Source: [database/sql](https://pkg.go.dev/database/sql) and the [Go database tutorial](https://go.dev/doc/database/index).

## Correctness

- Use the context-aware methods: `QueryContext`, `QueryRowContext`, `ExecContext`, `BeginTx`.
- Close `*sql.Rows` on every path. Defer `Close` after checking the query error, as every official example does. Iterating to the end closes the rows too, but a return before the end leaks the connection. On a query that can write, check the `Close` error.
- Check `rows.Err()` after the loop; `Next` returns false both at the end and on failure.
- Branch on `sql.ErrNoRows` with `errors.Is`; the official examples use `==`, which breaks once a driver wraps the error. `QueryRowContext` reports its error from `Scan`.
- Pass runtime values as parameters. Identifiers and sort directions come from an allowlist or validated construction, never from string concatenation.
- Use the placeholder syntax of the driver in use.
- Scan nullable columns into a type that accepts null: `sql.Null[T]` (Go 1.22), `sql.Null*`, a pointer, or a `sql.Scanner`.
- Inside a transaction, run every related statement on the `*sql.Tx`. A `Tx` is bound to one connection; a statement on the `*sql.DB` takes another and cannot see uncommitted work.
- Never carry a pool or transaction in a `context.Context`.
- Do not rely on `LastInsertId` or `RowsAffected` without confirming the driver supports them.

## Defaults

- A `*sql.DB` is a long-lived pool: open it once at startup, configure it, and pass it in. Never open one per request. Size `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`, and `SetConnMaxIdleTime` from the workload and server limits; the defaults are unlimited open and two idle.
- `PingContext` at startup when readiness needs a live connection; `Open` may not connect.
- Define the interface over a pool or transaction in the consuming package, with only the methods it calls.
- The workflow that begins a transaction owns it: defer a rollback, commit on success, and check the commit error. Functions called inside it take the `*sql.Tx` and never commit it.
- Test persistence and migrations against the real database engine.
