'''
Name: Chung-Hsin(Jack) Hou
'''

import requests, json, copy
from collections import defaultdict


# modified binary search to search for one product.
def findOne(seq, goal):
    if not seq:
        return None
    
    min = 0
    max = len(seq) - 1
    #if the goal price is larger than the max price, simply return the max price. 
    if goal > seq[max]:
        return [seq[max]]
    
    while True:
        if max < min:
            if goal > seq[m]:
                # determines the closeset value with respect to goal value
                if abs(goal-seq[m]) < abs(goal-seq[m+1]):
                    return [seq[m]]
                else:
                    return [seq[m+1]]
                    
            else:
                if abs(goal-seq[m]) < abs(goal-seq[m-1]):
                    return [seq[m]]
                else:
                    return [seq[m-1]]
                
        m = (min + max) // 2
        if seq[m] < goal:
            min = m + 1
        elif seq[m] > goal:
            max = m - 1
        else:
            return [seq[m]]


# using two pointers, compare the first and last element in an array to minimize the price differnece
def findTwo(seq, goal):
    if not seq:
        return None
    
    left = 0
    right = len(seq) - 1

    # initialize the tracker for the differences
    goalDifference = float("inf")
    dl = -1
    dr = -1

    # as long as the tracker on the left of the list is less than the tracker on the right of the list...
    while(left < right):

        # keep track of the closest differences right now. 
        if(abs(goal - (seq[left] + seq[right])) < goalDifference):
            goalDifference = abs(goal - (seq[left] + seq[right]))
            dl = left
            dr = right
        # if a goal is found, simply returns
        if(seq[left] + seq[right] == goal):
            return [seq[left], seq[right]]
        
        elif(seq[left] + seq[right] < goal):
            left += 1
         
        else:
            right -= 1

    # if nothing is found after the while loop, return the best left and right tracker
    return [seq[dl], seq[dr]]


# using three trackers similar to findTwo(), find the cloest three elements
def findThree(seq, goal):
    if not seq:
        return None

    # initialize the differences 
    goalDifference = float("inf")
    dl = -1
    dr = -1
    dx = -1
    
    for x in range(len(seq)-1):
        
        left = x+1
        right = len(seq)-1

        
        while (left < right):

            tmp = seq[left] + seq[right] + seq[x]

            # if the absolute value of the previous set and the goal is less than the current goalDifference, keep track of the new set
            if(abs(goal - (seq[left] + seq[right] + seq[x])) < goalDifference):
                goalDifference = abs(goal - (seq[left] + seq[right] + seq[x]))
                dl = left
                dr = right
                dx = x
            
            if tmp > goal:
                right -= 1
            elif tmp < goal:
                left += 1
            else:
                return [seq[left],seq[right],seq[x]]

    # if no match is found, return the closest set using the tracker values
    return [seq[dl],seq[dr], seq[dx]]



# findFourPlus will utilizes the subset_sum function to find the most suitable subset_sum given an itemCount
def findFourPlus(itemCount, seq, goal):

    #hello, world
    hello = subset_sum(itemCount, seq, goal, partial=[])
    # if hello is not None, return its value. Otherwise, let's do some searching...
    if not hello is None:        
        return hello
    # since there is no efficient way of implementing subset_sum, I've decided to simply broaden the search range from [goal-200, goal+200] and hope
    # that one of the value will stike the gold mine. This is an inefficent approach for a huge list of prices, but since the API
    #only returns at most 10 prices, the run-time will still be relatively reasonable for this case.
    else:
        tempGoal = 0
        if (goal - 200 < 0):
            tempGoal = goal
        else:
            tempGoal = goal - 200
        # keep on searching for a potential match
        while(tempGoal <= goal+200):
            # hello world, again
            hello = subset_sum(itemCount, seq, tempGoal, partial=[])
            if not hello is None:
                return hello
            else:
                tempGoal += 1     
            
# subset_sum implementation using recursion. 
def subset_sum(itemCount, seq, goal, partial):
    s = sum(partial)

    # check if the partial sum is equals to target
    if(len(partial) == itemCount):
        if s == goal:
                return partial 

    for i in range(len(seq)):
        n = seq[i]
        remaining = seq[i+1:]
        t = subset_sum(itemCount, remaining, goal, partial + [n])
        if t:
            return t
    

# prints out the final results
def returnResult(a, limit, dictionary):
    print("with around $", limit, ",you can get...")
    currentSum = 0
    for x in range(len(a)):
        currentSum += a[x]
        print("    ", dictionary[a[x]][0], " for $", a[x])
        del dictionary[a[x]][0]
    print("for a total of $", currentSum, "!!")

# main body!
def main():

    # my awesome api key
    key = "52ddafbe3ee659bad97fcce7c53592916a6bfd73"

    #Added another field to utilize the seach API. Before anything users will be asked what kind of product they are looking for
    search_term = input("What type of product are you looking for?? (ie: boots, swimsuits, tanktops...) ")
    search_term = search_term.replace(" ", "_")

    #asks the user for the quantity. Catches potential errors such as quantity < 1 or not a number at all.
    while True:
        try:
            quantity = int(input("How many do you want?? "))
        except ValueError:
            print("Please enter a whole number!")
            continue

        if quantity < 1:
            print("Please enter a positive quantity!")
            continue
        else:
            break

    # asks for how many items the user wants
    while True:
        try:
            limit = int(input("Around how much are you willing to spend?? (no decimals please!) "))
        except ValueError:
            print("Please enter a whole number!")
            continue
        else:
            break
        
    # set up the data from the server!
    r = requests.get("http://api.zappos.com/Search?term="+search_term+"&key="+key) 
    data = r.json()

    #get the data from the API
    prices = [item["originalPrice"] for item in data["results"]]
    brandName = [item["brandName"] for item in data["results"]]
    productName = [item["productName"] for item in data["results"]]

    # strip the $ sign from all prices and sort the prices in order
    for x in range(len(prices)):
        prices[x] = float(prices[x][1:])
    prices = sorted(prices)

    # save the prices into a dictionary, with the key being the prices and the values being what kind of products are associated with that price
    dictionary = defaultdict(list)
    for x in range(len(prices)):
        dictionary[prices[x]].append(brandName[x]+" "+productName[x])

        
    # determine how many items user wants and use the appropriate functions
    if(quantity == 1):
        a = findOne(prices, limit)
        if a is None:
            print("Sorry, no results found :(")
        else:
            print("with around $" , limit ,", you can get a " , dictionary[a[0]][0], " for $" , a[0] ,"!")
        
    elif(quantity == 2):
        a = findTwo(prices, limit)
        if a is None:
            print("Sorry, no results found :(")
        else:
            returnResult(a, limit, dictionary)
        
    elif(quantity == 3):
        a = findThree(prices, limit)
        if a is None:
            print("Sorry, no results found :(")
        else:
            returnResult(a, limit, dictionary)
        
    else:
        a = findFourPlus(quantity, prices, limit)
        if a is None:
            print("Sorry, no combinations were found within $200 of your desired budget :(")
        else:
            returnResult(a, limit, dictionary)
            
        
if __name__ == "__main__":
    main()
    input('Press Any Key to exit')










