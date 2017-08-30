from time import ctime,sleep

def music(func):
    for i in range(2):
        print("I was listening to music",func,i,ctime())
        sleep(1)

def movie(func):
    for i in range(2):
        print("I was at the movie !",func,i,ctime())
        sleep(5)
if __name__ == '__main__':
    music("少年二十五六时")
    movie("The Shawshank Redemption")
    print("all over",ctime())