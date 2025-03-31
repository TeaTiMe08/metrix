import datetime
import logging
from datetime import datetime, timedelta, timezone

import requests

from config import Config

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class GitHubAPI:
    """Class to handle GitHub API requests."""
    @staticmethod
    def fetch_github_data(username, token):
        if not token:
            logging.error("GitHub token is required.")
            raise ValueError("GitHub token is required.")

        headers = {"Authorization": f"Bearer {token}"}
        user_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?type=all&per_page=100"
        events_url = f"https://api.github.com/users/{username}/events"

        user_response = requests.get(user_url, headers=headers)
        if user_response.status_code != 200:
            logging.error(f"Failed to fetch user data: {user_response.status_code} - {user_response.text}")

        events_response = requests.get(events_url, headers=headers)
        if events_response.status_code != 200:
            logging.error(f"Failed to fetch events: {events_response.status_code} - {events_response.text}")

        repos_data = []
        page = 1
        while True:
            response = requests.get(f"{repos_url}&page={page}", headers=headers)
            if response.status_code == 200:
                repos_page = response.json()
                if not repos_page:
                    break
                repos_data.extend(repos_page)
                page += 1
            else:
                logging.error(f"Failed to fetch repositories on page {page}: {response.status_code} - {response.text}")
                break

        data = {
            "user": user_response.json() if user_response.status_code == 200 else {},
            "repos": repos_data,
            "events": events_response.json() if events_response.status_code == 200 else []
        }
        return data

    @staticmethod
    def get_total_commits(username, token):
        commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc&per_page=1"
        response = requests.get(commits_url, headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            logging.error(f"Failed to fetch total commits: {response.status_code} - {response.text}")
            return 0
        return response.json().get("total_count", 0)

    @staticmethod
    def get_commits_last_month(username, token):
        today = datetime.now(timezone.utc)
        start_date = today - timedelta(days=Config.ACTIVITY_DAYS)
        commits_url = f"https://api.github.com/search/commits?q=author:{username}+committer-date:>={start_date.strftime('%Y-%m-%d')}&sort=author-date&order=desc"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.cloak-preview"
        }

        daily_commit_counts = [0] * Config.ACTIVITY_DAYS
        page = 1

        while True:
            response = requests.get(commits_url, headers=headers, params={"page": page, "per_page": 100})
            if response.status_code != 200:
                logging.error(f"Failed to fetch commits for the last month: {response.status_code} - {response.text}")
                break

            for commit in response.json().get("items", []):
                commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%S.%f%z")
                delta = today - commit_date
                if delta.days < Config.ACTIVITY_DAYS:
                    daily_commit_counts[delta.days] += 1

            if "next" not in response.links:
                break
            page += 1

        return daily_commit_counts[::-1]
