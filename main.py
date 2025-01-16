from config import get_config
from agents import QAAgents
from testplan_generator import TestPlanGenerator

def main():
    # Get configuration
    agent_config = get_config()

    # Initial prompt for the test plan
    initial_prompt = """
    Create a comprehensive test plan for a financial technology system designed for high-frequency trading. The system includes:
    - A stock prediction algorithm for market trends
    - Real-time trade execution
    - A web-based dashboard for analytics and reporting

    Key aspects to test:
    1. Functional tests for the prediction algorithm's accuracy and edge cases.
    2. Load tests to simulate high-frequency trading scenarios.
    3. Security tests to prevent data breaches and unauthorized access.
    4. UI/UX tests to ensure usability and accessibility of the dashboard.
    5. Integration tests for seamless operation between the prediction engine, trade execution system, and dashboard.

    Constraints:
    - The system must process at least 1,000,000 trades per second.
    - Predictions must have an accuracy rate above 95%.
    - Downtime must be under 2 minutes per year.

    Expected Deliverables:
    - Test cases grouped by functional area.
    - Detailed steps, preconditions, and expected results for each test case.
    - Priority and severity levels for each test case.
    - A summary of test coverage.

    Ensure that the test cases cover edge cases, error handling, and scalability scenarios. Each test case should follow this format:
    - Test Case Number
    - Title
    - Objective
    - Preconditions
    - Test Steps
    - Expected Results
    - Priority
    - Status
    """

    num_test_cases = 10
    # Create agents
    test_plan_agents = QAAgents(agent_config)
    agents = test_plan_agents.create_agents(initial_prompt)
    
    # Generate the test plan
    test_plan_gen = TestPlanGenerator(agents, agent_config)
    print("Generating test plan...")
    test_plan = test_plan_gen.generate_test_plan(initial_prompt)
    
    
    # Print the generated test cases
    print("\nGenerated Test Plan:")
    for test_case in test_plan:
        print(f"\nTest Case {test_case['test_case_number']}: {test_case['title']}")
        print("-" * 50)
        print(f"Objective: {test_case['objective']}")
        print(f"Preconditions: {test_case['preconditions']}")
        print("Steps:")
        for step in test_case['steps']:
            print(f"- {step}")
        print(f"Expected Results: {test_case['expected_results']}")
        print(f"Priority: {test_case['priority']}")
        print(f"Status: {test_case['status']}")
    
    # Save the test plan for reference
    print("\nSaving test plan to file...")
    with open("test_plan_output/test_plan.txt", "w") as f:
        for test_case in test_plan:
            f.write(f"\nTest Case {test_case['test_case_number']}: {test_case['title']}\n")
            f.write("-" * 50 + "\n")
            f.write(f"Objective: {test_case['objective']}\n")
            f.write(f"Preconditions: {test_case['preconditions']}\n")
            f.write("Steps:\n")
            for step in test_case['steps']:
                f.write(f"- {step}\n")
            f.write(f"Expected Results: {test_case['expected_results']}\n")
            f.write(f"Priority: {test_case['priority']}\n")
            f.write(f"Status: {test_case['status']}\n\n")
    
    # Generate the test case documentation
    print("\nGenerating test case documentation...")
    # if test_plan:
    #     # test_plan_gen_with_context.generate_test_case_documentation(test_plan)
    # else:
    #     print("Error: No test plan was generated.")

if __name__ == "__main__":
    main()
