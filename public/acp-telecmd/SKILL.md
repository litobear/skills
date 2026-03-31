---
name: acp-telecmd
description: Orchestrates an ACP Codex agent to manage and execute project-native build and test scripts for spec-driven development, enabling automated code fixes, compilation, and testing based on formal proposals.
---

# ACP Telecommand Skill

This skill outlines the automated workflow for an AI agent (myself) to collaborate with an ACP Codex instance for software development tasks, ensuring a clear and iterative process from proposal to tested implementation.

## Workflow Overview (Agent's Perspective)

Upon receiving a development task (proposal) from the user, I will initiate and manage an ACP Codex session through the following phases:

1.  **Proposal Ingestion:** Read and understand the detailed task proposal provided by the user (typically in an `openspec` file).
2.  **Codex Session Orchestration:** Spawn and maintain a persistent ACP Codex session, feeding it the proposal and relevant context.
3.  **Iterative Development Loop:** Continuously monitor Codex's progress, and when build/test is required, I will instruct Codex to execute the project's own native build/test scripts and relay feedback between Codex and the user.
4.  **Completion & Archiving:** Conclude the task upon successful implementation and testing, notifying the user for final review and potential archiving.

## Execution Steps (Detailed Agent Workflow)

When directed to process an `openspec` task (Proposal), I will execute the following sequence using OpenClaw's tools and openspec skill:

1.  **Receive Proposal Path:** Obtain the path to the `openspec` proposal file from the user.

2.  **Read Proposal:**
    *   Use `read(path=<proposal_file_path>)` to load the proposal content.
    *   Parse and internalize the task requirements.

3.  **Spawn ACP Codex Session:**
    *   Use `sessions_spawn(runtime="acp", agentId=<your_acp_codex_agent_id>, mode="session", task=<initial_task_prompt>, cwd=<project_root_directory>)`
        *   `<your_acp_codex_agent_id>`: Replace with the actual ACP Codex agent ID configured in OpenClaw (e.g., `openai-codex/gpt-5.3-codex`).
        *   `<initial_task_prompt>`: A prompt constructed from the proposal content, guiding Codex on its initial task.
        *   `<project_root_directory>`: The mounted project path (e.g., `/home/ubuntu/.openclaw/workspace/projects/synotelecommand-client`).
    *   Capture the `sessionId` for subsequent interaction.

4.  **Orchestration Loop (Monitor, Build, Test, Relay):**
    *   Continuously poll the ACP Codex session using `sessions_history(sessionKey=<codex_session_id>)` or `process(action="poll")` to monitor its output and status.
    *   **Codex Output Analysis:** Interpret Codex's messages to identify requests for compilation, testing, clarification, or status updates.
    *   **Execute Build:** If Codex indicates a need to build (e.g., “build” or “compile”), instruct Codex to execute the project's native build script:
        *   Instruct Codex to run `./testfiles/build.sh` (via `acpx` prompt, orchestrated by my `build.sh` wrapper).
        *   Relay the output back to the Codex session via `sessions_send(sessionKey=<codex_session_id>, message=<build_output>)`.
    *   **Execute Test:** If Codex indicates a need to test (e.g., “test” or “run tests”), instruct Codex to execute the project's native test script:
        *   Instruct Codex to run `./testfiles/test.sh` (via `acpx` prompt, orchestrated by my `test.sh` wrapper).
        *   Relay the output back to the Codex session via `sessions_send(sessionKey=<codex_session_id>, message=<test_output>)`.
    *   **Relay User Feedback:** If the user provides feedback or new instructions for Codex, relay these messages using `sessions_send(sessionKey=<codex_session_id>, message=<user_message>)`.
    *   **Report to User:** Periodically (or upon significant events) report Codex's progress, questions, or implementation status to the user using `message(action="send", message=<status_update>)`.

5.  **Task Completion:**
    *   When Codex signals task completion and all tests pass, or if directed by the user, mark the task as complete.
    *   Notify the user of successful completion and the changes made by Codex.
    *   Offer to assist with archiving the `openspec` or reviewing the implemented changes.
