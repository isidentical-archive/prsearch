import json
import os
from argparse import ArgumentParser
from urllib.request import Request, urlopen

API_BASE = "https://api.github.com"
MAX_PAGES = 20
QUERY = """
{
  repository(name: "cpython", owner: "python") {
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


def get_fresh_data(token):
    after = ""
    results = []
    while len(results) == 0 or valid_data(results[-1]):
        if len(results) > 0:
            end = results[-1]["data"]["repository"]["pullRequests"][
                "pageInfo"
            ]["endCursor"]
            after = ' after: "%s",' % end

        results.append(send_query(QUERY % after, token))
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
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--token", default=os.getenv("GH_TOKEN"))
    parser.add_argument("--cachedir", default="results.json")
    options = parser.parse_args()

    if options.fresh:
        results = get_fresh_data(options.token)
        dump_results(results, options.cachedir)

    query_files = set(options.files)
    for result in get_prs(options.cachedir):
        if match := query_files.intersection(result["files"]):
            print("Matching:", *match)
            print("URL:", result["url"])
            print("=" * 30)


if __name__ == "__main__":
    main()
