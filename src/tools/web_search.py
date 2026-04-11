from ddgs import DDGS
from src.config.setting import settings
from src.schemas.tool_outputs import build_tool_response


def search_web(query: str):
    try:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=settings.WEB_SEARCH_MAX_RESULTS)

            for r in search_results:
                results.append(
                    {
                        "title": r.get("title"),
                        "href": r.get("href"),
                        "body": r.get("body"),
                    }
                )

        return build_tool_response(
            tool_name="web_search",
            status="success",
            input_data={"query": query},
            output_data={"results": results},
        )
    except Exception as e:
        return build_tool_response(
            tool_name="web_search",
            status="error",
            input_data={"query": query},
            error=str(e),
        )