# Huaqiangbei Component Price Inquiry Assistant

An AI-powered tool that helps electronics engineers quickly research price ranges and suppliers for electronic components in the Huaqiangbei market.

## 📖 Problem

Huaqiangbei is the world's largest electronics market, but gathering real-time price and supply information for a specific component is time-consuming and fragmented across various platforms. 

## ✨ What It Does

- Takes a component model (e.g., STM32F103C8T6) and quantity as input.
- Uses two AI agents (Researcher + Planner) to search the web and generate a structured procurement report.
- Outputs price ranges, recommended suppliers, and risk alerts in a Markdown table.
- **Value:** Reduces manual research time from 30 minutes to 30 seconds.

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** Agno (multi-agent framework)
- **Search:** DuckDuckGo Search (Zero-cost)
- **LLM API:** SiliconFlow (Qwen model)
- **UI:** Streamlit

## 🏗️ Architecture Flow

1. **User Input** (Component Model & Quantity)
2. **Researcher Agent** (Searches web for prices and supply)
3. **Planner Agent** (Analyzes data and generates report)
4. **Output** (Structured Markdown Table & Risk Alerts)

## 🚀 How to Run

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your SiliconFlow API key
4. Run: `streamlit run app.py`

## 📸 Example Output

*(Insert a screenshot of your app here)*

## 🧠 What I Learned

- How to build a multi-agent system with Agno for task decomposition.
- How to integrate free LLM APIs and search tools to build a zero-cost prototype.
- How to structure technical documentation (SOP & FAQ) for real-world business use cases.
- Understanding LLM hallucinations and how to design risk alerts for end-users.

---

*(You can move the FAQ to a separate FAQ.md file or keep it below)*
