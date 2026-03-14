SESS_DIR="$HOME/.openclaw/agents/main/sessions"

# 找 LINE direct 的 session key
LINE_KEY=$(jq -r 'keys[] | select(startswith("agent:main:line:direct:"))' "$SESS_DIR/sessions.json" | head -n1)

# 取 session id（對應 jsonl 檔名）
LINE_ID=$(jq -r --arg k "$LINE_KEY" '.[$k].sessionId // empty' "$SESS_DIR/sessions.json")

# 建備份資料夾
BK_DIR="$SESS_DIR/_bak_$(date +%Y%m%d-%H%M%S)_line_reset"
mkdir -p "$BK_DIR"
cp "$SESS_DIR/sessions.json" "$BK_DIR/sessions.json.before"

# 備份 transcript
[ -n "$LINE_ID" ] && [ -f "$SESS_DIR/$LINE_ID.jsonl" ] && mv "$SESS_DIR/$LINE_ID.jsonl" "$BK_DIR/"

# 從 sessions 索引刪掉 LINE key
jq --arg k "$LINE_KEY" 'del(.[$k])' "$BK_DIR/sessions.json.before" > "$SESS_DIR/sessions.json"

# 驗證
openclaw sessions
echo "Reset done. Backup at: $BK_DIR"