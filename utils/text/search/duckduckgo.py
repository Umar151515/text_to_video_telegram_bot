from duckduckgo_search import DDGS


@staticmethod
async def search_tool(query: str, add_text: bool = True) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query)
        if not results:
            return ""
        context = "\n".join([r['body'] for r in results if 'body' in r][:5])
        return context if add_text else ""