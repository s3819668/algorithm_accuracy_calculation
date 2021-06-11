from operator import  attrgetter
import random
import time
class algorithm:
    def __init__(self,random_rate,sample):
        self.rate=0
        self.random_rate=random_rate
        self.correct=[]
        self.incorrect=[]
        for i in range(sample):
            if random_rate>random.uniform(0,1):
                self.correct.append(i)
            else:
                self.incorrect.append(i)

def inEveryAlgorithm(algorithm_pool,num,state,target=None):
    if state=="correct":
        for i in algorithm_pool :
            if i==target:
                pass
            elif num not in i.correct:
                return None
        return num
    else:
        for i in algorithm_pool :
            if i==target:
                pass
            elif num not in i.incorrect:
                return None
        return num

def main(algorithm_pool,sample):
    ####檢測每個都有
    ##正確
    common_correct = []
    for i in range(sample):
        temp = inEveryAlgorithm(algorithm_pool,i,"correct")
        if temp:
            common_correct.append(temp)
    ##錯誤
    common_incorrect = []
    for i in range(sample):
        temp = inEveryAlgorithm(algorithm_pool, i, "incorrect")
        if temp:
            common_incorrect.append(temp)

    ####排除單一項
    ##正確
    correct_without=[]
    for i in algorithm_pool:
        arr = []
        for j in range(sample):
            temp = inEveryAlgorithm(algorithm_pool,j,"correct",target=i)
            #排除NONE
            if temp:
                arr.append(temp)
        correct_without.append(arr)

    ####排除單一項
    ##錯誤
    incorrect_without = []
    for i in algorithm_pool:
        arr = []
        for j in range(sample):
            temp = inEveryAlgorithm(algorithm_pool, j, "incorrect", target=i)
            # 排除NONE
            if temp:
                arr.append(temp)
        incorrect_without.append(arr)

    ###計算單一準確率
    for i in range(len(algorithm_pool)):
        algorithm_pool[i].rate=(len(common_correct)+len(common_incorrect))/(len(correct_without[i])+len(incorrect_without[i]))
    return algorithm_pool

if __name__=="__main__":
    start_time = time.time()
    ####假資料創造
    sample = 4350  # 暫定寫死 資料進來後改為array, len array
    algorithm_num = 5
    algorithm_pool = [algorithm(0.9 + 0.01 * i, sample) for i in range(algorithm_num)]

    # #建立壞分類器
    algorithm_pool.append(algorithm(0.45,sample))
    algorithm_num=len(algorithm_pool)

    while True:
        algorithm_pool = main(algorithm_pool,sample)
        algorithm_pool=sorted(algorithm_pool, key=attrgetter("rate"))
        try:
            if algorithm_pool[0].rate<0.8:
                del algorithm_pool[0]
            if len(algorithm_pool)==algorithm_num:
                break
            algorithm_num=len(algorithm_pool)
        except:
            print("no one is better than .8")
            break

    incredibility=1
    for i in range(len(algorithm_pool)):
        incredibility*=(1-algorithm_pool[i].rate)
        print(algorithm_pool[i].rate)


    end_time = time.time()
    print("可信度為",(1-incredibility)*0.987)
    print("t", end_time - start_time)