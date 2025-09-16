import unittest
from unittest.mock import patch
from src.crews.interview_prep_crew import interview_prep_crew

class TestFullWorkflowMock(unittest.TestCase):
    @patch('crewai.Crew.kickoff')
    def test_full_workflow_with_mock_data(self, mock_kickoff):
        # Define the mock return value for the kickoff method
        mock_kickoff.return_value = "Mocked interview preparation report"

        # Define the inputs for the crew
        inputs = {
            'company_name': 'Mock Company',
            'interviewer_names': 'Mock Interviewer 1, Mock Interviewer 2',
            'job_role': 'Mock Role'
        }

        # Run the crew with the mocked kickoff method
        result = interview_prep_crew.kickoff(inputs=inputs)

        # Assert that the kickoff method was called with the correct inputs
        mock_kickoff.assert_called_once_with(inputs=inputs)

        # Assert that the result is the mocked return value
        self.assertEqual(result, "Mocked interview preparation report")

        print("\nSuccessfully tested the full workflow with mock data.")
        print(f"Result: {result}")

if __name__ == '__main__':
    unittest.main()
