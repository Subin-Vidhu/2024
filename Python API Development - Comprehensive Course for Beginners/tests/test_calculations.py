from app.calculations import add
def test_add():
    print("Test add")
    assert add(1, 2) == 3
    assert add(1, 1) == 2
    # false case
    assert add(1, 1) == 2
def test_add2():
    print("Test add2")
    assert add(1, 2) == 3
    assert add(1, 1) == 2
    # false case
    assert add(1, 1) == 2
# test_add()