from .models import User, Posts, Profile



#logged in user unfollowed profile user
def unfollowed(logged_in_user, profile_user):

    #get logged in user and profile user profiles
    profile_user_obj = User.objects.get(username=profile_user)
    profile_user_profile = Profile.objects.get(user=profile_user_obj)

    logged_in_user_obj = User.objects.get(username=logged_in_user)
    logged_in_user_profile = Profile.objects.get(user=logged_in_user_obj)

    #logged in user unfollowed profile user, therefore remove 1 following from logged in user and remove follower from profile user

    #remove follower from profile user
    profile_user_profile.followers.remove(logged_in_user_obj)
    profile_user_profile.save()

    #remove 1 following from logged in user
    logged_in_user_profile.following.remove(profile_user_obj)
    logged_in_user_profile.save()


#
def followed(logged_in_user, profile_user):
    #get logged in user and profile user profiles
    profile_user_obj = User.objects.get(username=profile_user)
    profile_user_profile = Profile.objects.get(user=profile_user_obj)

    logged_in_user_obj = User.objects.get(username=logged_in_user)
    logged_in_user_profile = Profile.objects.get(user=logged_in_user_obj)

    #logged in user followed profile user, therefore add 1 following to logged in user and add follower to profile user

    #add follower to profile user
    profile_user_profile.followers.add(logged_in_user_obj)
    profile_user_profile.save()

    #add 1 following to logged in user
    logged_in_user_profile.following.add(profile_user_obj)
    logged_in_user_profile.save()