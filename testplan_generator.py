"""Generate detailed test plans using AutoGen agents with improved error handling and file saving"""
import autogen
from typing import Dict, List
import re
import os

class TestPlanGenerator:
    def __init__(self, agents: Dict[str, autogen.ConversableAgent], agent_config: Dict, output_folder: str = "output"):
        self.agents = agents
        self.agent_config = agent_config
        self.output_folder = output_folder

        # Ensure the output folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def generate_test_plan(self, initial_prompt: str, num_test_cases: int = 25, output_file_name: str = "test_plan.txt") -> Dict:
        """Generate a comprehensive test plan based on the initial prompt and save it to a file"""
        print("\nGenerating test plan...")

        groupchat = autogen.GroupChat(
            agents=[
                self.agents["test_plan_creator"],
                self.agents["user_proxy"],
                self.agents["manual_qa_agent"],
                self.agents["api_qa_agent"]
                ],
            messages=[],
            max_round=6,
            speaker_selection_method="round_robin"
        )

        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.agent_config)

        test_plan_prompt = f"""Create a detailed test plan with the following requirements:
        
        Context: {initial_prompt}

        Test Plan Requirements:
        1. Include a clear **Objective** for the test plan.
        2. Define the **Scope**, including which systems, components, or APIs will be tested.
        3. Specify the **Testing Strategy**, such as manual testing, automated testing, API testing, database testing, and system testing.
        4. Highlight the **Test Environment** requirements and setup.
        5. Provide a **Schedule** and testing phases (e.g., Unit Testing, Integration Testing, End-to-End Testing).
        6. Include a list of **Test Cases**:
            - Each test case must follow this format:
              Test Case [Number]: [Test Case Title]
              Objective: [Purpose of the test case]
              Preconditions: [Preconditions required before executing the test]
              Test Steps:
                1. [Step 1]
                2. [Step 2]
                3. [Step 3]
              Expected Results: [Expected outcome for this test case]
              Priority: [Low/Medium/High]
              Status: [Draft/Ready for Execution/Completed]
        7. End with **Risk Assessment**: Highlight potential risks and mitigation strategies.

        Generate {num_test_cases} detailed test cases and ensure no fields are left incomplete.

        START WITH 'TEST PLAN:' AND END WITH 'END OF TEST PLAN'"""

        try:
            # Initiate the chat
            self.agents["user_proxy"].initiate_chat(
                manager,
                message=test_plan_prompt
            )

            # Extract the test plan from the chat messages
            test_plan = self._process_test_plan_results(groupchat.messages)

            # Save the test plan to a file
            self._save_test_plan_to_file(test_plan, output_file_name)

            return test_plan
        except Exception as e:
            print(f"Error generating test plan: {str(e)}")
            # Try to salvage any test plan content
            test_plan = self._emergency_test_plan_processing(groupchat.messages)

            # Save the salvaged plan to a file
            self._save_test_plan_to_file(test_plan, output_file_name)

            return test_plan

    def _process_test_plan_results(self, messages: List[Dict]) -> Dict:
        """Process the test plan results from the chat messages"""
        print("Processing test plan results...")
        return self._extract_test_plan_content(messages)

    def _extract_test_plan_content(self, messages: List[Dict]) -> Dict:
        """Extract the test plan content from messages with error handling"""
        print("Extracting test plan content...")

        # Look for content between "TEST PLAN:" and "END OF TEST PLAN"
        for msg in reversed(messages):
            content = msg.get("content", "")
            if "TEST PLAN:" in content:
                start_idx = content.find("TEST PLAN:")
                end_idx = content.find("END OF TEST PLAN")

                if start_idx != -1 and end_idx != -1:
                    return {"test_plan": content[start_idx:end_idx].strip()}

        print("No structured test plan found in the messages.")
        return {"test_plan": "No test plan could be extracted."}

    def _emergency_test_plan_processing(self, messages: List[Dict]) -> Dict:
        """Fallback processing when test plan extraction fails"""
        print("Attempting emergency test plan processing...")

        test_plan = {
            "objective": "To be determined",
            "scope": "To be determined",
            "testing_strategy": "To be determined",
            "test_environment": "To be determined",
            "schedule": "To be determined",
            "test_cases": [],
            "risk_assessment": "To be determined"
        }

        current_test_case = None

        # Extract test cases
        for msg in messages:
            content = msg.get("content", "")
            lines = content.split("\n")

            for line in lines:
                # Look for test case markers
                test_case_match = re.search(r"Test Case (\d+)", line)
                if test_case_match and "Objective:" in content:
                    if current_test_case:
                        test_plan["test_cases"].append(current_test_case)

                    current_test_case = {
                        "test_case_number": int(test_case_match.group(1)),
                        "title": line.split(":")[-1].strip() if ":" in line else f"Test Case {test_case_match.group(1)}",
                        "objective": "",
                        "preconditions": "",
                        "steps": [],
                        "expected_results": "",
                        "priority": "Medium",
                        "status": "Draft"
                    }

                # Extract fields for the current test case
                if current_test_case:
                    if line.strip().startswith("Objective:"):
                        current_test_case["objective"] = line.split("Objective:")[-1].strip()
                    elif line.strip().startswith("Preconditions:"):
                        current_test_case["preconditions"] = line.split("Preconditions:")[-1].strip()
                    elif line.strip().startswith("Expected Results:"):
                        current_test_case["expected_results"] = line.split("Expected Results:")[-1].strip()
                    elif line.strip().startswith("Priority:"):
                        current_test_case["priority"] = line.split("Priority:")[-1].strip()
                    elif line.strip().startswith("Status:"):
                        current_test_case["status"] = line.split("Status:")[-1].strip()
                    elif line.strip().startswith("-") or re.match(r"\d+\.", line.strip()):
                        current_test_case["steps"].append(line.strip())

        # Append the last test case
        if current_test_case:
            test_plan["test_cases"].append(current_test_case)

        return test_plan

    def _save_test_plan_to_file(self, test_plan: Dict, file_name: str) -> None:
        """Save the generated test plan to a file in the specified folder"""
        output_path = os.path.join(self.output_folder, file_name)
        print(f"Saving test plan to {output_path}...")

        with open(output_path, "w", encoding="utf-8") as file:
            if isinstance(test_plan, dict) and "test_plan" in test_plan:
                file.write(test_plan["test_plan"])
            else:
                file.write("TEST PLAN:\n")
                file.write(str(test_plan))
                file.write("\nEND OF TEST PLAN")

        print(f"Test plan saved successfully at {output_path}!")
