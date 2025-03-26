import pytest
from simulation import Car, Field, SimulationEngine, Simulation

@pytest.fixture
def sample_field():
    return Field(width=10, height=10)

def test_add_car_to_field(sample_field):
    car = Car("CarA", 1, 2, 'N', "FFRFFFFRRL")
    sample_field.add_car(car)
    assert "CarA" in sample_field.cars
    assert sample_field.cars["CarA"].x == 1
    assert sample_field.cars["CarA"].y == 2
    assert sample_field.cars["CarA"].direction == 'N'

def test_car_movement_no_collision(sample_field):
    car = Car("CarA", 1, 2, 'N', "FFRFF")
    sample_field.add_car(car)
    engine = SimulationEngine(sample_field)
    engine.process_commands()

    assert car.x == 3
    assert car.y == 4
    assert car.direction == 'E'
    assert not engine.collisions

def test_car_boundary_stop(sample_field):
    car = Car("CarA", 0, 0, 'S', "F") 
    sample_field.add_car(car)
    engine = SimulationEngine(sample_field)
    engine.process_commands()

    assert car.x == 0
    assert car.y == 0
    assert car.stopped

def test_collision_detection(sample_field):
    car_a = Car("CarA", 1, 2, 'N', "FFRFFFFRRL")
    car_b = Car("CarB", 7, 8, 'W', "FFLFFFFFFF")
    sample_field.add_car(car_a)
    sample_field.add_car(car_b)
    engine = SimulationEngine(sample_field)
    collisions = engine.process_commands()

    assert any(col for col in collisions if col[0] == 'CarA' and col[1] == 'CarB' and col[2:] == (5, 4, 7)) 
    assert car_a.stopped
    assert car_b.stopped

def test_simulation_display_result(capsys):
    sim = Simulation()
    sim.initialize_field(10, 10)
    car = Car("CarA", 1, 2, 'N', "FFRFFFFRRL")
    sim.add_car(car)
    sim.run_simulation()

    captured = capsys.readouterr()
    assert "CarA, (5,4) S" in captured.out


def test_add_car_duplicate_name_handled(sample_field):
    car_a = Car("CarA", 1, 2, 'N', "FFRFFFFRRL")
    car_duplicate = Car("CarA", 3, 3, 'E', "FFLFF")

    sample_field.add_car(car_a)
    
    with pytest.raises(ValueError, match="Car with name 'CarA' already exists"):
        sample_field.add_car(car_duplicate)

  