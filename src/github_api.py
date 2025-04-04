import datetime
from datetime import datetime, timedelta, timezone
import requests
from requests.exceptions import RequestException
from config import Config
from log_config import logger

class GitHubAPI:
    """Class to handle GitHub API requests."""

    @staticmethod
    def fetch_github_data(username, token):
        if not token:
            logger.error("GitHub token is required.")
            raise ValueError("GitHub token is required.")

        headers = {"Authorization": f"Bearer {token}"}
        user_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?type=all&per_page=100"
        events_url = f"https://api.github.com/users/{username}/events"

        # Handling the user response with error management
        try:
            user_response = requests.get(user_url, headers=headers)
            user_response.raise_for_status()  # Raises an HTTPError for bad responses
        except RequestException as e:
            logger.error(f"Failed to fetch user data: {e}")
            user_response = None

        # Handling the events response with error management
        try:
            events_response = requests.get(events_url, headers=headers)
            events_response.raise_for_status()
        except RequestException as e:
            logger.error(f"Failed to fetch events: {e}")
            events_response = None

        # Handling the repos response with pagination
        repos_data = []
        page = 1
        while True:
            try:
                response = requests.get(f"{repos_url}&page={page}", headers=headers)
                response.raise_for_status()
            except RequestException as e:
                logger.error(f"Failed to fetch repositories on page {page}: {e}")
                break

            repos_page = response.json()
            if not repos_page:
                break
            repos_data.extend(repos_page)
            page += 1

        # Collecting the data and returning it
        data = {
            "user": user_response.json() if user_response else {},
            "repos": repos_data,
            "events": events_response.json() if events_response else []
        }
        return data

    @staticmethod
    def get_total_commits(username, token):
        commits_url = f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc&per_page=1"

        try:
            response = requests.get(commits_url, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
        except RequestException as e:
            logger.error(f"Failed to fetch total commits: {e}")
            return 0

        return response.json().get("total_count", 0)

    @staticmethod
    def get_commits_last_month(username, token):
        today = datetime.now(timezone.utc)
        start_date = today - timedelta(days=Config.ACTIVITY_DAYS)
        commits_url = f"https://api.github.com/search/commits?q=user:{username}+committer-date:{start_date.strftime('%Y-%m-%d')}..{today.strftime('%Y-%m-%d')}&sort=author-date&order=desc"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.cloak-preview"
        }

        daily_commit_counts = [0] * Config.ACTIVITY_DAYS
        page = 1

        while True:
            try:
                response = requests.get(commits_url, headers=headers, params={"page": page, "per_page": 1000})
                response.raise_for_status()
            except RequestException as e:
                logger.error(f"Failed to fetch commits for the last month: {e}")
                break

            for commit in response.json().get("items", []):
                commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%S.%f%z")
                delta = today - commit_date
                if 0 <= delta.days < Config.ACTIVITY_DAYS:
                    daily_commit_counts[delta.days] += 1

            if "next" not in response.links:
                break
            page += 1

        return daily_commit_counts[::-1]
