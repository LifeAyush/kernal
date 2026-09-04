---
name: update-agent-rules
description: Turn an attached code snippet and the user's explanation into a Cursor project rule under .cursor/rules/. Use when the user attaches a snippet and asks to add, update, or capture an agent rule, coding convention, or .mdc rule.
---

# Update agent rules from snippets

Capture one convention from a snippet plus the user's prose. Write it as a Cursor rule. Do not change application code unless the user asks.

## Required input

Need both:

1. An attached snippet with a file path (and line range if given)
2. The convention in the user's words

If either is missing, ask. Do not invent a rule from the snippet alone.

## Workflow

1. Infer **one concern**, a kebab-case filename (`<concern>.mdc`), and `globs` from the snippet path.
   - Backend Python (`core/`, `apps/api/`, `apps/linkedin/`, `cli/`): `core/**/*.py,apps/api/**/*.py,apps/linkedin/**/*.py,cli/**/*.py`
   - Other trees: globs that match that tree (e.g. `apps/web/**/*.{ts,tsx}`)
   - `alwaysApply: false` unless the user says the rule is global
2. List `.cursor/rules/*.mdc`. If an existing rule is **clearly the same concern**, extend that file. Otherwise create a new one-concern `.mdc`. Do not merge unrelated rules.
3. Write or extend the file using the format below. Keep each rule file under ~50 lines.
4. Reply with the path and whether it was **new** or **extended**.

## Rule file format

Match [`.cursor/rules/backend-typing.mdc`](../../rules/backend-typing.mdc):

```markdown
---
description: <one-line what the rule enforces>
globs: <inferred globs>
alwaysApply: false
---

# <Short title>

<Imperative bullets from the user's context.>

Pattern:

\`\`\`<lang>
<the attached snippet>
\`\`\`

\`\`\`<lang>
# BAD
<violation>

# GOOD
<follows the snippet / convention>
\`\`\`
```

## Do not

- Create rules under `rules/` or `~/.cursor/skills/`
- Edit application source to "comply" unless asked
- Add a second concern to an existing `.mdc`
