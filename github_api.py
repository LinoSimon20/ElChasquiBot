import httpx
import os
import logging

from cache import get_cache, set_cache
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN no encontrado en variables de entorno."
    )

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

async def github_user_exists(usuario):

    url = f"https://api.github.com/users/{usuario}"

    try:

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=HEADERS,
                timeout=10
            )

    except httpx.RequestError as error:

        logging.error(
            f"GitHub connection error: {error}"
        )

        return False

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
                headers=HEADERS,
                timeout=10
            )

    except httpx.RequestError as error:
        logging.error(
            f"Error GitHub API: {error}"
        )
        return None

    if response.status_code == 403:

        logging.warning(
            "GitHub API rate limit reached."
        )

        return "rate_limit"
    
    if response.status_code != 200:
        
        logging.error(
            f"GitHub API returned status "
            f"{response.status_code}: "
            f"{response.text}"
        )
        
        return None

    try:

        events = response.json()

    except ValueError as error:

        logging.error(
            f"Invalid GitHub JSON response: {error}"
        )

        return None

    comentarios = []

    for event in events:

        if event.get("type") not in [
            "IssueCommentEvent",
            "PullRequestReviewCommentEvent"
        ]:
            continue

        repo = (
            event.get("repo", {})
            .get("name", "Repositorio desconocido")
        )

        payload = event.get("payload", {})

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

    except httpx.RequestError as error:

        logging.error(
            f"GitHub issues request failed: {error}"
        )
    
        return None
    
    if response.status_code == 403:

        logging.warning(
            "GitHub API rate limit reached."
        )

        return "rate_limit"
    
    if response.status_code != 200:
        
        logging.error(
            f"GitHub API returned status "
            f"{response.status_code}: "
            f"{response.text}"
        )
        
        return None
    
    try:
        
        data = response.json()

    except ValueError as error:

        logging.error(
            f"Invalid GitHub JSON response: {error}"
        )

        return None

    issues = []

    for item in data.get("items", []):

        issues.append({
            "title": item.get("title", "Sin título"),
            "repo": (
                item.get("repository_url", "repos/desconocido")
                .split("repos/")[-1]
            ),
            "url": item.get("html_url", "Sin URL")
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

    except httpx.RequestError as error:

        logging.error(
            f"GitHub PRs request failed: {error}"
        )

        return None
    
    if response.status_code == 403:

        logging.warning(
            "GitHub API rate limit reached."
        )

        return "rate_limit"
    
    if response.status_code != 200:
        
        logging.error(
            f"GitHub API returned status "
            f"{response.status_code}: "
            f"{response.text}"
        )
        
        return None
    
    try:

        data = response.json()

    except ValueError as error:

        logging.error(
            f"Invalid GitHub JSON response: {error}"
        )

        return None

    prs_mergeados = []

    for item in data.get("items", []):

        pull_request = item.get("pull_request", {})

        if (
            item.get("state") == "closed"
            and pull_request.get("merged_at")
        ):
            
            prs_mergeados.append({
                "title": item.get("title", "Sin título"),
                "repo": (
                    item.get("repository_url", "repos/desconocido")
                    .split("repos/")[-1]
                ),
                "url": item.get("html_url", "Sin URL")
            })

    set_cache(cache_key, prs_mergeados)

    return prs_mergeados