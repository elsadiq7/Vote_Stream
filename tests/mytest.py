from app.cal import add
def test_add():
    print("#" * 50)
    print("testing add function ")
    num1=1
    num2=2
    num3=3
    assert add(num1,num2)==num3

test_add()