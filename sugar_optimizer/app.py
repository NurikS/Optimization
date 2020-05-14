import pandas as pd
from pulp import *

def run_process():
    """Import data"""
    data = pd.read_csv("resultset.csv", sep=";")

    """
    Data cleaning.
    Create the helper columns, transform data and remove NaN values.
    """
    kJ2cal = 0.24
    data["energy,calculated (kcal)"] = data["energy,calculated (kJ)"]*kJ2cal
    data["name"] = data["name"].str.replace("-", "_")
    data["name"] = data["name"].str.replace(" ", "_")
    data["name"] = data["name"].str.replace(",", "_")
    data["name"] =  data["name"].str.replace("%", "pct")
    data["sugars, total (g)"].replace({"<0.1":0.1}, inplace=True)
    data["sugars, total (g)"] = data["sugars, total (g)"].astype("float")
    data["fat, total (g)"].replace({"<0.1":0.1}, inplace=True)
    data["fat, total (g)"] = data["fat, total (g)"].astype("float")
    data["protein, total (g)"].replace({"<0.1":0.1}, inplace=True)
    data["protein, total (g)"] = data["protein, total (g)"].astype("float")
    data["carbohydrate, available (g)"].replace({"<0.1":0.1}, inplace=True)
    data["carbohydrate, available (g)"] = data["carbohydrate, available (g)"].astype("float")
    data["fibre, total (g)"].replace({"<0.1":0.1}, inplace=True)
    data["fibre, total (g)"] = data["fibre, total (g)"].astype("float")
    food_options = data[["id", "name", "energy,calculated (kcal)", "fat, total (g)", "carbohydrate, available (g)",
                    "protein, total (g)", "fibre, total (g)", "sugars, total (g)" ]]
    food_options["amount (g)"] = 100

    food_options = food_options.dropna()

    food_items = food_options["name"]

    """Divide the dataset into 7 days"""
    mon = food_options[:593]
    tue = food_options[593:1186]
    wed = food_options[1186:1779]
    thu = food_options[1779:2372]
    fri = food_options[2372:2965]
    sat = food_options[2965:3558]
    sun = food_options[3558:]

    """Define necessary varibles"""
    sugar = dict(zip(food_items, food_options["sugars, total (g)"]))
    energy = dict(zip(food_items, food_options["energy,calculated (kcal)"]))
    fat = dict(zip(food_items, food_options["fat, total (g)"]))
    carbos = dict(zip(food_items, food_options["carbohydrate, available (g)"]))
    protein = dict(zip(food_items, food_options["protein, total (g)"]))
    fibre = dict(zip(food_items, food_options["fibre, total (g)"]))

    """Create  the  optimization tasks for each day"""
    prob1 = LpProblem("Monday", LpMinimize)
    prob2 = LpProblem("Tuesday", LpMinimize)
    prob3 = LpProblem("Wednesday", LpMinimize)
    prob4 = LpProblem("Thursday", LpMinimize)
    prob5 = LpProblem("Friday", LpMinimize)
    prob6 = LpProblem("Saturday", LpMinimize)
    prob7 = LpProblem("Sunday", LpMinimize)

    probs = {prob1:mon["name"], prob2:tue["name"], prob3:wed["name"],
            prob4:thu["name"], prob5:fri["name"], prob6:sat["name"], prob7:sun["name"]}
    food_vars = LpVariable.dicts("Food",food_items,lowBound=0,upBound=5,cat='Integer')

    """Add constraints"""
    for i in range(len(list(probs.keys()))):
        list(probs.keys())[i] += lpSum([sugar[f]*food_vars[f] for f in list(probs.values())[i]])
        list(probs.keys())[i] += lpSum([energy[f] * food_vars[f] for f in list(probs.values())[i]]) >= 1800.0, "CalorieMinimum"
        list(probs.keys())[i] += lpSum([energy[f] * food_vars[f] for f in list(probs.values())[i]]) <= 2200.0, "CalorieMaximum"
        
        list(probs.keys())[i] += lpSum([fat[f] * food_vars[f] for f in list(probs.values())[i]]) >= 20.0, "FatMinimum"
        list(probs.keys())[i] += lpSum([fat[f] * food_vars[f] for f in list(probs.values())[i]]) <= 50.0, "FatMaximum"
        
        list(probs.keys())[i] += lpSum([protein[f] * food_vars[f] for f in list(probs.values())[i]]) >= 60.0, "ProteinMinimum"
        list(probs.keys())[i] += lpSum([protein[f] * food_vars[f] for f in list(probs.values())[i]]) <= 100.0, "ProteinMaximum"
        
        list(probs.keys())[i] += lpSum([carbos[f] * food_vars[f] for f in list(probs.values())[i]]) >= 130.0, "CarbsMinimum"
        list(probs.keys())[i] += lpSum([carbos[f] * food_vars[f] for f in list(probs.values())[i]]) <= 450.0, "CarbsMaximum"
        
        list(probs.keys())[i] += lpSum([fibre[f] * food_vars[f] for f in list(probs.values())[i]]) >= 20.0, "FibreMinimum"
        list(probs.keys())[i] += lpSum([fibre[f] * food_vars[f] for f in list(probs.values())[i]]) <= 450.0, "FibreMaximum"



    """Solve and print""" 
    for i in probs:
        i.solve()

    for i in probs:
        for v in i.variables():
            if v.varValue:
                print(v.name , "=", v.varValue)
        print(value(i.objective))
        print("---------------------------------------")


if __name__ == '__main__':
    run_process()