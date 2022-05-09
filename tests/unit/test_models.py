from src.models import Users, Post

def test_user_model():
    newUser = Users(user_name = "Test", passed = "123", email = "test@gmail.com")

    assert newUser.user_name =="Test"
    assert newUser.passed == "123"
    assert newUser.email == "test@gmail.com"

def test_post_model():
    newUser = Users(user_name = "Test", passed = "123", email = "test@gmail.com")
    newPost = Post(user_name = newUser.user_name, post_label = "sports", post_cap = "Football Team", post_picture = "TESTURL")

    assert newPost.user_name == "Test"
    assert newPost.post_label == "sports"
    assert newPost.post_cap == "Football Team"
    assert newPost.post_picture == "TESTURL"

