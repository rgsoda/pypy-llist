from pyllist import dllist


#Classical implementation, requires manipulations with indexes
def ins_sort(array):
    for i in range(1, len(array)):
        for k in range(i, 0, -1):
            if array[k] < array[k - 1]:
                array[k], array[k - 1] = array[k - 1], array[k]
    return array


#Linked-list implementation, demonstrates iteration starting from a given node
def ins_sort_llist(data):
    for card in data.first.next.iternext():  # Start iterating from the second!
        for left_card in card.iterprev():
            if left_card.prev is not None and left_card.value < left_card.prev.value:
                left_card.value, left_card.prev.value = left_card.prev.value, left_card.value
    return data


#Linked-list implementation, demonstrates other types of iteration
#and moves nodes instead of their values, which isn't really efficient
def ins_sort_llist2(data):
    for card in data.first.next.iternext():
        for left_card in data.iternodes(to=card):
            if left_card.value > card.value:
                data.remove(card)
                data.insert(card, before=left_card)
                break
    return data


data = [6, 5, 32, 8, 234, 5, 1, 9, 0, 33]
print(ins_sort(data))

data_llist = dllist([6, 5, 32, 8, 234, 5, 1, 9, 0, 33])
print(ins_sort_llist(data_llist))

data_llist = dllist([6, 5, 32, 8, 234, 5, 1, 9, 0, 33])
print(ins_sort_llist2(data_llist))
