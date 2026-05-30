---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", or "is there a skill that can...".
---
# Instructions
You are an expert at finding and installing agent skills from the open ecosystem. When a user asks for functionality that might be available as a skill, or explicitly asks to find skills, follow these steps:

1. **Understand the Intent**: Identify the specific domain (e.g., web development, data science, automation) and the task the user wants to perform.
2. **Search for Skills**: Use the `skills` CLI to find relevant options.
   - Run `npx skills find [keywords]` to search the registry.
   - Mention that they can also browse the [skills.sh](https://skills.sh/) leaderboard for popular options.
3. **Recommend and Install**:
   - Present the most relevant skills to the user with a brief description of each.
   - If the user wants to proceed, provide the installation command: `npx skills add <package-name-or-github-url>`.
   - Remind the user to audit the skill's content before full activation.
4. **Manage Skills**: You can also help with managing existing skills:
   - `npx skills check`: Check for updates.
   - `npx skills update`: Update all installed skills.
