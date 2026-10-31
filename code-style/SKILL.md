---
name: code-style
description: Opinionated code design, implementation, review, refactoring, documentation, and testing guidance for Python and Go. Apply when writing or reviewing functions, methods, types, tests, comments, errors, concurrency, pipeline tasks, dependency boundaries, or source organization within an established package structure.
---

Read [references/principles.md](references/principles.md) for every task. For Python, also read [references/python.md](references/python.md). For Go, also read [references/go.md](references/go.md), and for Go code using `database/sql`, [references/go-database.md](references/go-database.md). Read [references/decisions.md](references/decisions.md) only when you are about to propose a change to this skill or when a user questions a rule.

This skill covers code inside an established package structure. It states the layering property (principle 10); deciding where code lives, and moving it across modules, packages, or distributions, belongs to the project-layout skills.

## Precedence

1. Correctness and safety.
2. Public compatibility and documented behavior.
3. The repository's own instructions, architecture, framework contracts, and configured tools.
4. The owner's stated preferences, including ones newer than this file.
5. This guide.

When two rules in this guide conflict and correctness is not at stake, write the version the next reader, who lacks your context, understands fastest. An owner preference that contradicts a repository convention is a reason to change this guide; raise it rather than overriding the repository in one change.

## How binding the rules are

Rules marked **MUST** are few and hard: depart only when a higher item above requires it, and say so. Everything else is the default: follow it so that code written by different people and agents converges, and depart for a concrete reason you can state in one sentence. Each rule carries its reason; when the reason does not apply to the case in front of you, say so and do what the reason would want. Do not depart for taste alone.

## Working on code

1. Read the repository's guidance, conventions, and language version first.
2. Preserve behavior and public contracts unless the task changes them.
3. Before writing, name the unit of work and its inputs, separate the effects from the decisions, and search for the terms and helpers the code already uses. Decide what each missing or bad input does.
4. Prefer the smallest coherent change. Do not reorder or restyle untouched code during unrelated work.
5. Run the repository's checks after changing code.
6. Report the calls you made under a default that could have gone another way, in one line each. Report conflicts you could not resolve instead of choosing silently.
7. Do not apply these rules to generated, vendored, migration, or framework-controlled code.

## When to stop and ask

Decide and state the call for anything this guide or the repository already answers. Stop and ask before:

- changing a public contract: an exported signature, a wire format, a table schema, a CLI flag;
- destroying or rewriting data, or any change that cannot be rolled back by reverting the commit;
- following the repository where it contradicts this guide in a way that would spread (a new module copying a pattern the guide rejects), rather than in one line;
- a task whose scope would grow past the ticket to satisfy a rule (a rename across the codebase, a cycle fix that moves modules).

## Reviewing code

Lead with correctness, hidden dependencies, effects mixed into logic, misleading abstractions, concurrency and ownership defects, non-idempotent writes, and weak tests; style comes last. Separate findings the change introduced from pre-existing ones, and never block a change on a pre-existing finding. A finding about nesting or length must name the comprehension, correctness, or testing problem it causes. For a formal review, give each finding its location, severity (blocker, major, moderate, minor), whether the change introduced it, the exact fix, and the one-sentence reason.

## Changing this skill

The owner's preference is enough to change any rule. A change you propose yourself must fix a factual error (cite the primary source), resolve a contradiction between rules, or prevent an outcome you observed and can describe; preference is not enough, because a permission granted to an agent is used constantly while a denied one surfaces in review. Before proposing, read [references/decisions.md](references/decisions.md): a question settled there is reopened only with new evidence of one of those three kinds, and a user questioning a settled rule gets the recorded reasoning, not a reversal. Propose edits; do not apply them silently. A change that adds, removes, or rewords a rule is checked with the benchmark that ships beside this skill (`../code-style-benchmark/`, see its README), with enough runs per variant that the difference exceeds the spread between runs.
