import requests
import random
from twilio.rest import Client

account_sid = "ACf9d710510a3e71df488fcdb209e02bbe"
auth_token  = "0709e5ad8b67972c60bda0cea54de381"

def get_distance(address1, address2):
    data = requests.get(f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={address1}&destinations={address2}&key=AIzaSyCRjohDPZ0D83rNb2Nh2N8VGNgJXKBdenM").json()
    return data["rows"][0]["elements"][0]["distance"]["value"]

def send_sms(to, body):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to, 
        from_="+12243520240",
        body=body)

    return True

def create_mega_route(addresses):
    # Encode addresses for URL
    encoded_addresses = [address.replace(' ', '+') for address in addresses]

    # Start with the base URL for directions
    base_url = "https://www.google.com/maps/dir/"

    # Add all addresses to the URL
    url_with_addresses = base_url + '/'.join(encoded_addresses)

    return url_with_addresses

def calculate_total_distance(distances_dict, children):
    total_distance = 0
    for x in range(len(children) - 1):
        child1 = children[x]
        child2 = children[x+1]
        if distances_dict.get(f"{child1}-{child2}"):
            total_distance += distances_dict[f"{child1}-{child2}"]
        else:
            total_distance += distances_dict[f"{child2}-{child1}"]

    return total_distance


def get_all_distances(addresses):
    distances = {}
    for x in range(len(addresses)):
        for y in range(x+1, len(addresses)):
            distances[f"{x}-{y}"] = get_distance(addresses[x], addresses[y])
    return distances


def geocode_address(address):
    data = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyCRjohDPZ0D83rNb2Nh2N8VGNgJXKBdenM").json()
    return data["results"][0]["geometry"]["location"]


def makeGenChildren(numAddresses):
    parent = []
    parentList = []
    for i in range(0, numAddresses):
        parent.append(i)
    def generationEmpty():
        def randomizeRoute():
            
            listP = parent
            for _ in range(100):
                i = random.randint(0, len(listP) - 1)
                j = random.randint(0, len(listP) - 1)
                while(i == j):
                    j = random.randint(0, len(listP) - 1)
                temp = listP[i]
                listP[i] = listP[j]
                listP[j] = temp
            parentList.append(listP.copy())
            

        def createParents():
            x = 0
            while(x < 50):
                randomizeRoute()
                x += 1
            
                
        createParents()

        def createChildren(parent1, parent2):
            child = []
            portion1 = len(parent1) // 3
            portion2 = (len(parent2) * 2) // 3
            child = parent1[:portion1] + parent2[portion1:portion2] + parent1[portion2:]
            
            replaceDuplicates(child)
                        
            i = random.randint(0, len(child) - 1)
            j = random.randint(0, len(child) - 1)
            while(i == j):
                j = random.randint(0, len(child) - 1)
            temp = child[i]
            child[i] = child[j]
            child[j] = temp
            
            return child
            
        def replaceDuplicates(childX):
            
            duplicates = getDuplicates(childX)
            
            missing = findMissing(childX)
            for x in childX:
                for y in duplicates:
                    if(x == y): 
                        if len(missing) > 0:
                            childX[childX.index(x)] = missing[0]
                            del missing[0]
                        duplicates.remove(x)
                    
                        

            
                    
        def getDuplicates(childX):
            duplicateList = []
            temp = list(childX)
            for x in range(len(temp)):
                for j in range(len(temp)):
                    if (temp[x] == temp[j] and x != j):
                        duplicateList.append(temp[x])
                        break
            duplicateList = set(duplicateList)
            duplicateList = list(duplicateList)
            return duplicateList
                        
        def findMissing(childX):
            temp = list(parent)
            for x in childX:
                for i in temp:
                    if(x == i):
                        temp.remove(x)
            
            return temp

        def findOptimalRoute():
            children = []
            for i in range(0, len(parentList)):
                if(i == len(parentList) - 1):
                    children.append(createChildren(parentList[i], parentList[0]))
                    
                else:
                    children.append(createChildren(parentList[i], parentList[i+1]))
                    
            
            return children

        return findOptimalRoute()

    def generation(parentList):

        def createChildren(parent1, parent2):
            child = []
            portion1 = len(parent1) // 3
            portion2 = (len(parent2) * 2) // 3
            child = parent1[:portion1] + parent2[portion1:portion2] + parent1[portion2:]
            
            replaceDuplicates(child)
            
            
            i = random.randint(0, len(child) - 1)
            j = random.randint(0, len(child) - 1)
            while(i == j):
                j = random.randint(0, len(child) - 1)
            temp = child[i]
            child[i] = child[j]
            child[j] = temp
            
            return child
            
        def replaceDuplicates(childX):
            
            duplicates = getDuplicates(childX)
           
            missing = findMissing(childX)
            for x in childX:
                for y in duplicates:
                    if(x == y): 
                        if len(missing) > 0:
                            childX[childX.index(x)] = missing[0]
                            del missing[0]
                        duplicates.remove(x)
            
                    
        def getDuplicates(childX):
            duplicateList = []
            temp = list(childX)
            for x in range(len(temp)):
                for j in range(len(temp)):
                    if (temp[x] == temp[j] and x != j):
                        duplicateList.append(temp[x])
                        break
            duplicateList = set(duplicateList)
            duplicateList = list(duplicateList)
            return duplicateList
                        
        def findMissing(childX):
            temp = list(parent)
            for x in childX:
                for i in temp:
                    if(x == i):
                        temp.remove(x)
            
            return temp

        def findOptimalRoute():
            children = []
            
            for i in range(0, len(parentList)):
                if(i == len(parentList) - 1):
                    children.append(createChildren(parentList[i], parentList[0]))
                    
                else:
                    children.append(createChildren(parentList[i], parentList[i+1]))
                    
            
            return children

        return findOptimalRoute()

    
    
    children = generation(generation(generation(generation(generationEmpty()))))
    return children
    
    
def findBestChild(distance_dict, num):
    distances = []
    genChildren = makeGenChildren(num)
    for i in genChildren:
        distances.append(calculate_total_distance(distance_dict, i))
    min = distances[0]
    min_list = genChildren[0]
    for j in range(len(distances)):
        if(distances[j] < min):
            min = distances[j]
            min_list = genChildren[j]
    return min_list