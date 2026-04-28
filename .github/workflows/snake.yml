name: Generate Datas

on:
  schedule:
    - cron: "0 */12 * * *" # executes every 12 hours
  workflow_dispatch:
  push:
    branches:
    - main

# THIS IS THE MAGIC FIX FOR THE 403 ERROR
permissions:
  contents: write

jobs:
  build:
    name: Jobs to update datas
    runs-on: ubuntu-latest
    steps:
      # 1. Checkout the repository
      - uses: actions/checkout@v4

      # 2. Generate the Snake Animation (Updated to v3 to fix warnings)
      - uses: Platane/snk@v3
        id: snake-gif
        with:
          github_user_name: SD10LEGACY
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # 3. Push to the output branch (Updated to v4 to fix warnings)
      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # 4. Setup Python for the contribution count script
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          
      # 5. Install Python dependencies
      - name: Install Python dependencies
        run: pip install requests

      # 6. Run the Python script to update README.md
      - name: Update Contribution Count
        env:
          # Uses the Personal Access Token we discussed for the GraphQL API
          GITHUB_TOKEN: ${{ secrets.GH_PAT }} 
        run: python update_count.py

      # 7. Commit the updated README.md to the main branch
      - name: Commit and Push Updated README
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          # Only commit if there are changes
          git diff --quiet && git diff --staged --quiet || (git commit -m "chore: update dynamic contribution count" && git push)
