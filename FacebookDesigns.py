"""
Design Facebook (LLD) :

Implement the below APIs
public void post(int userId, int postId);
public void follow(int followerId, int followeeId);
public void unfollow(int followerId, int followeeId);
public List<Integer> getNewsFeed(int userId);
public List<Integer> getNewsFeedPaginated(Integer userId, Integer pageNumber);
public void deletePost(int postId);

"""


from collections import defaultdict, deque
import itertools

class Facebook:
    def __init__(self):
        self.users_posts = defaultdict(list)  # Maps userId to list of postIds
        self.user_followees = defaultdict(set)  # Maps userId to set of followeeIds
        self.posts = {}  # Maps postId to userId
        self.news_feed_limit = 10  # Maximum number of posts in the news feed

    def post(self, userId, postId):
        self.users_posts[userId].append(postId)
        self.posts[postId] = userId
        print(f'User {userId} posted post {postId}')

    def follow(self, followerId, followeeId):
        self.user_followees[followerId].add(followeeId)
        print(f'User {followerId} followed user {followeeId}')

    def unfollow(self, followerId, followeeId):
        self.user_followees[followerId].discard(followeeId)
        print(f'User {followerId} unfollowed user {followeeId}')

    def getNewsFeed(self, userId):
        feed = []
        followees = self.user_followees[userId] | {userId}  # Include the user's own posts

        for followee in followees:
            feed.extend(self.users_posts[followee])

        feed = sorted(feed, key=lambda postId: postId, reverse=True)  # Sorting by postId for simplicity
        return feed[:self.news_feed_limit]

    def getNewsFeedPaginated(self, userId, pageNumber, pageSize=10):
        feed = self.getNewsFeed(userId)
        start = (pageNumber - 1) * pageSize
        end = start + pageSize
        return feed[start:end]

    def deletePost(self, postId):
        if postId in self.posts:
            userId = self.posts[postId]
            if postId in self.users_posts[userId]:
                self.users_posts[userId].remove(postId)
            del self.posts[postId]
            print(f'Post {postId} deleted')
        else:
            print(f'Post {postId} not found')


# Driver code for demonstration
if __name__ == "__main__":
    fb = Facebook()

    # Users posting
    fb.post(1, 101)
    fb.post(1, 102)
    fb.post(2, 201)
    fb.post(3, 301)
    fb.post(3, 302)

    # Users following
    fb.follow(1, 2)
    fb.follow(1, 3)

    # Getting news feed
    print(f'News feed for user 1: {fb.getNewsFeed(1)}')
    print(f'News feed for user 2: {fb.getNewsFeed(2)}')

    # Getting paginated news feed
    print(f'Paginated news feed for user 1, page 1: {fb.getNewsFeedPaginated(1, 1)}')
    print(f'Paginated news feed for user 1, page 2: {fb.getNewsFeedPaginated(1, 2)}')

    # Deleting a post
    fb.deletePost(101)
    print(f'News feed for user 1 after deleting post 101: {fb.getNewsFeed(1)}')

    # Unfollowing a user
    fb.unfollow(1, 3)
    print(f'News feed for user 1 after unfollowing user 3: {fb.getNewsFeed(1)}')
