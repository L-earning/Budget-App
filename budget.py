import math


class Category:



  def __init__(self, category):
    self.category = category
    #each category has its own ledger
    self.ledger = []


  def __str__(self):
    total = 0
    result = str(self.category).center(30,"*") + '\n'
    for item in self.ledger:
      result += str(item["description"])[:23].ljust(23) + str("{:.2f}".format(item["amount"]).rjust(7)) +"\n"
      total += item["amount"]
    result += "Total: "+str(total)
    return result

  #takes an amount and an optional description as parameters
  #adds an object to the ledger list
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  #amount is to be withdrawed from the ledger, stored as a negative amount to show this
  #description is reason for withdrawl
  #if withdrawl amount is too high, it does not withdraw
  def withdraw(self, amount, description=""):
    #use check_funds method, if it is True, you can withdraw
    if self.check_funds(amount):
      #add withdrawl to ledger
      self.ledger.append({"amount": (amount * -1), "description": description})
      return True
    #no withdrawl took place
    return False

  #calculate the current balance
  def get_balance(self):
    balance = 0.00
    #access each dictionary in the list
    for item in self.ledger:
      #access each amount in the dictionaries, add them all together
      balance += item["amount"]
    return balance

  #transfer frunds from this category to another category
  def transfer(self, amount, category):
    #use check_funds method
    if self.check_funds(amount):
      #withdraw from this category
      self.withdraw(amount, f'Transfer to {category.category}')
      #transfer to other category
      category.deposit(amount, f'Transfer from {self.category}')
      return True
    #no transfer could be made, insufficient funds
    return False

  #check if funds are sufficient for amount given
  def check_funds(self, amount):
    balance = self.get_balance()

    #check if given amount is more than what you have
    if amount > balance:
      return False
    return True


#return a bar chart string of how much in percent was spent in each category
def create_spend_chart(categories):
  #calculate percentage of how much was spent(withdrawls) by each category
  total_each = []
  total_spent = 0.00
  len_longest_category = 0
  for category in categories:
    total_in_cat = 0.00
    for amount in category.ledger:
      #withdrawls are negative, hence if the amount is less than 0
      if amount["amount"] < 0.00:
        total_in_cat += amount["amount"]
      else:
        continue
    total_spent += total_in_cat
    total_each.append({
        "Category": category.category,
        "Amount spent": total_in_cat
    })
    if len(category.category) > len_longest_category:
      len_longest_category = len(category.category)


  percent_category = []
  #what each category is percentage wise of total spent
  for each in total_each:
    percent = (each["Amount spent"] / total_spent) * 10
    #round down to nearest 10 percent
    percent = math.floor(percent)
    #turn into percentage
    percent = int(percent * 10)
    percent_category.append({
      "Category": each["Category"], 
      "Percent": percent
    })


  result = "Percentage spent by category\n"

  i=100
  #first, print out the percent labels
  while i >= 0:
    result += str(i).rjust(3) + "| "
    #per percent label, for each category, add the percentage and more columns
    for cat in percent_category:
      cat_percent = cat["Percent"]
      if i <= cat_percent:
        result += "o  "
      else:
        result += "   "

    result += "\n"
    i -= 10

  result += "    -" + "---"*len(percent_category) + "\n"

  #print out each category
  for i in range(len_longest_category):
    result += "     "
    for j in range(len(percent_category)):
      if i < len(percent_category[j]["Category"]):
        result += percent_category[j]["Category"][i] + "  "
      else:
        result += "   "
    if i < len_longest_category-1:
      result += "\n"


  return result
