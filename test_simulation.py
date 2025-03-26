import unittest
from unittest.mock import patch
from io import StringIO
from simulation import add_car, add_commands, run_simulation, reset_simulation

class TestCarSimulation(unittest.TestCase):
    
    @patch('builtins.input', side_effect=[
        'CarA',            # car name
        '1 2 N'            # position input
    ])
    def test_add_car_success(self, mock_input):
        dic = {}
        name, x, y, direction = add_car(dic)
        self.assertEqual(name, 'CarA')
        self.assertEqual(x, '1')
        self.assertEqual(y, '2')
        self.assertEqual(direction, 'N')
    
    @patch('builtins.input', side_effect=[
        'CarA',            # Duplicate car name
        'CarB',            # New car name
        '3 3 E'            # position input
    ])
    def test_add_car_duplicate_name_handled(self, mock_input):
        dic = {'CarA': ['1', '2', 'N', 'F']}
        name, x, y, direction = add_car(dic)
        self.assertEqual(name, 'CarB')
        self.assertEqual(x, '3')
        self.assertEqual(y, '3')
        self.assertEqual(direction, 'E')

    @patch('builtins.input', side_effect=['CarA', '1 2 N','FFRFFFFRRL'])
    def test_add_commands_success(self, mock_input):
        dic = {}
        add_commands(dic)
        self.assertIn('CarA', dic)
        self.assertEqual(dic['CarA'], ['1', '2', 'N', 'FFRFFFFRRL'])

    def test_reset_simulation_clears_dict(self):
        dic = {'CarA': ['1', '2', 'N', 'FFRFFFFRRL']}
        width, height = reset_simulation(dic)
        self.assertEqual(dic, {})
        self.assertEqual((width, height), (0, 0))   

    def test_run_simulation_no_collision(self):
        dic = {'CarA': ['1', '2', 'N', 'FFRFFFFRRL']}
        width, height = 10, 10
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            run_simulation(dic, width, height)
            output = mock_stdout.getvalue()
            self.assertIn("- CarA, (5,4) S", output)

    def test_run_simulation_boundary_respect(self):
        dic = {'CarA': ['0', '0', 'S', 'F']}  
        width, height = 10, 10
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            run_simulation(dic, width, height)
            output = mock_stdout.getvalue()
            self.assertIn("- CarA, (0,0) S", output) 

    def test_run_simulation_with_collision(self):
        dic = {
            'CarA': ['1', '2', 'N', 'FFRFFFFRRL'], 
            'CarB': ['7', '8', 'W', 'FFLFFFFFFF']  
        }
        width, height = 10, 10
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            run_simulation(dic, width, height)
            output = mock_stdout.getvalue()

            # Check that both cars registered a collision at (5,4)
            self.assertIn("CarA, collides with CarB at (5,4) at step 7", output)
            self.assertIn("CarB, collides with CarA at (5,4) at step 7", output)            

if __name__ == '__main__':
    unittest.main()
