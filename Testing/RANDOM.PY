def listify(item1, item2):
    pair = [item1, item2]
    print(pair)
    returnList = []
    for item in pair:
        count = 0
        newItem = ""
        li = []
        for ch in item:
            if ch == "[":
                newItem += ch
                count += 1
            elif ch == "]":
                newItem += ch
                count -= 1
            elif ch == "," and count == 0:
                li.append(newItem)
                newItem = ""
            else:
                newItem += ch
        if newItem != "":
            li.append(newItem)
        returnList.append(li)

    return returnList

def compare(item1, item2):
    print(f"Comparing {item1} and {item2}")
    if item1.isnumeric() == item2.isnumeric() == True:
        if int(item1) < int(item2):
            return True
        elif int(item1) > int(item2):
            return False
        else:
            return None

    l1, l2 = listify(item1, item2)
    print(l1,l2)

    for i1, i2 in zip(l1,l2):
        result = compare(i1,i2)
        if result is None:
            pass
        else:
            return result

    if len(l1) < len(l2):
        return True
    elif len(l1) > len(l2):
        return False
    else:
        return None

print(compare("3", "3,[]"))