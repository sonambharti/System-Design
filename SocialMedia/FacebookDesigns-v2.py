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
        self.postId = itertools.count(100) # value starts from 100 and will iterate every time

    def post(self, userId, post):
        postId = next(self.postId) # will generate an incremented value by one every time
        self.users_posts[userId].append(postId)
        # self.posts[postId] = userId
        self.posts[postId] = {"userId": userId, "content": post}
        print(f'User {userId} posted post with {postId} and content {post}')

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
            # feed.extend(self.users_posts[followee])
            for postId in  self.users_posts[followee]:
                feed.append((postId, self.posts[postId]["content"]))

        # feed = sorted(feed, key=lambda postId: postId, reverse=True)  # Sorting by postId for simplicity
        feed = sorted(feed, key=lambda x: x[0], reverse=True) 
        # print(feed)
        return feed[:self.news_feed_limit]

    def getNewsFeedPaginated(self, userId, pageNumber, pageSize=10):
        feed = self.getNewsFeed(userId)
        start = (pageNumber - 1) * pageSize
        end = start + pageSize
        return feed[start:end]

    def deletePost(self, postId):
        if postId in self.posts:
            userId = self.posts[postId]["userId"]
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
    fb.post('a', 'str1')
    fb.post('a', 'str2')
    fb.post('b', 'str3')
    fb.post('c', 'str4')
    fb.post('c', 'str5')

    # Users following
    fb.follow('a', 'b')
    fb.follow('a', 'c')

    # # Getting news feed
    print("News feed of user a: ", fb.getNewsFeed('a'))

    # # Getting paginated news feed
    print(f'Paginated news feed for user a, page 1: {fb.getNewsFeedPaginated('a', 1)}')
    print(f'Paginated news feed for user a, page 2: {fb.getNewsFeedPaginated('a', 2)}')

    # Deleting a post
    fb.deletePost(101)
    print(f'News feed for user a after deleting post 101: {fb.getNewsFeed('a')}')

    # Unfollowing a user
    fb.unfollow('a', 'c')
    print(f'News feed for user a after unfollowing user c: {fb.getNewsFeed('a')}')
