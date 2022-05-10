from src.models import Users, Post

def test_homepage(test_app):
    res = test_app.get('/index')

    res = test_app.post('/index', data={
            'post_picture': "TESTURL",
        }, follow_redirects=True)

    assert res.status_code == 200
    assert b'TESTURL' in res.data