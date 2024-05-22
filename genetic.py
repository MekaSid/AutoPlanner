# Example Data
import random

# Just run the code using python genetic.py

hotels = [
    {'hotel': 'Normandie Hostel', 'price': '$302', 'rating': '8.1'}, 
    {'hotel': 'The Delphi Hotel', 'price': '$1,160', 'rating': '8.1'}, 
    {'hotel': '8th and Ardmore', 'price': '$208', 'rating': '7.9'}, 
    {'hotel': 'Marina del Rey Marriott', 'price': '$2,034', 'rating': '8.1'}, 
    {'hotel': 'PodShare DTLA', 'price': '$424', 'rating': '6.8'}, 
    {'hotel': "Gorgeous Hollywood Apts LA's Best Location and Amazing Roof Deck", 'price': '$1,058', 'rating': '8.7'}, 
    {'hotel': 'The Metric - Los Angeles Downtown', 'price': '$1,354', 'rating': '9.2'}, 
    {'hotel': 'STILE Downtown Los Angeles by Kasa', 'price': '$761', 'rating': '7.8'}, 
    {'hotel': 'Cityscape Luxury Rental Homes in the Heart of Los Angeles', 'price': '$1,152', 'rating': '9.0'}, 
    {'hotel': 'citizenM Los Angeles Downtown', 'price': '$1,134', 'rating': '8.8'}, 
    {'hotel': 'Fenix Hotel Hollywood', 'price': '$1,545', 'rating': '8.3'}, 
    {'hotel': 'Los Angeles Premium 2BR&2BT Suites with Free Parking', 'price': '$2,500', 'rating': '8.8'}, 
    {'hotel': 'Short Stories Hotel', 'price': '$1,804', 'rating': '8.6'}, 
    {'hotel': 'The Westin Bonaventure Hotel & Suites, Los Angeles', 'price': '$1,583', 'rating': '8.2'}, 
    {'hotel': 'Park Plaza Lodge', 'price': '$1,822', 'rating': '8.6'}, 
    {'hotel': 'tommie Hollywood, part of Jdv by Hyatt', 'price': '$1,248', 'rating': '8.0'}, 
    {'hotel': 'The LINE Hotel LA', 'price': '$1,264', 'rating': '7.6'}, 
    {'hotel': 'AC Hotel by Marriott Downtown Los Angeles', 'price': '$1,372', 'rating': '8.2'}, 
    {'hotel': 'Moxy Downtown Los Angeles', 'price': '$1,362', 'rating': '8.0'}, 
    {'hotel': 'Hotel June West LA, a Member of Design Hotels', 'price': '$1,393', 'rating': '8.2'}, 
    {'hotel': 'E Central Hotel Downtown Los Angeles', 'price': '$1,270', 'rating': '8.5'}, 
    {'hotel': '4 Star Motel', 'price': '$559', 'rating': '6.8'}, 
    {'hotel': "Hampton Inn Los Angeles Int'l Airport/Hawthorne", 'price': '$1,192', 'rating': '8.2'}, 
    {'hotel': 'USC Hotel', 'price': '$1,290', 'rating': '8.5'}, {'hotel': 'Omni Los Angeles Hotel', 'price': '$1,721', 'rating': '8.6'}, {'hotel': 'The Biltmore Los Angeles', 'price': '$1,342', 'rating': '7.6'}
]

activities = [
    {'name': 'Touring Universal Studios Hollywood', 'cost': 100, 'value': 9.5},
    {'name': 'Enjoying a day at Disneyland Resort', 'cost': 150, 'value': 9.5},
    {'name': 'Taking a studio tour at Warner Bros. Studio', 'cost': 60, 'value': 9.0},
    {'name': 'Watching a concert at the Hollywood Bowl', 'cost': 50, 'value': 9.0},
    {'name': 'Attending a performance at the Greek Theatre', 'cost': 50, 'value': 9.0},
    {'name': 'Visiting the Los Angeles County Museum of Art (LACMA)', 'cost': 25, 'value': 9.0},
    {'name': 'Attending a game at Dodger Stadium', 'cost': 30, 'value': 8.5},
    {'name': 'Visiting the Getty Center', 'cost': 20, 'value': 9.0},
    {'name': 'Taking a scenic drive along Pacific Coast Highway', 'cost': 0, 'value': 8.0},
    {'name': 'Exploring the Griffith Observatory', 'cost': 0, 'value': 8.5},
    {'name': 'Shopping on Rodeo Drive', 'cost': 0, 'value': 8.0},
    {'name': 'Strolling along Santa Monica Pier', 'cost': 0, 'value': 8.0},
    {'name': 'Attending a live taping of a TV show', 'cost': 0, 'value': 8.0},
    {'name': 'Exploring Venice Beach', 'cost': 0, 'value': 7.5},
    {'name': 'Hiking in Griffith Park', 'cost': 0, 'value': 8.5},
    {'name': 'Biking along the Venice Beach Boardwalk', 'cost': 0, 'value': 7.5},
    {'name': 'Checking out the Hollywood Walk of Fame', 'cost': 0, 'value': 7.0},
    {'name': 'Exploring the Museum of Contemporary Art (MOCA)', 'cost': 15, 'value': 8.0},
    {'name': 'Exploring the California Science Center', 'cost': 0, 'value': 8.0},
    {'name': 'Taking a scenic drive along Mulholland Drive', 'cost': 0, 'value': 8.0},
    {'name': 'Exploring the Japanese American National Museum', 'cost': 12, 'value': 8.0},
    {'name': 'Attending a performance at the Ahmanson Theatre', 'cost': 50, 'value': 9.0},
    {'name': 'Visiting the Griffith Park Merry-Go-Round', 'cost': 0, 'value': 7.0},
    {'name': 'Relaxing at Echo Park Lake', 'cost': 0, 'value': 7.5}
]

