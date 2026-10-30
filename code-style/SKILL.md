---
name: code-style
description: Opinionated code design, implementation, review, refactoring, documentation, and testing guidance for Python and Go. Apply when writing or reviewing functions, methods, tests, comments, errors, concurrency, dependency boundaries, or source organization within an established package structure.
---

Read [references/principles.md](references/principles.md) for every task. For Python, also read [references/python.md](references/python.md). For Go, also read [references/go.md](references/go.md), and for Go code using `database/sql`, [references/go-database.md](references/go-database.md).

This skill covers code inside an established package structure. It states the layering property (principle 9); deciding where code lives, and moving it across modules, packages, or distributions, belongs to the project-layout skills.

## Precedence

1. Correctness and safety.
2. Public compatibility and documented behavior.
3. The repository's own instructions, architecture, framework contracts, and configured tools.
4. The owner's stated preferences, including ones newer than this file.
5. This guide.

When two rules in this guide conflict and correctness is not at stake, write the version the next reader, who lacks your context, understands fastest. An owner preference that contradicts a repository convention is a reason to change this guide; raise it rather than overriding the repository in one change.

## How binding the rules are

Rules marked **MUST** are few and hard: depart only when a higher item above requires it, and say so. Everything else is the default: follow it so that code written by different people and agents converges, and depart for a concrete reason you can state in one sentence. Do not depart for taste alone.

## Changing this skill

The owner's preference is enough to change any rule. When you notice a rule that produced worse code, a contradiction, a factual error, or an official source the guide should restate, say so and propose the edit; do not apply it silently.

## Working on code

1. Read the repository's guidance, conventions, and language version first.
2. Preserve behavior and public contracts unless the task changes them.
3. Separate effects from logic before deciding what to extract, and do not extract or inline code to satisfy a slogan.
4. Prefer the smallest coherent change. Do not reorder or restyle untouched code during unrelated work.
5. Run the repository's checks after changing code.
6. Report conflicts you could not resolve instead of choosing silently.
7. Do not apply these rules to generated, vendored, migration, or framework-controlled code.

## Reviewing code

Lead with correctness, hidden dependencies, effects mixed into logic, misleading abstractions, concurrency and ownership defects, and weak tests; style comes last. Separate findings the change introduced from pre-existing ones, and never block a change on a pre-existing finding. A finding about nesting or length must name the comprehension, correctness, or testing problem it causes. For a formal review, give each finding its location, severity (blocker, major, moderate, minor), whether the change introduced it, the exact fix, and the one-sentence reason.
