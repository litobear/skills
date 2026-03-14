---
name: reset-line-sessions
description: Resets OpenClaw sessions for troubleshooting or cleanup. Use when sessions become unresponsive or need to be cleared.
---

# Reset Line Sessions

## Overview
This skill executes a script to reset active OpenClaw sessions. This can be useful for troubleshooting unresponsive sessions or for general cleanup.

## How to Use

### 1. Reset Sessions
To reset sessions, simply call the `reset_session.sh` script located in the `scripts/` directory.

```bash
/home/ubuntu/.openclaw/workspace/skills/public/reset-line-sessions/scripts/reset_session.sh
```

**Note:** Executing this script may terminate active sessions and could lead to data loss if not used carefully.

## Resources
### `scripts/`
*   `reset_session.sh`: The shell script that performs the session reset operation.
