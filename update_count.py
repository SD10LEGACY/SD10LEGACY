import os
import requests
import re

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
    
    # Read your README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Safely replace the number between the markers using strict group definitions
    new_readme = re.sub(
        r'().*?()', 
        rf'\g<1>{count}\g<2>', 
        readme,
        flags=re.DOTALL
    )

    # Write the updated README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)
        
    print(f"Successfully updated contribution count to: {count}")
    
except KeyError:
    print("Error parsing GitHub API response. Token might be invalid or expired.")
    print(data) # This will print the actual error from GitHub if it fails
