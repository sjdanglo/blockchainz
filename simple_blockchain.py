import json
import hashlib
import sys
import random

def main():

    ledger = {u'User_1': 5,u'User_2': 5}
    print("User 1 and User 2 both have 5 coins\n")
    print("Lets validate some transactions: \n")
    print("* User 1 buys 3 coins. Valid Transaction? ..." + str(isTxnValid({u'User_1': -3, u'User_2': 3}, ledger)))
    print("\n* User 1 now (tries) to buy 4 coins. Valid Transaction? ..." + str(isTxnValid({u'User_1': -4, u'User_2': 3}, ledger)))
    
    #adding new users doesn't work. :(
    '''print("\n* Sarah is new and buys 1 coin each from Users 1 and 2. Valid Transaction? ..." + str(isTxnValid({u'User_1': -4,u'User_2': 2,u'Sarah': 2}, ledger)))
    print("\n Sarah now (tries) to buy 10 coins from User_2. Valid Transaction? ..." + str(isTxnValid({u'User_1': -4,u'User_2': -8 ,u'Sarah': 12}, ledger)))'''

#Generate a hash for each blockchain transaction
def hashThis(transaction):
    if type(transaction) != str:   #Only generate hash if transaction is not a string
        transaction = json.dumps(transaction, sort_keys = True)  #Sort the keys, idk why???

    if sys.version_info.major == 2:   #if running python 2
        return unicode(hashlib.sha256(transaction).hexdigest(), 'utf-8')

    else: 
        return hashlib.sha256(str(transaction).encode('utf-8')).hexidigest()


#Genenete random transaction between 2 users
random.seed(0)  #initializes the random number generator
def makeTransaction(maxValue=3):
    sign = int(random.getrandbits(1))*2 - 1    #sign will be +1 or -1, a deposit or withdrawl
    amount = random.randint(1, maxValue)
    user1_pays = sign * amount
    user2_pays  = -1 *user1_pays      #ensures conservation of coins

    return {u'User_1':user1_pays, u'User_2':user2_pays}

#Update the state of a transaction
# INPUT: transactions = {username; transfer amount)
#        ledger = {username; amount balance)
# OUTPUT: updated balances, with new users added if necessary
def updateLedger(transactions, ledger):
    ledger = ledger.copy()
    for key in transactions:
        if key in ledger.keys():
            ledger[key] += transactions[key]   #adds transfer amount
        else:
            ledger[key] = transactions[key]    #adds a new user
    return ledger

#Validate a transaction
def isTxnValid(transactions, ledger):
    if sum(transactions.values()) is not 0:    #check that all transactions add up to 0
           return False
    
    for key in transactions.keys():      #for each user in the transaction dictionary
           
           if key in ledger.keys():    #if the user is in the ledger already
               accountBalance = ledger[key]  #set their account balance to the number of coins they have by looking at the ledger
           else:
               accountBalance = 0  #or if the user isn't in the ledger, they start of with a balance of 0. this is okay
           if (accountBalance + ledger[key]) < 0:
               return False   #if the user's balance is less than 0 after the transaction, the user overdrafted. this is NOT okay
           return True



if __name__ == "__main__": main()
