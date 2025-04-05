import cal
def test_main():
    response = cal.add(5, 10)
    assert response == 15, "5+10 should be 15" # This will raise an AssertionError if the condition is not met
    print ("Test Passed")


if __name__ == "__main__":
    test_main()