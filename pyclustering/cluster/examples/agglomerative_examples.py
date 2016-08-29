def bread(func):
    def wrapper():
        print("</------\>");
        func();
        print("</______\>");
        
    return wrapper;

def ingridients(func):
    def wrapper():
        print("#tomatos#");
        func();
        print("~salad~");
    
    return wrapper


@bread
@ingridients
def sandwich(food = "beef"):
    print(food);
    

sandwich();