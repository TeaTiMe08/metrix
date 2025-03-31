
import math
from datetime import datetime

from config import Config
from github_api import GitHubAPI


class TextBuilder:
    """Class to generate text and activity graphics."""
    @staticmethod
    def generate_activity_graphic(commits_last_month):
        if not commits_last_month:
            return ""

        log_commits = [math.log(c + 1) for c in commits_last_month]
        max_log = max(log_commits) if max(log_commits) > 0 else 1

        graphic = ""
        for log_commit in log_commits:
            percentage = (log_commit / max_log) * 100
            if percentage == 0:
                graphic += " "
            elif percentage < 25:
                graphic += "_"
            elif percentage < 50:
                graphic += "▁"
            elif percentage < 75:
                graphic += "▄"
            elif percentage < 100:
                graphic += "█"
            else:
                graphic += "◘"
        return graphic

    @staticmethod
    def generate_text(user_data, repos):
        lines = [
            f"{Config.GITHUB_USERNAME}{Config.TITLE_SUFFIX}",
            "-" * (len(Config.GITHUB_USERNAME) + len(Config.TITLE_SUFFIX)),
            "",
            f"Joined GitHub {datetime.strptime(user_data.get('created_at', '1970-01-01T00:00:00Z'), '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')}",
            f"Followed by {user_data.get('followers', 0)} Users",
            f"Owner of {user_data.get('public_repos', 0) + user_data.get('total_private_repos', 0)} Repos",
            "",
            f"Total Commits: {GitHubAPI.get_total_commits(Config.GITHUB_USERNAME, Config.TOKEN)}",
            f"Total Stars: {sum(repo.get('stargazers_count', 0) for repo in repos)}",
            "",
            f"Data updated: {datetime.now().strftime('%Y-%m-%d')}"
        ]
        return lines
