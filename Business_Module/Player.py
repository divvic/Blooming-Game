from Business_Module import Opportunity_Package
from Business_Module.Profession import provide_profession
from random import randint


class Player (object):
    def __init__(self, pseudo, profession = provide_profession(), cashFlow = 0, cash = 0, childNumber = 0, liabilities = [], monthExpenses = [], investmentList = [], fundList = []):
        "Initialization of a player interface game"
        self.__mPseudo = pseudo
        self.__mProfession = profession
        self.__mSalary = self.__mProfession.get_salary()
        self.__mCashFlow = cashFlow
        self.__mChildNumber = childNumber
        # Condition des parametres par defaut ou par valeurs sur les dettes
        if(len(liabilities) == 0):
            self.__mLiabilities = self.__mProfession.get_liabilities()
        else:
            self.__mLiabilities = liabilities
        # Condition des parametres par defaut ou par valeurs sur les depenses mensuelles
        if(len(monthExpenses) == 0):
            self.__mMonthExpenses = self.__mProfession.get_monthExpenses()
        else:
            self.__mMonthExpenses = monthExpenses
        # Condition des parametres par defaut ou par valeurs sur le cash
        if(cash == 0):
            self.__mCash = self.__mSalary - self.get_sum_monthExpenses() + self.__mProfession.get_savings()
        else:
            self.__mCash = cash
        self.__mInvestments = investmentList # Liste des grandes opportunités
        self.__mFunds = fundList # Liste des petites opportunités


    def set_pseudo(self, pseudo):
        self.__mPseudo = pseudo
    

    def get_pseudo(self):
        return self.__mPseudo


    def set_liability(self, tupl = ("Liability name", 0)):
        self.__mLiabilities.append(tupl)
    

    def get_liabilities(self):
        return self.__mLiabilities
    

    def set_monthExpense(self, tupl = ("Expense name", 0)):
        self.__mMonthExpenses.append(tupl)
    

    def get_monthExpenses(self):
        return self.__mMonthExpenses
    

    def set_investment(self, invest):
        self.__mInvestments.append(invest)


    def get_investments(self):
        return self.__mInvestments


    def set_fund(self, fund):
        self.__mFunds.append(fund)


    def get_funds(self):
        return self.__mFunds


    def get_cashFlow(self):
        return self.__mCashFlow
    

    def get_salary(self):
        return self.__mSalary


    def pay (self, summ):
        self.__mCash -= summ


    def receive (self, summ):
        self.__mCash += summ


    def get_cash(self):
        return self.__mCash


    def get_childNumber(self):
        return self.__mChildNumber
    

    def get_sum_monthExpenses(self):
        summ = 0
        for tupl in self.get_monthExpenses():
            summ = summ + tupl[1]
        return summ


    def roll_dice(self):
        number = randint(1,6)
        print(".\n..\n...\n{} roll {}\n".format(self.get_pseudo(), number))
        return number
    

    def roll_2dice(self):
        number = randint(2,12)
        print(".\n..\n...\n{} roll {}\n".format(self.get_pseudo(), number))
        return number


    def status(self):
        print("===== PLAYER STATUS =====")
        print("Pseudo/Name : {}".format(self.get_pseudo()))
        print("Profession : {}".format(self.__mProfession.get_name()))
        print("Salary : {} Fcfa".format(self.get_salary()))
        print("CashFlow : {} Fcfa".format(self.get_cashFlow()))
        print("Number of child : {}".format(self.get_childNumber()))
        print("Total Expenses : {} Fcfa".format(self.get_sum_monthExpenses()))
        print("Cash : {} Fcfa\n".format(self.get_cash()))
        print("MONTH EXPENSES LIST")
        print("-------------------")
        for tupl in self.get_monthExpenses() :
            print("- {} : {} Fcfa".format(tupl[0], tupl[1]))
        print("\nLIABILITIES")
        print("-----------")
        for tupl in self.get_liabilities() :
            print("- {} : {} Fcfa".format(tupl[0], tupl[1]))
        print("")


    def has_a_baby(self):
        if(self.get_childNumber() >= 3):
            print("You alreary have 3 child, can't give you more MONSTER !!!")
        else:
            self.__mChildNumber += 1
            for tupl in self.get_monthExpenses() :
                if(tupl[0] == "Child(s) Expenses"):
                    self.get_monthExpenses().remove(tupl)
                    break
            num = self.get_childNumber() * int(self.get_salary()*0.1)  # Le budget d'un enfant vaut 10% du salaire
            self.set_monthExpense(("Child(s) Expenses", num))


    def buy_investment(self, opportunity):
        "Function for buying an investment"
        # Cas où le cash est inférieur à la somme de l'opportunité
        if (self.get_cash() < opportunity.get_payDown()):
            print("You can not buy this opportunity")
            while(True):
                sugg = input("Borrow ? (Y/N° : ")
                if (sugg in ("Yes", "yes", "Y", "y", "No", "no", "N", "n")):
                    break
            if (sugg in ("Yes", "yes", "Y", "y")):
                while (True):
                    summStr = input("How much do you want to borrow :")
                    try:
                        summ = int(summStr)
                        if (summ > 0):
                            self.borrow(summ)
                            self.buy_investment(opportunity)
                            break
                        else:
                            print("Enter a valid sum !")
                    except:
                        print("Enter a sum !")
            else:
                print("Opportunity too big.")
        # Cas d'achat normal de l'opportunité
        else:
            self.set_investment(opportunity)
            self.__mCashFlow += opportunity.get_cashFlow()
            self.set_liability((opportunity.get_name(), opportunity.get_cost()-opportunity.get_payDown()))
            self.pay(opportunity.get_payDown())


    def buy_funds(self, opportunity):
        "Function for buying a funds"
        if (self.get_cash() < self.get_cash() < opportunity.get_payDown()):
            print("You don't have enough money")
            while(True):
                sugg = input("Borrow ? (Y/N° : ")
                if (sugg in ("Yes", "yes", "Y", "y", "No", "no", "N", "n")):
                    break
            if (sugg in ("Yes", "yes", "Y", "y")):
                while (True):
                    summStr = input("How much do you want to borrow :")
                    try:
                        summ = int(summStr)
                        if (summ > 0):
                            self.borrow(summ)
                            self.buy_funds(opportunity)
                            break
                        else:
                            print("Enter a valid sum !")
                    except:
                        print("Enter a sum !")
            else:
                print("Opportunity too big.")
        else:
            self.set_fund(opportunity)
            self.__mCashFlow += opportunity.get_cashFlow()
            # Vérification de la somme à enlever du cash, selon la forme du small deal
            if (opportunity.get_payDown() == 0):
                self.pay(opportunity.get_shares()*opportunity.get_cost())
            else:
                self.pay(opportunity.get_payDown())


    def sell_investment(self, opportunity):
        "Function for selling an investment"
        self.get_investments().remove(opportunity)
        self.__mCashFlow -= opportunity.get_cashFlow()
        for tupl in self.get_liabilities():
            if(tupl[0] == opportunity.get_name()):
                self.get_liabilities().remove(tupl)
                break
        self.receive(opportunity.get_payDown())  # A revoir
    

    def sell_funds(self, opportunity):
        "Function for selling a fund"
        self.get_funds().remove(opportunity)
        self.__mCashFlow -= opportunity.get_cashFlow()
        self.receive(opportunity.get_shares()*opportunity.get_cost())


    def borrow(self, summ):
        "Function used when the player borrow at the Bank"
        self.receive(summ)
        # Cas où il y'a un prêt déjà en cours
        for tupl in self.get_liabilities():
            if(tupl[0] == "Loans"):
                x = True
                val = tupl[1]+summ
                self.get_liabilities().remove(tupl)
                self.get_liabilities().append((tupl[0], val))
                for tupl2 in self.get_monthExpenses():
                    if(tupl2[0] == "Loans Payment"):
                        self.get_monthExpenses().remove(tupl2)
                        self.get_monthExpenses().append((tupl2[0], int(val*0.1)))
                        break
                break
            else:
                x = False
        # Cas où il n'y a pas de prêt en cours
        if(x == False):
            self.get_liabilities().append(("Loans", summ))
            self.get_monthExpenses().append(("Loans Payment", int(summ*0.1)))


    def pay_debt(self):
        "Function called when the player want to pay their debt at the Bank"
        i, x = 1, 0
        print("REPAY")
        for tupl in self.get_liabilities():
            print("{} - {} : {} Fcfa".format(i, tupl[0], tupl[1]))
            i += 1
        while(x != 1):
            debt = input("\nWhat debt do you want to repay ? : ")
            try:
                debt = int(debt)
                if(debt > 0 or debt <= len(self.get_liabilities())):
                    x = 1
                else:
                    print("Enter a valid choice.")
                    x = 0
            except:
                print("Refund cancelled !\n")
                break
            if(x == 1):
                for j in range(1,i+1):
                    if(debt == j):
                        val = self.get_liabilities()[debt-1] # Sauvegarde du tuple avant suppression de la liste
                        if(self.get_cash() < val[1]):
                            print("Unable to pay this debt.\n")
                        else:
                            self.pay(val[1])
                            del self.get_liabilities()[debt-1]
                            for tupl in self.get_monthExpenses():
                                if(tupl[0] == val[0]+" Payment"):
                                    self.get_monthExpenses().remove(tupl)
                                    break
                            print("Debt paid !\n")
                        break

#===== Main test =======#

'''player = Player("Edghi")
player.status()
player.has_a_baby()
player.status()'''