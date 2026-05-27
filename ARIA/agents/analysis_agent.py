import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents.base_agent import BaseAgent
from message import AgentMessage
load_dotenv()
class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AnalysisAgent")
        cerebras_key = os.getenv("CEREBRAS_API_KEY")
        if not cerebras_key:
            raise ValueError("CEREBRAS_API_KEY not set")
        self.client = AsyncOpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=cerebras_key,
        )
    async def run(self, message: AgentMessage) -> AgentMessage:
        sources = message.payload.get("sources")
        query = message.payload.get("query")
        if not sources:
            return message.fail("No sources in payload - did DataAgent run successfully?")
        self.log(f"Analyzing {len(sources)} sources for: '{query}'")
        insights = []
        for i, source in enumerate(sources, 1):
            if not source.get("content"):
                self.log(f"Skipping source {i} - no content extracted")
                continue
            self.log(f"Analyzing source {i}: {source['title']}")
            insight = await self._analyze_source(source, query)
            insights.append(insight)
        self.log("Synthesizing insights...")
        synthesis = await self._synthesize(query, insights)
        return message.succeed({
            "query": query,
            "insights": insights,
            "synthesis": synthesis,
        })
    async def _analyze_source(self, source: dict, query: str) -> dict:
        prompt = f"""
You are a research analyst. A user is researching: {query}
Here is content from one source:
Title: {source.get('title')}
URL: {source.get('url')}
Content: {source.get('content','')[:800]}
Extract 3 key facts or insights from this source relevant to the query.
Respond in this exact format:
FACT 1: <fact>
FACT 2: <fact>
FACT 3: <fact>
RELEVANCE: <high/medium/low>
"""
        try:
            response = await self.client.chat.completions.create(
                model="llama3.1-8b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            raw = response.choices[0].message.content.strip()
            return {"title": source.get("title"), "url": source.get("url"), "raw_analysis": raw}
        except Exception as e:
            self.log(f"Analysis failed for {source['title']}: {e}")
            return {
                "title": source["title"],
                "url": source["url"],
                "raw_analysis": f"Analysis failed: {e}",   
            }
    async def _synthesize(self, query: str, insights: list) -> str:
        combined = "\n\n".join([
            f"Source: {i['title']}\n{i['raw_analysis']}"
            for i in insights
        ])
        prompt = f"""
You are a senior research analyst.
A user researched: "{query}"
Here are analyses from multiple sources:
{combined}
Write a concise synthesis - 3 to 5 sentences - summarizing the most important
findings across all sources. Be direct and factual. No fluff.
"""
        try:
            response = await self.client.chat.completions.create(
                model="llama3.1-8b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
            )
            raw = response.choices[0].message.content.strip()
            return raw
        except Exception as e:
            return f"synthesis failed: {e}"
