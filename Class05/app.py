import cal
def main():
    print("Main function")
    response = cal.add(5, 10)
    assert response == 15, "The addition result is incorrect" # This will raise an AssertionError if the condition is not met
    return response

if __name__ == "__main__":
    response = main()
    print(response)