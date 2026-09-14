---
name: cross-session-messaging
description: >-
  Send messages to other existing Codex sessions or threads when asked to contact,
  notify, coordinate with, or pass information to another Codex conversation.
  Prefer native thread tools; fall back to codex queue when those tools are
  unavailable, including in SSH remote sessions.
---

# Cross-session messaging

1. Resolve the target using available Codex thread-list or read tools when needed.
   Prefer a thread UUID. The CLI also accepts an exact session name; ask for the
   target if it remains ambiguous.

2. Check available tools, including tool discovery when supported, for a native
   Codex thread-message tool such as `send_message_to_thread`. Use it when available
   for the target, passing its thread ID and host ID as required by that tool.

3. Otherwise, check `codex queue --help` and run the following on the target
   session's host, under the user and `CODEX_HOME` that own that session. For an
   SSH-hosted session, this normally means running it in the remote shell.

   ```sh
   codex queue --thread '<THREAD_UUID_OR_EXACT_NAME>' --message '<MESSAGE>'
   ```

   Pass the message as one literal argument using the current shell's quoting and
   escaping rules, preserving quotes, backticks, dollar signs, and line breaks.
   If this CLI lacks `queue`, report that limitation.

4. Do not use `codex resume` merely to send a message to an active thread; it may
   conflict with the active writer.

5. Report the destination and the delivery result. Successful queueing confirms
   enqueueing, not processing; a cold or unloaded thread may not process the
   message immediately. Use available read/wait thread tools when confirmation or
   a reply is needed. If delivery is uncertain, inspect the target before retrying
   to avoid sending the same message twice.
