"""
Design a file sharing app, that can send files between multiple users. Users can follows other users, also show the follower list.
"""


from collections import defaultdict
from typing import List, Set

class File:
    def __init__(self, name: str, content: str, owner: str):
        self.name = name
        self.content = content
        self.owner = owner
        self.shared_with: Set[str] = set()

    def __repr__(self):
        return f"{self.name} (Owner: {self.owner})"

class User:
    def __init__(self, name: str):
        self.name = name
        self.followers: Set[str] = set()
        self.following: Set[str] = set()
        self.uploaded_files: List[File] = []
        self.received_files: List[File] = []

class FileSharingApp:
    def __init__(self):
        self.users: dict[str, User] = {}

    def register(self, username: str):
        if username in self.users:
            print(f"User '{username}' already exists.")
        else:
            self.users[username] = User(username)
            print(f"User '{username}' registered successfully.")

    def follow(self, follower: str, followee: str):
        if follower not in self.users or followee not in self.users:
            print("One or both users do not exist.")
            return
        self.users[follower].following.add(followee)
        self.users[followee].followers.add(follower)
        print(f"{follower} now follows {followee}")

    def upload(self, username: str, filename: str, content: str):
        if username not in self.users:
            print("User does not exist.")
            return
        file = File(filename, content, username)
        self.users[username].uploaded_files.append(file)
        print(f"{username} uploaded file '{filename}'")

    def share(self, sender: str, receivers: List[str], filename: str):
        if sender not in self.users:
            print("Sender does not exist.")
            return
        sender_files = self.users[sender].uploaded_files
        file_to_share = next((f for f in sender_files if f.name == filename), None)
        if not file_to_share:
            print(f"File '{filename}' not found.")
            return
        for receiver in receivers:
            if receiver in self.users:
                self.users[receiver].received_files.append(file_to_share)
                file_to_share.shared_with.add(receiver)
                print(f"Shared '{filename}' with {receiver}")
            else:
                print(f"Receiver '{receiver}' does not exist.")

    def show_files(self, username: str):
        if username not in self.users:
            print("User does not exist.")
            return
        user = self.users[username]
        all_files = user.uploaded_files + user.received_files
        print(f"Files for {username}:")
        for f in all_files:
            print(f" - {f}")

    def show_followers(self, username: str):
        if username not in self.users:
            print("User does not exist.")
            return
        print(f"Followers of {username}: {sorted(self.users[username].followers)}")

    def show_following(self, username: str):
        if username not in self.users:
            print("User does not exist.")
            return
        print(f"{username} is following: {sorted(self.users[username].following)}")


# --------------------------
# Sample Usage / Commands
# --------------------------
if __name__ == "__main__":
    app = FileSharingApp()

    app.register("Alice")
    app.register("Bob")
    app.register("Charlie")

    app.follow("Alice", "Bob")
    app.follow("Charlie", "Alice")

    app.upload("Alice", "report.pdf", "Quarterly financial report.")
    app.upload("Bob", "notes.txt", "Docker & Kubernetes notes")

    app.share("Alice", ["Bob", "Charlie"], "report.pdf")
    app.share("Bob", ["Alice"], "notes.txt")

    app.show_files("Alice")
    app.show_files("Bob")
    app.show_files("Charlie")

    app.show_followers("Alice")
    app.show_following("Alice")
