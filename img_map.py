def add_reverse(dictionary):
    new_dictionary = {}

    for key, value in dictionary.items():
        new_dictionary[key] = value
        new_dictionary[value] = key

    return new_dictionary
    
img_map = add_reverse({
    "0,3": "3,0",
    "0,2": "2,0",
    "1,3": "3,1",
})
