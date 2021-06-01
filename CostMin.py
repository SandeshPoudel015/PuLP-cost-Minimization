# first of all, we import PuLP for linear programming
# pandas for excel handling and numpy for arrays

from pulp import *
import pandas as pd
import numpy as np

#reading the excel file, second sheet

df=pd.read_excel(r'MSTDistance.xlsx',sheet_name='valuesonly') 

# taking input of operating cost per km and converting to per meter

o_perkm1 = float(input('Enter the rate of operating cost over earthen roads per KM: NRs '))
o_perm1=o_perkm1/1000
o_perkm2 = float(input('Enter the rate of operating cost over gravelled roads per KM: NRs '))
o_perm2=o_perkm2/1000
o_perkm3 = float(input('Enter the rate of operating cost over asphalt roads per KM: NRs '))
o_perm3=o_perkm3/1000

# taking input of investment cost per km and converting to per meter

inv_perm1 = 0
inv_perkm2 = float(input('Enter the rate of investment per KM for Earthen to Gravel: NRs '))
inv_perm2=inv_perkm2/1000
inv_perkm3 = float(input('Enter the rate of investment per KM for Earthen to Asphalt: NRs '))
inv_perm3=inv_perkm3/1000

# taking total budget

budget = float(input("Enter total budget available: NRs "))

#taking the distance values

h=np.array(df)
d=h[:,3]

v= int(input("Enter number of vertices: "))
links=v-1

# defining the linear programming problem with LpProblem

prob = LpProblem("CostMin",LpMinimize)

# creating the dictionaries for decision variables x for all types of surfaces

Earthen= LpVariable.dicts("Earthen", list(range(links)), cat="Binary")
Gravel= LpVariable.dicts("Gravel", list(range(links)), cat="Binary")
Asphalt = LpVariable.dicts("Asphalt", list(range(links)), cat="Binary")


investment = 0 # to check the investment with bidget
op_cost = 0 # to store total operation cost in the objective function

for i in range(links):
    
    # the binary decision variables are summed to be 1 in total
    prob += Earthen[i] + Gravel[i] + Asphalt[i] == 1
  
    # sum up the investment
    investment += Earthen[i]*inv_perm1*d[i] + Gravel[i]*inv_perm2*d[i] + Asphalt[i]*inv_perm3*d[i]
    
    # objective funtion to minimize
    op_cost +=  Earthen[i]*d[i]*o_perm1 + Gravel[i]*d[i]*o_perm2 + Asphalt[i]*d[i]*o_perm3


prob += investment <= budget
prob += op_cost

# showing all the equations and constraints in the problem

print(prob)
status=prob.solve()
prob.solve()

# showing the solution of decision variables x

for i in range(links):
 print(int(value(Earthen[i])),'-',int(value(Gravel[i])),'-',int(value(Asphalt[i])))

# making the solution in array fornat
 
def list_of_solution():
    list_of_solution=[]
    for i in range(0,links):
        if int(value(Earthen[i]))==1:
          list_of_solution.append('E')
        if (int(value(Gravel[i]))==1):
          list_of_solution.append('G')
        if (int(value(Asphalt[i]))==1):
          list_of_solution.append('A')
    return list_of_solution

# finally printing out the solution

print('The  operation cost is: NRs ',value(prob.objective))
print('The  total investment utilized is: NRs ',value(investment))
print(list_of_solution())
print("Copy the array of E G and A to a csv file for your use")
print("Other items like variables, objective function, constraints, bounds, etc are also printed above")

