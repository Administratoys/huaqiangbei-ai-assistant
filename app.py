from textwrap import dedent
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.duckduckgo import DuckDuckGoTools  # 替换为免费搜索工具
import streamlit as st
import re
from agno.models.openai import OpenAIChat
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


def generate_ics_content(plan_text: str, start_date: datetime = None) -> bytes:
    # ... (这部分保持原样，未做修改) ...
    cal = Calendar()
    cal.add('prodid', '-//AI Travel Planner//github.com//')
    cal.add('version', '2.0')

    if start_date is None:
        start_date = datetime.today()

    day_pattern = re.compile(r'Day (\d+)[:\s]+(.*?)(?=Day \d+|$)', re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days:
        event = Event()
        event.add('summary', "Travel Itinerary")
        event.add('description', plan_text)
        event.add('dtstart', start_date.date())
        event.add('dtend', start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)
    else:
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num - 1)
            event = Event()
            event.add('summary', f"Day {day_num} Itinerary")
            event.add('description', day_content.strip())
            event.add('dtstart', current_date.date())
            event.add('dtend', current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()


# Set up the Streamlit app
st.title("华强北元器件询价助手")
st.caption(
    "Plan your next adventure with AI Travel Planner by researching and planning a personalized itinerary on autopilot using SiliconFlow & DuckDuckGo")

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# 从环境变量读取 API Key，不再需要用户手动输入
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")

if not api_key or not base_url:
    st.error("请先在 .env 文件中配置 OPENAI_API_KEY 和 OPENAI_API_BASE")
    st.stop()

# 初始化 Agents（使用硅基流动的免费模型和 DuckDuckGo）
researcher = Agent(
    name="Researcher",
    role="Searches for travel destinations, activities, and accommodations based on user preferences",
    model=OpenAIChat(
        id="Qwen/Qwen2.5-7B-Instruct",  # 硅基流动上的免费模型
        api_key=api_key,
        base_url=base_url
    ),
    description=dedent(
        """\
    You are a senior electronic components procurement expert in Huaqiangbei (Shenzhen). 
    Given an electronic component model and a purchase quantity, your goal is to search the web for recent price trends, supplier information, and stock status in the Huaqiangbei market.
    """
    ),
    instructions=[
        "Given the component model and quantity, first generate 3 search terms (in Chinese) related to its price and supply in Huaqiangbei, e.g., 'STM32F103C8T6 华强北 报价', 'STM32F103C8T6 现货 价格', 'STM32F103C8T6 替代型号'.",
        "For each search term, use the search tool and analyze the results.",
        "From the results of all searches, return the 10 most relevant results, focusing on price ranges, supplier names (if available), and whether it is original, refurbished, or dismantled (原装/翻新/拆机).",
        "Remember: the accuracy of the price and supply information is crucial for procurement decisions.",
    ],
    tools=[DuckDuckGoTools()],  # 替换为免费的 DuckDuckGo
    add_datetime_to_context=True,
)

planner = Agent(
    name="Planner",
    role="Generates a draft itinerary based on user preferences and research results",
    model=OpenAIChat(
        id="Qwen/Qwen2.5-7B-Instruct",
        api_key=api_key,
        base_url=base_url
    ),
    description=dedent(
        """\
    You are a senior procurement consultant. Given a component model, a purchase quantity, and a list of market research results,
    your goal is to generate a structured procurement report that meets the buyer's needs.
    """
    ),
    instructions=[
        "Given the component model, quantity, and research results, generate a structured procurement report.",
        "The report MUST include the following sections and format:",
        "1. **型号与需求概览**: 简要说明查询的型号和数量。",
        "2. **华强北市场报价表** (必须使用 Markdown 表格)：",
        "   | 报价类型 | 价格区间 (元) | 推荐采购地点/渠道 | 备注 |",
        "   | :--- | :--- | :--- | :--- |",
        "   | 原装正品 | 例如：5.0 - 8.0 | 赛格电子市场 | 质保期长 |",
        "   | 翻新/拆机 | 例如：1.5 - 3.0 | 华强电子世界 | 价格低，需测试 |",
        "3. **替代型号推荐**: 如果有更便宜或更容易买的替代型号，请列出并说明区别。",
        "4. **采购风险提示**: 提醒买家注意翻新件、假货或价格异常波动。",
        "Ensure the report is well-structured, informative, and directly useful for a procurement decision.",
        "Never make up facts. Base the report strictly on the provided research results.",
    ],
    add_datetime_to_context=True,
)

# Input fields for the user's destination and the number of days
component_model = st.text_input("请输入元器件型号（如：STM32F103C8T6）")
quantity = st.number_input("请输入采购数量（用于估算批量价格）", min_value=1, max_value=100000, value=100)

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Itinerary"):
        with st.spinner("Researching your destination..."):
            # First get research results
            research_results: RunOutput = researcher.run(f"Research {component_model} for a quantity of {quantity}", stream=False)
            st.write(" Research completed")

        with st.spinner("Creating your personalized itinerary..."):
            prompt = f"""
            元器件型号: {component_model}
            采购数量: {quantity}
            市场调研结果: {research_results.content}

            请根据以上调研结果，为我生成一份详细的华强北采购报告。
            """
            response: RunOutput = planner.run(prompt, stream=False)
            st.session_state.itinerary = response.content
            st.write(response.content)

with col2:
    if st.session_state.itinerary:
        ics_content = generate_ics_content(st.session_state.itinerary)
        st.download_button(
            label="Download Itinerary as Calendar (.ics)",
            data=ics_content,
            file_name="travel_itinerary.ics",
            mime="text/calendar"
        )