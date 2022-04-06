import os
filePath = 'F:\\树莓派ROS\\树莓派4B ROS机器人客户资料\\5.相关技术理论资料\\ROS机器人相关书籍\\'
for i,j,k in os.walk(filePath):
    print(k)
    print('\n')
    index = 0
    for n in k:
        index = index +1
        print(str(index) + '.'+n)
