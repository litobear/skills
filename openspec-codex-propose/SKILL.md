---
name: openspec-codex-propose
description: "Guides the creation of a new OpenSpec change proposal. This skill interacts with the user to gather details, generates content for `proposal.md`, `tasks.md`, and `spec.md` (including modifications to existing requirements), and adheres to project's `openspec/AGENTS.md` guidelines. Use when you need to initiate a new OpenSpec change and require assistance in structuring the proposal documents."
---

# OpenSpec Codex Propose Automation

This skill guides an agent through the interactive process of creating a new OpenSpec change proposal. It will gather necessary information from the user and structure the proposal documents (`proposal.md`, `tasks.md`, and the `spec.md` delta) according to OpenSpec guidelines and project-specific `AGENTS.md` rules.

## Usage

To use this skill, the agent should initiate it with a general request to "propose an OpenSpec change" or "create a new OpenSpec proposal." The skill will then prompt the user for the necessary details.

## Workflow

The automated workflow performs the following interactive and generative steps:

1.  **Obtain Project Context**:
    *   **Action**: Ask the user for the absolute `project_path` (the root of the project containing the `openspec` directory). If not provided, default to the current working directory.
    *   **Guidance**: "Please provide the absolute path to the root of your project where the `openspec` directory is located."

2.  **Gather Proposal Details from User**:
    *   **Action**: Prompt the user for key information needed for the proposal.
    *   **Guidance**: "To create the proposal, I need a few details from you:\n\n    *   **Change Summary**: A brief, concise summary of the change (e.g., 'Add overview link to info command'). This will also be used to generate the `change_id`.\n    *   **Motivation**: Why is this change necessary? (e.g., 'Users need direct access to comprehensive overview.').\n    *   **Affected Components**: List of files/modules/systems impacted (e.g., '``fastify-ts-app/src/routes/lineWebhook.ts``').\n    *   **High-Level Plan**: Outline the main steps to implement the change.\n    *   **Acceptance Criteria**: What defines the successful completion of this change?\n    *   **Specific Requirement to Modify (if applicable)**: If this change modifies an existing requirement, provide the exact heading of that requirement from the project's main `spec.md` (e.g., '### Requirement: Message event control plane'). If it's a new requirement, state 'NEW'."

3.  **Generate Change ID**:
    *   **Action**: Convert the user-provided "Change Summary" into a kebab-case `change_id`.
    *   **Example**: "Add overview link to info command" -> ``add-overview-link-to-info``.

4.  **Navigate to Project Root**:
    *   **Action**: `cd <project_path>`.

5.  **Create New OpenSpec Change Directory**:
    *   **Action**: Execute `openspec new change <change_id>`.

6.  **Read `openspec/AGENTS.md`**:
    *   **Action**: Read the content of `openspec/AGENTS.md` to ensure adherence to project-specific proposal guidelines.
    *   **Guidance**: "I am now reviewing the project's OpenSpec `AGENTS.md` for specific proposal formatting guidelines."

7.  **Generate and Write `proposal.md`**:
    *   **Action**: Construct the content for `openspec/changes/<change_id>/proposal.md` using the gathered user input and standard OpenSpec `proposal.md` structure.
    *   **Guidance**: "Generating `proposal.md` based on your input."

8.  **Generate and Write `tasks.md`**:
    *   **Action**: Construct the content for `openspec/changes/<change_id>/tasks.md`.
    *   **Guidance**: "Generating `tasks.md` for the implementation steps."

9.  **Generate and Write `spec.md` Delta**:
    *   **Action**: This is the most critical and complex step.\n        *   If the user specified an existing "Specific Requirement to Modify":\n            *   Read the *original* `spec.md` (``openspec/specs/<project>/spec.md``).\n            *   Extract the exact content of the specified requirement.\n            *   Modify this content to include the new changes, ensuring ``## MODIFIED Requirements`` heading is used.\n        *   If it's a "NEW" requirement:\n            *   Generate a new requirement block.\n        *   Write the final content to ``openspec/changes/<change_id>/specs/<project>/spec.md``.\n    *   **Guidance**: "Generating the `spec.md` delta. This involves incorporating your changes into the project's specification, referencing existing requirements if applicable."

10. **Validate the Newly Created Proposal**:
    *   **Action**: Execute `openspec validate --changes` (from `project_path`).
    *   **Guidance**: "Validating the newly created proposal for structural integrity."

11. **Inform User of Completion**:
    *   **Action**: Report success or any validation errors.\n    *   **Guidance**: "Your OpenSpec change proposal `[change_id]` has been successfully created and validated. You can now proceed to apply it."

## Important Considerations for the Agent

*   **Error Handling**: Be robust to errors during file creation, `openspec` commands, and user input.
*   **Clarification**: If user input is ambiguous or insufficient, ask clarifying questions.
*   **File Paths**: Always use absolute paths internally for reliability, especially when interacting with `openspec` commands.
*   **Interactive Nature**: This skill requires frequent interaction with the user to gather information. Use clear and concise prompts.
*   **Markdown Generation**: The agent will need to be proficient in generating correctly formatted Markdown for `proposal.md`, `tasks.md`, and `spec.md`.
