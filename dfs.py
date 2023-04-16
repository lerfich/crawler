import json
 
# Opening JSON file

with open('./results/data.json') as json_file:
    data = json.load(json_file)
 
allLinks = []
for key, value in data.items():
    temp = [key, value]
    allLinks.append(temp)


counter = 0
ter = 0
for link in allLinks:
    if (link[1] == 'Checked'):
        counter += 1
    else:
        ter += 1    

print(allLinks[0])
print(counter, ter)