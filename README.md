# Test Plan Generator

A Python-based project for generating comprehensive test plans using AutoGen agents. This tool facilitates the creation of detailed, structured test cases for various software systems, including functional, load, security, and integration tests.

## Features

- **Dynamic Test Plan Creation**: Generates test plans based on user-defined system requirements.
- **Agent Collaboration**: Utilizes multiple agents for specialized roles:
  - Manual QA Agent
  - API QA Agent
  - Database QA Agent
  - System QA Agent
  - Test Plan Orchestrator
- **Customizable Outputs**: Saves the generated test plans and test cases to easily accessible files for further use.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Virtualenv (optional, but recommended)

### Steps
1. Clone this repository:
    ```bash
    git clone https://github.com/your-repo/test-plan-generator.git
    cd test-plan-generator
    ```
2. Set up a virtual environment (optional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Unix/Mac
    venv\Scripts\activate   # For Windows
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Define the Initial Prompt**
   Modify the `initial_prompt` in `main.py` to include the system context and test plan requirements. For example:
   ```python
   initial_prompt = """
   Create a comprehensive test plan for a financial technology system designed for high-frequency trading...
   """
   ```

2. **Run the Script**
   Execute the `main.py` file to generate a test plan:
   ```bash
   python main.py
   ```

3. **View the Output**
   The generated test plan is saved in the `test_plan_output` folder:
   ```
   test_plan_output/test_plan.txt
   ```

## File Structure

```
project-root
├── main.py              # Entry point of the application
├── config.py            # Configuration file for agent settings
├── agents.py            # Defines various agents involved in the test plan generation
├── testplan_generator.py # Core logic for generating test plans
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Example Output

### Test Case Format
Each test case in the generated test plan follows this structure:
```
Test Case 1: High-Frequency Trading Scenario Validation
--------------------------------------------------
Objective: Validate the trading system's behavior under high-frequency scenarios.
Preconditions: System initialized with mock trading data.
Steps:
- Step 1: Simulate 1,000,000 trades per second.
- Step 2: Monitor system response time.
- Step 3: Verify accurate trade execution.
Expected Results: All trades are executed within 1 millisecond.
Priority: High
Status: Ready for Execution
```

## Contributing
Contributions are welcome! If you'd like to add features or fix issues, please fork the repository and create a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact.

