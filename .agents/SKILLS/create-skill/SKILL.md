---
name: create-skill
description: Creates a new agent skill following the standard conventions. Use when the user asks to create a new skill or extend capabilities with a new skill.
---

# Create Skill

When creating a new skill, follow these instructions to ensure it is structured correctly and conforms to the skills standard.

## Location
Determine where to place the skill based on the user's request:
- **Workspace-specific**: `<workspace-root>/.agents/skills/<skill-folder>/` (Default)
- **Global**: `~/.gemini/config/skills/<skill-folder>/`

Note: If using a workspace, use `.agents/skills` rather than `.agent/skills`.

## Skill Folder Structure
Create the following structure for the new skill. Make sure to use lowercase and hyphens for spaces in the skill folder name.

```text
<skill-location>/<skill-folder>/
├── SKILL.md       # Main instructions (required)
├── scripts/       # Helper scripts (optional)
├── examples/      # Reference implementations (optional)
└── resources/     # Templates and other assets (optional)
```

## SKILL.md Format
The `SKILL.md` file MUST contain YAML frontmatter at the top with `name` and `description`.
Write the description in the third person and include keywords to help the agent recognize when to use it.

### Template

```markdown
---
name: <skill-name>
description: <clear description of what the skill does and when to use it, written in third person>
---

# <Skill Title>

Detailed instructions for the agent go here.

## When to use this skill

- Use this when...
- This is helpful for...

## How to use it

Step-by-step guidance, conventions, and patterns the agent should follow.
```

## Best Practices to impart to the new skill:
1. **Keep it focused**: Each skill should do one thing well. Instead of a "do everything" skill, create separate skills for distinct tasks.
2. **Write clear descriptions**: The description is how the agent decides whether to use the skill. Make it specific about what the skill does and when it's useful.
3. **Use scripts as black boxes**: If your skill includes scripts, encourage the agent to run them with `--help` first rather than reading the entire source code.
4. **Include decision trees**: For complex skills, add a section that helps the agent choose the right approach based on the situation.
