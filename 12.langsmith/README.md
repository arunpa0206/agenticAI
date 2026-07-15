# LangSmith Setup Guide

Follow these simple steps to set up execution tracing for the flight booking agent.

---

## Step 1: Get a LangSmith API Key
1. Go to the LangSmith dashboard: [https://smith.langchain.com](https://smith.langchain.com)
2. Log in or create a free account.
3. Click on the **Settings** (gear icon) in the bottom-left corner.
4. Click on **API Keys** and then click **Create API Key**.
5. Copy the generated key (it usually starts with `lsv2_pt_...`).

---

## Step 2: Configure Environment Variables
Open the `.env` file in the root directory of the project and append the following configuration:

```env
# Enable LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_copied_api_key_here
LANGCHAIN_PROJECT=flight-booking-agent
```

*Replace `your_copied_api_key_here` with the API key you copied in Step 1.*

---

## Step 3: Run the Agent
Run the main script from your terminal:
```bash
python main.py
```
Interact with the chatbot (e.g. search or book a flight). The execution data will automatically upload in the background.

---

## Step 4: View Your Traces
1. Go back to the LangSmith dashboard: [https://smith.langchain.com](https://smith.langchain.com)
2. Click on **Projects** in the left sidebar menu.
3. Select the **`flight-booking-agent`** project.
4. Click on any run to inspect the node flowchart, inputs, outputs, prompts, tool calls, and execution latencies.
