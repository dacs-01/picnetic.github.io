from src.models import Comments, Users, Post
from src.repositories.users_repository import users_repository_singleton

def test_user_model():
    newUser = Users(user_id = 5, user_name = "Test", passed = "123", email = "test@gmail.com")

    assert newUser.user_id == 5
    assert newUser.user_name =="Test"
    assert newUser.passed == "123"
    assert newUser.email == "test@gmail.com"

def test_post_model():
    newUser = Users(user_id = 5, user_name = "Test", passed = "123", email = "test@gmail.com")
    newPost = Post(post_id = 3, user_name = newUser.user_name, post_label = "sports", post_cap = "Football Team", post_picture = "TESTURL")

    assert newPost.post_id == 3
    assert newPost.user_name == "Test"
    assert newPost.post_label == "sports"
    assert newPost.post_cap == "Football Team"
    assert newPost.post_picture == "TESTURL"

def test_comment_model():
    newUser = Users(user_id = 5, user_name = "Test", passed = "123", email = "test@gmail.com")
    newPost = Post(post_id = 3, user_name = newUser.user_name, post_label = "sports", post_cap = "Football Team", post_picture = "TESTURL")
    comments = Comments(comment_id = 1, user_id = newUser.user_id, comment = "Nice Picture!", post_id = newPost.post_id)

    assert comments.comment_id == 1
    assert comments.user_id == 5
    assert comments.comment == "Nice Picture!"
    assert comments.post_id == 3

# def test_search_user():
#     newUser = Users(user_id = 5, user_name = "Test", passed = "123", email = "test@gmail.com")

#     searchUser = users_repository_singleton.search_users(newUser.user_name)

#     print(searchUser)
