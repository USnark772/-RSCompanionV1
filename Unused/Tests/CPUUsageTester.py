from time import sleep as sl
while True:
    print("Hello World!")
    sl(.00000005)  # 100% cpu usage with no delay
