name = "12340"

stripedName = name.rstrip(".001")

if name.endswith(".001"):
    strippedName = name[:-4]  # Remove the last 4 characters, which are ".001"
    print(strippedName)
else:
    print(name)