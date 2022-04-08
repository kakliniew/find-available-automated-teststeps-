
dictionary = []

def find_dictionary(path):
    with open(path, "r") as f2:
        data = f2.readlines()
        for x in data:
            if "@" not in x and "Scenario" not in x and "Feature" not in x and x.strip():
                x = x.replace("When ", "").replace("Then ", "").replace("And ", "").replace("Given ", "")\
                    .replace("\n","").rstrip().lstrip()
                dictionary.append(x)
    return dictionary


dictionary = find_dictionary("example.feature")

print(dictionary)

