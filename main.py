import cmd
import requests
import json

from datetime import datetime


class GithubActivity(cmd.Cmd):
    intro = "Welcome to the Github Activity Tracker. Type help or ? to list commands.\n"
    prompt = "GithubActivity> "

    def __init__(self):
        """
        Initializes the GithubActivity command line interface.

        Args:
            None

        Attributes:
            _user (str): Github user to track. Defaults to None.
        """
        super().__init__()
        self._user = None

    def do_get_activity(self, arg):
        """
        Get the activity of a Github user.

        This function will get the activity of a Github user and print it to the console.
        If the user is not set, it will ask for one.

        Args:
            arg (str): argument passed to the function. Not used.

        Returns:
            None
        """
        if self._user is None:
            self._user = input("Please enter a Github user: ")
        response = requests.get(f"https://api.github.com/users/{self._user}/events")
        if response.status_code == 200:
            for event in response.json():
                print(
                    event["type"]
                    + " on "
                    + (datetime.fromisoformat(event["created_at"])).strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                    + ": "
                    + event["repo"]["name"]
                )
                self._user = None
        else:
            self._user = None
            print(f"Error: {response.status_code}")

    def do_list_repos(self, arg):
        """
        List all the repositories of a Github user.

        This function will list all the repositories of a Github user and print them to the console.
        If the user is not set, it will ask for one.

        Args:
            arg (str): argument passed to the function. Not used.

        Returns:
            None
        """
        if self._user is None:
            self._user = input("Please enter a Github user: ")
        response = requests.get(f"https://api.github.com/users/{self._user}/repos")
        if response.status_code == 200:
            for repo in response.json():
                print(repo["name"])
                self._user = None
        else:
            print(f"Error: {response.status_code}")

    def do_clear(self, arg):
        """
        Clear the console.

        This function will clear the console and print nothing.

        Args:
            arg (str): argument passed to the function. Not used.

        Returns:
            None
        """
        print("\033[H\033[J", end="")

    def do_quit(self, arg):
        """
        Quit the application.

        Args:
            arg (str): argument passed to the function. Not used.

        Returns:
            bool: True
        """
        print("Exiting...")
        return True


if __name__ == "__main__":
    GithubActivity().cmdloop()
