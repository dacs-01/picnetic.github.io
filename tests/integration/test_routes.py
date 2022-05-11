# def test_comments(test_app):
#     res = test_app.get('/comment/<comment_id>')

#     res = test_app.post('/comment/<comment_id>', data={
#             'comment': "Nice Picture!"
#         }, follow_redirects=True)

#     assert res.status_code == 200
#     assert b'Nice Picture!' in res.data
