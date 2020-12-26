import datetime,random
import UserAgent
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)
print(random_line('user-agents.txt'))
ua = UserAgent.UserAgent()
print (ua.random())
num2 = random.randint(10, 100)
print("Random integer: ", num2)