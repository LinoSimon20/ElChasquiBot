import httpx
import os
import logging

from cache import get_cache, set_cache
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


async def github_user_exists(usuario):

    url = f"https://api.github.com/users/{usuario}"

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            headers=HEADERS
        )

    return response.status_code == 200


async def get_user_comentarios(usuario):

    url = (
        f"https://api.github.com/users/"
        f"{usuario}/events/public"
    )

    cache_key = f"comments:{usuario}"

    cached = get_cache(cache_key)

    if cached is not None:
        return cached
    
    try:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=HEADERS
            )

    except httpx.RequestError as error:
        logging.error(
            f"Error GitHub API: {error}"
        )
        return None

    if response.status_code != 200:
        return []

    events = response.json()

    comentarios = []

    for event in events:

        if event["type"] not in [
            "IssueCommentEvent",
            "PullRequestReviewCommentEvent"
        ]:
            continue

        repo = event["repo"]["name"]

        payload = event["payload"]

        comment_body = (
            payload.get("comment", {})
            .get("body", "Sin comentario")
        )

        issue = payload.get("issue", {})

        title = issue.get(
            "title",
            "Sin título"
        )

        url = issue.get(
            "html_url",
            "Sin URL"
        )

        comentarios.append({
            "repo": repo,
            "title": title,
            "comment": comment_body,
            "url": url
        })

    set_cache(cache_key, comentarios)
    
    return comentarios


async def get_issues_asignados(usuario):
    
    cache_key = f"issues:{usuario}"

    cached = get_cache(cache_key)

    if cached is not None:
        return cached

    url = (
        "https://api.github.com/search/issues"
        f"?q=assignee:{usuario}+is:open"
    )

    try:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=HEADERS,
                timeout=10
            )

    except httpx.RequestError:
    
        return None
    
    if response.status_code != 200:
        
        return None
    
    data = response.json()

    issues = []

    for item in data["items"]:

        issues.append({
            "title": item["title"],
            "repo": item["repository_url"]
                .split("repos/")[-1],
            "url": item["html_url"]
        })

    set_cache(cache_key, issues)

    return issues

async def get_user_prs_mergeados(usuario):

    cache_key = f"prs:{usuario}"

    cached = get_cache(cache_key)

    if cached is not None:
        return cached
    
    url = (
        "https://api.github.com/search/issues"
        f"?q=type:pr+author:{usuario}"
    )

    try:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=HEADERS,
                timeout=10
            )

    except httpx.RequestError:

        return None
    
    if response.status_code != 200:

        return None
    
    data = response.json()

    prs_mergeados = []

    for item in data["items"]:

        pull_request = item.get("pull_request", {})

        if (
            item["state"] == "closed"
            and pull_request.get("merged_at")
        ):
            
            prs_mergeados.append({
                "title": item["title"],
                "repo": item["repository_url"]
                    .split("repos/")[-1],
                "url": item["html_url"]
            })

    set_cache(cache_key, prs_mergeados)

    return prs_mergeados