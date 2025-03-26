DIRECTIONS = ['N', 'E', 'S', 'W']
COMMANDS = {'F', 'R', 'L'}

class Car:
    def __init__(self, name, x, y, direction, commands):
        # Initialize 
        self.name = name
        self.initial_x = int(x)  # Store the initial x position
        self.initial_y = int(y)  # Store the initial y position
        self.x = self.initial_x  # Current x position
        self.y = self.initial_y  # Current y position 
        self.direction = direction
        self.initial_direction = direction.upper()
        self.direction = self.initial_direction 
        self.commands = commands
        self.step_count = 0 
        self.stopped = False  

    def __str__(self):
        return f"{self.name}, ({self.initial_x},{self.initial_y}) {self.initial_direction}, {self.commands}"

    def update_position(self, x, y):
        """Update the car's current position."""
        self.x = x
        self.y = y        
    
    def update_direction(self, direction):
        """Update the car's current direction."""
        self.direction = direction        


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cars = {} 

    def add_car(self, car):
        self.cars[car.name] = car

class SimulationEngine:
    def __init__(self, field):
        self.field = field
        self.collisions = []

    def process_commands(self):
        max_steps = max(len(car.commands) for car in self.field.cars.values())

        for step in range(max_steps):
            for car in self.field.cars.values():
                # Skip stopped cars
                if car.stopped:
                    continue 
                 # If the car has finished all commands 
                if car.step_count >= len(car.commands):
                    continue 

                command = car.commands[car.step_count]
                car.step_count += 1

                if command == 'F':
                    self.move_car(car, step)
                elif command == 'R':
                    self.turn_car_right(car)
                elif command == 'L':
                    self.turn_car_left(car)

        return self.collisions

    def move_car(self, car, step):
        """Move the car forward if no collision or out-of-bound occurs."""
        direction = car.direction
        if direction == 'N':
            new_x, new_y = car.x, car.y + 1
        elif direction == 'E':
            new_x, new_y = car.x + 1, car.y
        elif direction == 'S':
            new_x, new_y = car.x, car.y - 1
        elif direction == 'W':
            new_x, new_y = car.x - 1, car.y

        # Ensure the car stays within bounds and check for collisions
        if not (0 <= new_x < self.field.width and 0 <= new_y < self.field.height):
            print(f"{car.name} cannot move out of bounds.")
            car.stopped = True
            return

        # Check for collisions with other cars
        for other_car in self.field.cars.values():
            if other_car == car:
                continue
            if (new_x, new_y) == (other_car.x, other_car.y):
                print(f"Collision detected: {car.name} collides with {other_car.name} at ({new_x},{new_y})")
                self.collisions.append((car.name, other_car.name, new_x, new_y, step+1))
                self.collisions.append((other_car.name, car.name, new_x, new_y, step+1))
                car.stopped = True
                other_car.stopped = True
                return

        # Move the car if no collision
        car.update_position(new_x, new_y)

    def turn_car_right(self, car):
        """Turn the car 90 degrees to the right."""
        current_index = DIRECTIONS.index(car.direction)
        car.direction = DIRECTIONS[(current_index + 1) % 4]

    def turn_car_left(self, car):
        """Turn the car 90 degrees to the left."""
        current_index = DIRECTIONS.index(car.direction)
        car.direction = DIRECTIONS[(current_index - 1) % 4]

class Simulation:
    def __init__(self):
        self.field = None
        self.simulation_engine = None

    def initialize_field(self, width, height):
        """Initialize the field dimensions and the simulation engine."""
        self.field = Field(width, height)
        self.simulation_engine = SimulationEngine(self.field)

    def add_car(self, car):
        """Add a car to the simulation field."""
        self.field.add_car(car)

    def run_simulation(self):
        """Run the car simulation."""
        self.simulation_engine.process_commands() 
        self.display_results() 
    
    def display_results(self):
        """Display the results after simulation."""
        print("\nYour current list of cars are:")
        for car in self.field.cars.values():
            print(f"- {car}")  

        if not self.simulation_engine.collisions:
            print("\nAfter simulation, the result is:")
            for car in self.field.cars.values():
                print(f"- {car.name}, ({car.x},{car.y}) {car.direction}")
        
        else:
            print("\nAfter simulation, the result is:")
            for collision in self.simulation_engine.collisions:
                car_name, other_car_name, x, y, step = collision
                print(f"- {car_name}, collides with {other_car_name} at ({x},{y}) at step {step}")


class SimulationCLI:
    def __init__(self):
        self.simulation = Simulation() 

    def get_field_dimensions(self):
        """Prompts the user for the field dimensions (width and height)."""
        while True:
            try:
                width, height = map(int, input("Please enter the width and height of the simulation field in 'x y' format: ").split())
                return width, height
            except ValueError:
                print("Invalid input. Please only enter integers separated by space (e.g., '5 5')")

    def get_car_details(self):
        """Prompts the user for car details including its name, initial position, and commands."""
        while True:
            name = input("Please enter the name of the car: ").strip()
            if not name:
                print("Car name cannot be empty.")
                continue

            position = input(f"Please enter initial position of car {name} in 'x y Direction' format (e.g., '1 2 N'): ").strip().split()
            if len(position) != 3:
                print("Invalid position format. Please enter 'x y Direction'.")
                continue

            try:
                x, y, direction = int(position[0]), int(position[1]), position[2].upper()
                if direction not in DIRECTIONS:
                    print("Invalid direction. Please use one of N, E, S, W.")
                    continue
                commands = input(f"Please enter the commands for car {name}: ").strip().upper()
                if any(c not in COMMANDS for c in commands):
                    print("Invalid commands. Please only use 'F', 'R', and 'L'.")
                    continue
                return name, x, y, direction, commands
            except ValueError:
                print("Invalid input. Please enter valid numbers for position.")

    def start_over(self):
        """Resets the simulation and allows the user to start over."""
        print("\nSimulation reset successfully. You can start over.")
        # Reset the simulation object
        self.simulation = Simulation() 
        width, height = self.get_field_dimensions() 
        self.simulation.initialize_field(width, height) 


    def run(self):
        """Main method that runs the simulation CLI loop."""
        while True:
            # Step 1: Get the dimensions of the field and initialize
            width, height = self.get_field_dimensions()

            self.simulation.initialize_field(width, height)

            while True:
                # Step 2: Menu for adding cars and running the simulation
                print("\nPlease choose from the following options:")
                print("[1] Add a car to field")
                print("[2] Run simulation")
                choice = input("Enter your choice (1-2): ").strip()

                if choice == '1':
                    name, x, y, direction, commands = self.get_car_details()
                    car = Car(name, x, y, direction, commands)
                    self.simulation.add_car(car) 
                elif choice == '2':
                    # Step 3: Run the simulation
                    self.simulation.run_simulation()

                    # Step 4: Ask the user to either start over or exit
                    while True:
                        print("\nPlease choose from the following options:")
                        print("[1] Start over")
                        print("[2] Exit")
                        choice_after_simulation = input("Enter your choice (1-2): ").strip()

                        if choice_after_simulation == '1':
                            self.start_over() 
                            break 
                        elif choice_after_simulation == '2':
                            print("Thank you for running the simulation. Goodbye!")
                            return  
                        else:
                            print("Invalid choice. Please select 1 or 2.") 

if __name__ == "__main__":
    cli = SimulationCLI()
    cli.run()
