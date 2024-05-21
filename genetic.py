# Example Data
import random

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

budget = 800
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

def fitness(individual):
    print(individual)
    total_cost = float(individual['place']['price'].replace('$', '').replace(',', '')) + sum(activity['cost'] for activity in individual['activities'])
    print(total_cost)
    total_value = float(individual['place']['rating']) + sum(activity['value'] for activity in individual['activities'])
    
    if total_cost > budget:
        return 0
    return total_value



def selection(population):
    population.sort(key=fitness, reverse=True)
    return population[:population_size // 2]

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
    for generation in range(generations):
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

best_trip = genetic_algorithm()


print("Best Trip Plan:")
print(f"Hotel: {best_trip['place']['hotel']} - Cost: {best_trip['place']['price']}, Rating: {best_trip['place']['rating']}")
total_cost = float(best_trip['place']['price'].replace('$', '').replace(',', ''))
total_value = float(best_trip['place']['rating'])
for activity in best_trip['activities']:
    print(f"Activity: {activity['name']} - Cost: ${activity['cost']}, Value: {activity['value']}")
    total_cost += activity['cost']
    total_value += activity['value']
print(f"Total Cost: ${total_cost}")
print(f"Total Value: {total_value}")
