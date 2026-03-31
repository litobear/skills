# clawhub-installer

## Description
Install OpenClaw skills from ClawdHub using `npx clawhub install`. This skill simplifies the process of adding new capabilities to your OpenClaw environment by automating the `clawhub install` command.

## Usage
To install a skill, simply tell me: "安裝 skill <skill_name>" or "Install skill <skill_name>".

**Example:**
`安裝 skill agent-browser`

## Implementation
This skill executes the following command, retrying until successful:
`until npx clawhub@latest install {skill_name} --force; do sleep 1; done`

It will then report the installation status.
