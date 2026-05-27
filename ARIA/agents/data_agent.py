import httpx
from bs4 import BeautifulSoup
from agents.base_agent import BaseAgent
from message import AgentMessage
class DataAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="DataAgent")
        self.blocked_domains = [
            'linkedin.com',
            'twitter.com',
            'x.com',
            'facebook.com'
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    async def run(self, message: AgentMessage) -> AgentMessage:
        web_results = message.payload.get("results")
        if not web_results:
            return message.fail("No results in payload - did WebAgent run successfully?")
        self.log(f"Processing {len(web_results)} URLs from WebAgent")
        enriched = []
        async with httpx.AsyncClient(
            headers=self.headers,
            follow_redirects=True,
            timeout=10.0
        ) as client:
            for item in web_results:
                self.log(f"Fetching: {item['url']}")
                content = await self._fetch_content(client, item["url"])
                enriched.append({
                    "title": item["title"],
                    "url": item["url"],
                    "snippet": item["body"],
                    "content": content,
                    "word_count": len(content.split()) if content else 0
                })
        self.log(f"Enriched {len(enriched)} sources")
        return message.succeed({
            "query": message.payload.get("query"),
            "sources": enriched,
        })
    async def _fetch_content(self, client: httpx.AsyncClient, url: str) -> str:
        if any(domain in url for domain in self.blocked_domains):
            self.log(f"Skipping blocked domain: {url}")
            return ""
        try:
            response = await client.get(url)
            if response.status_code != 200:
                self.log(f"Skipping {url} - status code {response.status_code}")
                return ""
            return self._extract_text(response.text)
        except Exception as e:
            self.log(f"Failed to fetch {url}: {e}")
            return ""
    def _extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompse()
        text = soup.get_text(separator=" ", strip=True)
        # collapse whitespace
        words = text.split()
        return " ".join(words[:1000]) # cap at 1000 words per source