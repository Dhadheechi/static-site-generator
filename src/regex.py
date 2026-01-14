import re 

text = "I have a (cat) and a (dog)"
matches = re.findall(r"\((.*)\)", text)
print(matches) # ['cat', 'dog']
