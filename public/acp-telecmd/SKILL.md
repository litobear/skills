---
name: acp-telecmd
description: Orchestrates an ACP Codex agent for spec-driven development, handling code fixes, compilation, and testing based on proposals in an 'openspec' folder.
---

# ACP Spec Workflow

您現在是個資深軟體工程師，我有一個專案要委託你：
這是一個非常清晰且自動化的工作流程，透過將遠端專案掛載到本地並利用 ACP Codex 進行程式碼修正、編譯和測試，直到任務完成。

為了確保 ACP Codex 能夠順利執行您的工作，我已確認以下幾點：

1. SSHFS 掛載： 已透過 SSHFS 成功掛載到本地 projects 目錄下，路徑：/home/ubuntu/.openclaw/workspace/projects/synotelecommand-client。

2. 編譯指令：
ssh b.syno "~/build-master-synotelecommand-client.sh"

3. 測試指令：
ssh b.syno "~/test-master-synotelecommand-client.sh"


當 ACP Codex 的任務來自該專案的 openspec 資料夾。

為了能夠在這個流程中更好地與您協作，我將這樣與您互動：

任務定義 (Proposal)：
您可以在 openspec 資料夾中創建一個新的提案文件（例如 Markdown 或純文字檔案），裡面詳細描述您希望 ACP Codex 完成的工作。
您需要告訴我這個提案文件的路徑和名稱。
我會將這個提案作為 ACP Codex 的任務輸入。

審核討論 (review)：
在 ACP Codex 接收任務並開始工作後，如果它有任何疑問、需要澄清或在實作過程中遇到問題，它會向您發送訊息（透過我）。
我會將 ACP Codex 的問題或進度回報傳達給您。
您對 ACP Codex 的回饋或指示，可以透過文字訊息傳達給我，我會轉達給 ACP Codex。

Codex 實作 (Codex Apply implementation)：
ACP Codex 將會根據提案和您的回饋，在專案資料夾中進行程式碼修正、編譯和測試，直到達到預期的結果。
我會持續監控 ACP Codex 的執行狀態和進度，並向您定期回報。
固化規格歸檔 (Archive)：
當 ACP Codex 完成任務並通過所有測試後，我會通知您。
您可以在這個階段審核 ACP Codex 所做的更改。如果確認無誤，您可以將相關的 openspec 文件或程式碼歸檔。

### 啟動與管理 ACP Codex (Agent Workflow)

當您向我提供 `openspec` 中的任務（Proposal）後，我將執行以下步驟：

1.  **讀取提案：** 我會讀取您提供的提案文件，理解任務內容。
2.  **啟動 ACP Codex：** 我將使用 `sessions_spawn` 工具啟動一個 ACP Codex 會話。我將設定 `runtime="acp"`，`agentId="openai-codex/gpt-5.3-codex"`，並將專案的根目錄 `/home/ubuntu/.openclaw/workspace/projects/synotelecommand-client` 設定為 ACP Codex 的工作目錄。ACP Codex 的初始任務將來自提案內容。
3.  **持續監控與互動：**
    *   我會持續監控 ACP Codex 的輸出，檢查其進度、問題或需要您輸入的訊息。
    *   **執行編譯：** 如果 ACP Codex 需要編譯程式碼，我將執行 `skills/public/acp-spec-workflow/scripts/build.sh` 腳本。
    *   **執行測試：** 如果 ACP Codex 需要運行測試，我將執行 `skills/public/acp-spec-workflow/scripts/test.sh` 腳本。
    *   我會將編譯和測試的結果傳達給 ACP Codex。
    *   我會將 ACP Codex 的問題或狀態回報給您，並將您的指示傳達給它。
4.  **任務完成：** 當 ACP Codex 完成任務並通過所有檢查時，我將通知您。
