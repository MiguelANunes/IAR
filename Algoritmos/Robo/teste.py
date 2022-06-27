
def get_all_but_one(myDicts:dict, ignore:tuple) -> dict:
    # myDicts é um dict de dicts
    # as chaves de myDicts são tuplas

    # os valores de myDicts[chave1] são dicts
    # as chaves de myDicts[chave1] são tuplas

    # os valores de myDicts[chave1][chave2] são ints

    # quero garantir que myDicts[key].get vai retornar um dict de dicts
    # onde myDicts[<chave>] irá retornar um dict que não tem a chave ignore

    outerDict = dict()
    #   || dict     || dict de dicts
    #   \/          \/
    for outerKey in myDicts:
        innerDict = dict()
            # || tupla   || dict
            # \/         \/      
        for innerKey in myDicts[outerKey]:
            if innerKey == ignore: continue
            innerDict[innerKey] = myDicts[outerKey][innerKey]
        outerDict[outerKey] = innerDict
    
    return outerDict


list = [(i,j) for i in range(2) for j in range(2)]

d1 = dict()
# dRobot = dict()
dItem = dict()
for pair in list:
    d1[pair] = pair[0]+pair[1]
    tempDict = dict()
    for pair1 in list:
        if pair1 == pair: continue
        tempDict[pair1] = (pair1[0]+pair1[1]) * (1 + (pair1[0]*pair1[1]))
    dItem[pair] = tempDict

print("list")
for p in list:
    print(p)
print("d1")
for k in d1:
    print(f"{k}: {d1[k]}")
print("dItem")
for k in dItem:
    print(f"{k}: {dItem[k]}")
    print(f"min_{k} =",min(dItem[k], key=dItem[k].get))
    newDict = get_all_but_one(dItem, (0,0))
    print(f"new_min_{k} =",min(newDict[k], key=newDict[k].get),"\n")

# print()
# print()

# newDict = get_all_but_one(dItem, (1,0))
# for k in newDict:
#     print(f"{k}: {newDict[k]}")
#     print(f"min_{k} =",min(newDict[k], key=newDict[k].get),"\n")