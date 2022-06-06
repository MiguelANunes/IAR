valores1 = []
with open("teste1.txt") as f:
    for line in f:
        valores1.append(float(line))

# valores2 = []
# with open("teste2.txt") as f:
#     for line in f:
#         valores2.append(float(line))

# valores3 = []
# with open("teste3.txt") as f:
#     for line in f:
#         valores3.append(float(line))

# valores4 = []
# with open("teste4.txt") as f:
#     for line in f:
#         valores4.append(float(line))

# valores5 = []
# with open("teste5.txt") as f:
#     for line in f:
#         valores5.append(float(line))

res1 = sum(valores1)/len(valores1)
# res2 = sum(valores2)/len(valores2)
# res3 = sum(valores3)/len(valores3)
# res4 = sum(valores4)/len(valores4)
# res5 = sum(valores5)/len(valores5)

# final = sum([res1,res2,res3,res4,res5])/5
print(res1)
# print(res2)
# print(res3)
# print(res4)
# print(res5)