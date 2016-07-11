def calc():
    #emu = input("EMU?\n")
    #emu = int(emu)
    emu = 470

    # How many items to calculate
    n = input("Number of items:\n")
    n = int(n)

    #stores the items weight and quantity in a dict 
    items = {}

    # Names each item and stores it's weight and quanitty
    for times in range(n):
        # creates the weight of item
        item_emu = int(input("EMU of Item{}:\n".format(times+1)))
        items['item'+str(times)] = item_emu

        # Creates the number to use
        n_items = int(input("How many:\n"))
        items['item'+str(times)] =(items['item'+str(times)], n_items)

    count = 0
    counter = 0 
    while counter < emu:
        for item in items.values():
            counter += item[0] * item[1]
        count += 1
    # just in case it goes over emu
    if counter > emu:
        count -= 1

    sorted_list = []

    for item in items.keys():
        sorted_list.append(item)

    sorted_list.sort()

    for item in sorted_list:
        print("{} = {}".format(item,  items[item][1]* count))



calc()
