import numpy as np

with open('2023/9/9.txt') as f:
    content = f.readlines()

content = [x.strip().lower() for x in content]

def work(line):
    numbers = line.split(' ')
    numbers = np.array([int(k.strip()) for k in numbers])
    
    return predict_next(numbers)

def predict_next(numbers):
    print(numbers)
    if len(numbers) < 2:
        print('bad input')
        return 0
    
    n_ = numbers[1:] - numbers[:-1]

    if np.all(n_ == n_[0]):
        return numbers[-1] + n_[0]
    else:
        return numbers[-1] + predict_next(n_)
    
print(predict_next(np.array([0, 3, 6, 9, 12, 15])))

res = list(map(work, content))
print(res)

print(sum(res))