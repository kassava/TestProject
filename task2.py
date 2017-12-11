a = input("1 value: ")
b = input("2 value: ")
a = int(a)
b = int(b)


def nod_recur(num1, num2):
    n = num1 % num2
    num1 = num2
    num2 = n
    if n > 0:
        return nod_recur(num1, num2)
    else:
        return num1


print(a * b / nod_recur(a, b))
