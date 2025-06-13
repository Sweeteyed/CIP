'''
Data source:
https://fdc.nal.usda.gov/api-guide
https://fdc.nal.usda.gov/data-documentation
https://fdc.nal.usda.gov/Foundation_Foods_Documentation
https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFoodsSearch
'''
import math, requests

API_KEY = 'S8I7hej4gTpNspFPKMyNg0cxQjERUkAbDNh6AYJB'
BASIC_MASS = 100
BASIC_MASS_U = 'g'
BASIC_ENERGY_U = 'kcal'

def main():
    greeting()
    energy_sum = 0
    energy_part = search_api()
    energy_sum = energy_sum + energy_part
    while continue_query(energy_sum) != False:
        energy_part = search_api()
        energy_sum = energy_sum + energy_part
    print(f'Total energy in your meal: {energy_sum} {BASIC_ENERGY_U}')

def greeting(): #prints a welcome message
    print('Welcome to the calories calculator!')
    print()
    print('This app allows you to search through a limited nutritional database for the caloric values of basic foods.')
    print('You will be able to calculate the energetic value of your meal, based on the ingredients you select, and their amounts you provide.')
    pause_enter = input('Press ENTER to continue...')

def search_api(): #sends a HTTP query to the database and recovers partial results
    potential_matches = []
    while potential_matches == []:
        food_name = input("Search for: ")
        http_addr = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={API_KEY}&query={food_name}&dataType=Foundation"
        response = requests.get(http_addr)
        response_data = response.json()
        #potential_matches = search_contains(food_name, response_data)
        potential_matches = search_startswith(food_name, response_data)
        ingredient = select(potential_matches) # = potential_matches[select_item]
    ing_energy100 = float(get_energy(ingredient))
    print(f'Energy per {BASIC_MASS}{BASIC_MASS_U}: {get_energy(ingredient)} {BASIC_ENERGY_U}')
    divide = float(input("Provide the amount of the ingredient in grams: "))
    energy_part = ((ing_energy100 * divide) / 100)
    print(f"Energy count: {energy_part} {BASIC_ENERGY_U} for {divide} grams of selected product")
    return energy_part

def continue_query(energy_sum): #asks user if they wish to add more ingredients or finish
    ans = input("Would you like to add another ingredient? (Y/N): ")
    while ans.lower() != 'y' and ans.lower() != 'n':
        print('Invalid input')
        ans = input('Would you like to add another ingredient? (Y/N): ')
    if ans.lower() == 'y':
        return True
    elif ans.lower() == 'n':
        #print(f'Total energy in your meal: {energy_sum} {BASIC_ENERGY_U}')
        return False

def get_energy(ingredient):
    for i in ingredient['foodNutrients']:
        if i['nutrientName'].startswith('Energy'):
            return i['value']

def select(potential_matches):
    """returns the list of potential matches if there are more than 1"""
    if len(potential_matches) == 0:
        print('No matches found. Please try again.')
        return True
    elif len(potential_matches) == 1:
        print(f'Showing results for: {potential_matches[0]['description']}')
        return potential_matches[0]
    else:
        select_item = list_selection(potential_matches)
        select_item = select_item - 1
        print(f'Showing results for:  {potential_matches[select_item]['description']}')
        return potential_matches[select_item]

def list_selection(potential_matches):
    view_potentialmatches(potential_matches)
    select_item = is_numeric(potential_matches)
    return select_item

def is_numeric(potential_matches):
    '''verifies if the user input is numeric'''
    select_item = input(f'Select entry (1 - {len(potential_matches)}): ')
    while select_item.isnumeric() == False or int(select_item) < 1 or int(select_item) > len(potential_matches):
        print('Invalid entry. Please try again.')
        print()
        view_potentialmatches(potential_matches)
        select_item = (input(f'Select entry (1 - {len(potential_matches)}): '))
    select_item = int(select_item)
    print(f'Selected: {select_item}')
    return select_item

def view_potentialmatches(potential_matches):
    for i in range(len(potential_matches)):
        print(f'{i + 1}. {potential_matches[i]['description']}')

def search_contains(food_name, response_data):
    '''an optional search method'''
    potential_matches = []
    for i in response_data['foods']:
        if i['description'].lower().__contains__(food_name.lower()) == True:
            potential_matches.append(i)
    return potential_matches

def search_startswith(food_name, response_data):
    potential_matches = []
    for i in response_data['foods']:
        if i['description'].lower().startswith(food_name.lower()):
            potential_matches.append(i)
    return potential_matches

if __name__ == '__main__':
    main()
