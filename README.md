# Huaqiangbei Component Price Inquiry Assistant

An AI-powered tool that helps electronics engineers quickly research price ranges and suppliers for electronic components in the Huaqiangbei market.

## Problem

Huaqiangbei is the world's largest electronics market, but gathering real-time price and supply information for a specific component is time-consuming.

## What It Does

- Takes a component model (e.g., STM32F103C8T6) and quantity as input
- Uses two AI agents (Researcher + Planner) to search the web and generate a structured procurement report
- Outputs price ranges, recommended suppliers, and risk alerts in a Markdown table

## Tech Stack

- Python
- Agno (multi-agent framework)
- DuckDuckGo Search
- SiliconFlow API (Qwen model)
- Streamlit (web UI)

## How to Run

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your SiliconFlow API key
4. Run: `streamlit run travel_agent.py`

## Example Output

(Insert a screenshot of your app here)

## What I Learned

- How to build a multi-agent system with Agno
- How to integrate free LLM APIs and search tools
- How to structure technical documentation for a real use case



# FAQ

## 1. What is this project?

It's an AI assistant that helps users research electronic component prices in the Huaqiangbei market.

## 2. How does it work?

It uses two AI agents: one searches the web for price and supplier information, the other generates a structured report.

## 3. What AI model does it use?

It uses SiliconFlow's API with the Qwen model. It's free and OpenAI-compatible.

## 4. Does it require paid API keys?

No. It uses DuckDuckGo for search (free) and SiliconFlow's free tier for the LLM.

## 5. Can I use it for other markets?

Yes. You can modify the agent prompts to research other markets or product categories.

## 6. What if the AI gives wrong prices?

The tool is for reference only. Always verify with suppliers before making purchasing decisions.
