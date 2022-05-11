# from src.models import Users, Post

# def test_homepage(test_app):
#     res = test_app.get('/index')

#     newUser = Users(user_name = "Test", passed = "123", email = "test@gmail.com")
#     newPost = Post(post_id = 1, user_name = newUser.user_name, post_label = "sports", post_cap = "Football Team", post_picture = "TESTURL")

#     res = test_app.post('/index', data={
#             'post_id': "1", 
#             'user_name': "Test", 
#             'post_label': "sports", 
#             'post_cap': "Football Team", 
#             'post_picture': "TESTURL",
#         }, follow_redirects=True)

#     assert b'1' in res.data
#     assert b'Test' in res.data
#     assert b'sports' in res.data
#     assert b'Football Team' in res.data
#     assert b'TESTURL' in res.data