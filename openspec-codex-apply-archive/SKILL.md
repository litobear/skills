---
name: openspec-codex-apply-archive
description: "Automates the end-to-end workflow for applying OpenSpec change proposals using an ACP Codex agent. This skill handles the process from validation to archiving, ensuring the Codex agent adheres to project-specific OpenSpec guidelines (via AGENTS.md). It assumes an OpenSpec proposal has already been created according to project guidelines. Use when you have a validated OpenSpec change proposal (created via `openspec new change`) and need to apply/archive it into the main project specification. The change should be in 'draft' or 'validated' state."
---

# OpenSpec Codex Apply/Archive Automation

This skill guides an agent through the process of taking an OpenSpec change proposal and applying/archiving it into the project's main specification using a Codex sub-agent.

## Usage

To use this skill, provide the following parameters:

-   `change_id`: The ID of the OpenSpec change proposal (e.g., `add-overview-link-to-info`).
-   `project_path`: (Optional) The absolute path to the root of the project containing the `openspec` directory. If not provided, the current working directory will be assumed.

## Workflow

The automated workflow performs the following steps:

1.  **Navigate to Project Root**: The agent will `cd` into the specified `project_path`. This is crucial as `openspec` commands are sensitive to the current working directory.
2.  **Validate Change**: The agent will attempt to validate the OpenSpec change using `openspec validate --changes`. This ensures the proposal is structurally sound before application.
3.  **Spawn Codex Agent for Archiving**: A new ACP (Agent Communication Protocol) session will be spawned with a Codex agent (`agentId="codex"`, `runtime="acp"`). The Codex agent will operate from the `project_path`, and its task will explicitly include referencing `openspec/AGENTS.md`.
4.  **Codex Task Execution**: The Codex agent will be given a specific task to perform the archiving:
    *   **Read `openspec/AGENTS.md`**: This ensures the Codex agent is aware of and adheres to any project-specific guidelines for OpenSpec workflows.
    *   **Execute `openspec archive <change_id> --yes`**: This command is the current equivalent of "applying" or merging the change proposal into the main `openspec/specs` directory. The `--yes` flag bypasses confirmation prompts.
    *   **Error Handling**: If the `archive` command fails or is not found, the Codex agent is instructed to report the issue.

## Example

```
# Assuming current directory is the project root for LinePusher
# To apply the 'add-overview-link-to-info' change
sessions_spawn(
    agentId="openspec-codex-apply-archive",
    task="Apply OpenSpec change 'add-overview-link-to-info' in project '/home/ubuntu/.openclaw/projects/LinePusher'."
)
```

**Note**: The actual `sessions_spawn` call to trigger this skill would be handled by the main agent. The skill's internal logic will then manage the nested `sessions_spawn` to Codex.
