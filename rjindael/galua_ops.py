def x_02(num):
    if num < 0x80:
        res = (num<<1)
    else:
        res = (num<<1)^0x1b
    return res % 0x100

def x_03(num):
    return x_02(num)^num

def x_09(num):
    return x_02(x_02(x_02(num)))^num

def x_0b(num):
    return x_02(x_02(x_02(num)))^x_02(num)^num    

def x_0d(num):
    return x_02(x_02(x_02(num)))^x_02(x_02(num))^num

def x_0e(num):
    return x_02(x_02(x_02(num)))^x_02(x_02(num))^x_02(num)    