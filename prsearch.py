import json
import os
import webbrowser
from argparse import ArgumentParser
from urllib.request import Request, urlopen

API_BASE = "https://api.github.com"
MAX_PAGES = 20
QUERY = """
{
  repository(name: "%s", owner: "%s") {
    pullRequests(first: 100,%s states: OPEN) {
      nodes {
        files(first: 10) {
          nodes {
            path
          }
        }
        url
      }
      pageInfo {
        endCursor
      }
    }
  }
}
"""


def send_query(query, token):
    data = json.dumps({"query": query}).encode()
    request = Request(
        f"{API_BASE}/graphql",
        data=data,
        headers={"Authorization": f"token {token}"},
    )
    with urlopen(request) as page:
        return json.load(page)


def valid_data(data):
    if "errors" in data:
        return False
    elif data["data"]["repository"] is None:
        return False
    elif data["data"]["repository"]["pullRequests"] is None:
        return False
    elif len(data["data"]["repository"]["pullRequests"]["nodes"]) == 0:
        return False
    return True


def get_fresh_data(owner, repo, token):
    after = ""
    results = []
    while len(results) == 0 or valid_data(results[-1]):
        if len(results) > 0:
            end = results[-1]["data"]["repository"]["pullRequests"][
                "pageInfo"
            ]["endCursor"]
            after = ' after: "%s",' % end

        results.append(send_query(QUERY % (repo, owner, after), token))
        print(f"Crawling the {len(results)}th page.")

    results.pop()
    return results


def dump_results(results, cache_dir):
    pull_requests = []
    for result in results:
        for pull_request in result["data"]["repository"]["pullRequests"][
            "nodes"
        ]:
            pull_requests.append(
                {
                    "files": [
                        changed_file["path"]
                        for changed_file in pull_request["files"]["nodes"]
                    ],
                    "url": pull_request["url"],
                }
            )
    with open(cache_dir, "w") as cache:
        json.dump(pull_requests, cache)


def get_prs(cache_dir):
    with open(cache_dir) as cache:
        yield from json.load(cache)


def main():
    parser = ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--repo", help="owner/repo")
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--token", default=os.getenv("GH_TOKEN"))
    parser.add_argument("--cachedir", default="results.json")
    parser.add_argument("--max-files", type=int)
    parser.add_argument("--exact", action="store_true")
    options = parser.parse_args()

    if options.fresh:
        owner, repo = options.repo.split("/")
        results = get_fresh_data(owner, repo, options.token)
        dump_results(results, options.cachedir)

    for result in get_prs(options.cachedir):
        files = result["files"]
        matches = []
        for query_file in options.files:
            for result_file in result["files"]:
                if options.exact and query_file == result_file:
                    mathces.append(result_file)
                if not options.exact and query_file in result_file:
                    matches.append(result_file)
        if len(matches) == 0:
            continue
        if (
            options.max_files is not None
            and len(result["files"]) > options.max_files
        ):
            continue

        print("Touched files:", *result["files"])
        print("URL:", result["url"])
        if options.open:
            webbrowser.open(result["url"])


if __name__ == "__main__":
    main()