# {'destination': 'Los Angeles', 'start_date': '2024-05-22', 'return_date': '2024-05-30', 'budget': '4000', 'adults': '1', 'children': '0', 'rooms': '1'}

# Here are the variables you can change 
# budget = total price maximum
# trip_length = how long your trip is supposed to me 
budget = 1500
trip_length = 6

# Don't change this
population_size = 10
generations = 50
mutation_rate = 0.1

def create_individual():
    individual = {
        'place' : random.choice(hotels),
        'activities' : random.sample(activities, random.randint(1, len(activities)))
    }
    return individual

def create_population(size):
    return [create_individual() for _ in range(size)]

def calculate_cost(individual):
    hotel_cost_per_night = float(individual['place']['price'].replace('$', '').replace(',', ''))
    total_hotel_cost = hotel_cost_per_night * trip_length
    total_activity_cost = sum(activity['cost'] for activity in individual['activities'])
    return total_hotel_cost + total_activity_cost

def fitness(individual):
    total_cost = calculate_cost(individual)
    total_value = float(individual['place']['rating']) + sum(activity['value'] for activity in individual['activities'])
    
    if total_cost > budget:
        return 0
    return total_value



def selection(population):
    population.sort(key=fitness, reverse=True)
    filtered_population = [individual for individual in population if fitness(individual) > 0]
    while len(filtered_population) < 2:
        filtered_population.append(random.choice(population))
    return filtered_population[:population_size // 2]

def remove_duplicates(activities):
    seen = set()
    unique_activities = []
    for activity in activities:
        if activity['name'] not in seen:
            unique_activities.append(activity)
            seen.add(activity['name'])
    return unique_activities

def crossover(parent1, parent2):
    child1 = {
        'place' : random.choice([parent1['place'], parent2['place']]),
        'activities' : remove_duplicates(parent1['activities'] + parent2['activities'])
    }

    child2 = {
        'place' : random.choice([parent1['place'], parent2['place']]),
        'activities' : remove_duplicates(parent1['activities'] + parent2['activities'])
    }
    return child1, child2

def mutate(individual):
    if random.random() < mutation_rate:
        individual['place'] = random.choice(hotels)
    if random.random() < mutation_rate:
        if individual['activities']:
            individual['activities'].remove(random.choice(individual['activities']))
        individual['activities'].append(random.choice(activities))

def genetic_algorithm():
    population = create_population(population_size)
    for _ in range(generations):
        selected_population = selection(population)
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = new_population
    best_individual = max(population, key=fitness)
    return best_individual

# Run the genetic_algorithm multiple times and select the best one under the budget and 
# has the highest value instead of manually checking within the algorithm itself 

def run_multiple_times(runs, budget):
    best_individual = None
    best_fitness = 0
    
    for _ in range(runs):
        individual = genetic_algorithm()
        individual_fitness = fitness(individual)
        
        if individual_fitness > best_fitness and budget >= calculate_cost(individual):
            best_individual = individual
            best_fitness = individual_fitness
    
    return best_individual



best_individual = run_multiple_times(500, budget)

if best_individual:
    print("Best Trip Plan:")
    print(f"Hotel: {best_individual['place']['hotel']} - Cost: {best_individual['place']['price']}, Rating: {best_individual['place']['rating']}")
    
    total_cost = calculate_cost(best_individual)
    total_value = float(best_individual['place']['rating'])

    for activity in best_individual['activities']:
        print(f"Activity: {activity['name']} - Cost: ${activity['cost']}, Value: {activity['value']}")
        total_value += activity['value']
    
    print(f"Total Cost: ${total_cost}")
    print(f"Total Value: {total_value}")
else:
    print("No suitable trip found within the budget.")

