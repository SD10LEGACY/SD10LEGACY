import os
import requests

# Fetch GitHub Token from environment
TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "SD10LEGACY"

headers = {"Authorization": f"Bearer {TOKEN}"}
query = """
{
  user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
""" % USERNAME

# Call GitHub GraphQL API
response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

data = response.json()

try:
    count = data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']

    # Read the README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # These markers wrap the count in the README heading
    start_marker = "<!-- CONTRIBUTION_COUNT_START -->"
    end_marker = "<!-- CONTRIBUTION_COUNT_END -->"

    if start_marker in readme and end_marker in readme:
        before = readme.split(start_marker)[0]
        after = readme.split(end_marker)[1]

        new_readme = f"{before}{start_marker}{count}{end_marker}{after}"

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_readme)

        print(f"Successfully updated contribution count to: {count}")
    else:
        print("Could not find the HTML markers in the README. No changes made.")

except Exception as e:
    print(f"Error occurred: {e}")
    print(f"API response: {data}")
