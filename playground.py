if __name__ == "__main__":
    a = [1,2,3]
    b = [4,5,6]
    c= [x + y for x,y in zip(a,b)]
    print(c)
