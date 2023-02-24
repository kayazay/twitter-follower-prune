import tweepy
import authfile as af
import pandas as pd

# authenticate using the credentials in authfile.py
auth = tweepy.OAuthHandler(
    af.api_key,  # consumer key goes here
    af.api_secret  # consumer secret goes here
)
auth.set_access_token(
    af.access_token,  # access token goes here
    af.access_secret  # access token secret goes here
)

# create an instance of tweepy API
api = tweepy.API(
    auth,
    wait_on_rate_limit=True  # wait for rate limits to reset automatically
)

# get user input for minimum number of followers for an influencer
min_followers = int(input('What is the minimum number of followers a person should have to be viewed as an influencer to you?'))


# function to get a dataframe of followers with less than the minimum number of followers
def get_followers_df():
    # initialize empty lists to store follower details
    screen_name_list, user_id_list, bio_list, followers_count_list = [], [], [], []
    page_num = 0
    # loop over all pages of friends/followers (in increments of 200 at a time)
    for page in tweepy.Cursor(api.get_friends, count=200).pages():
        print(f'{page_num} to {page_num+200} friends gotten')
        for follower in page:
            # extract follower details
            screen_name_list.append(follower.screen_name)
            user_id_list.append(follower.id_str)
            bio_list.append(follower.description)
            followers_count_list.append(follower.followers_count)
        page_num += 200
    print('Exhausted friends')
    # create a dictionary of follower details
    userinfo = {}
    userinfo['screen_name'] = screen_name_list
    userinfo['user_id'] = user_id_list
    userinfo['bio'] = bio_list
    userinfo['followers_count'] = followers_count_list
    # convert the dictionary to a pandas dataframe and return only those with less than the minimum number of followers
    user_df_in = pd.DataFrame(userinfo)
    return user_df_in[user_df_in['followers_count']<min_followers]

# call the function to get the dataframe of followers
followers_df = get_followers_df()

# get a list of user IDs of the followers who we are following
followers_ids_list = followers_df['user_id'].tolist()

# initialize an empty list to store whether each follower is followed by us or not
is_followed_list = []
i = 0

# loop over all the IDs in increments of 100 at a time
while i < len(followers_ids_list):
    # get the next 100 IDs
    ids_in_100s = followers_ids_list[i:i+100]
    # look up the friendships (i.e., whether each follower is being followed by us or not)
    friendships_in_100s = api.lookup_friendships(user_id=ids_in_100s)
    for friendship in friendships_in_100s:
        # add the result to the list
        is_followed_list.append(friendship.is_followed_by)
    i += 100

# add the list of whether each follower is followed by us or not to the dataframe
followers_df['is_followed_by'] = is_followed_list

# select only those followers who are not being followed by us
not_following_df = followers_df[followers_df['is_followed_by']==False]

# loop over the user IDs of the followers who are not being followed by us and unfollow them
for not_following_id in not_following_df['user_id']:
    api.destroy_friendship(user_id=not_following_id)
