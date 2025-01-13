"""Define the agents used in the test case generation system with improved context management"""
import autogen
from typing import Dict, List, Optional

class QAAgents:
    def __init__(self, agent_config: Dict, test_plan: Optional[List[Dict]] = None):
        """Initialize agents with test plan context"""
        self.agent_config = agent_config
        self.test_plan = test_plan

    def _format_test_plan_context(self) -> str:
        """Format the test plan into a readable context"""
        if not self.test_plan:
            return ""

        context_parts = ["Complete Test Plan:"]
        for test_case in self.test_plan:
            context_parts.extend([
                f"\nTest Case {test_case['id']}: {test_case['title']}",
                f"Objective: {test_case['objective']}",
                f"Preconditions: {test_case['preconditions']}",
                f"Steps: {', '.join(test_case['steps'])}",
                f"Expected Results: {test_case['expected_results']}",
            ])
        return "\n".join(context_parts)

    def create_agents(self, initial_prompt: str) -> Dict:
        """Create and return all agents needed for test case generation"""
        test_plan_context = self._format_test_plan_context()

        # Memory Keeper: Maintains testing continuity and context
        memory_keeper = autogen.AssistantAgent(
            name="memory_keeper",
            system_message=f"""You are the keeper of the testing process continuity and context.
            Your responsibilities:
            1. Track and summarize each agent's contributions
            2. Monitor dependencies between agents
            3. Maintain consistency across test cases, results, and automation scripts
            4. Flag any conflicts or gaps in requirements or testing coverage

            Testing Overview:
            {test_plan_context}

            Format your responses as follows:
            - Start updates with 'MEMORY UPDATE:'
            - List agent contributions with 'CONTRIBUTION:'
            - Highlight dependencies with 'DEPENDENCY:'
            - Flag conflicts or issues with 'ISSUE ALERT:'""",
            llm_config=self.agent_config,
        )

        manual_qa_agent = autogen.AssistantAgent(
            name="manual_qa_agent",
            system_message=f"""You are a manual QA expert focused on creating test cases based on user requirements.

            Your sole responsibility is:
            1. Analyze requirements provided by SpecFinder
            2. Create detailed, reproducible test cases for functional testing
            3. Ensure the test cases cover edge cases and are user-focused

            Format your output EXACTLY as:
            TEST_CASES:
            - Title: [Test Case Title]
            - Steps: [List step-by-step instructions for execution]
            - Expected Results: [Describe the expected outcome for each step]
            
            Always provide detailed, actionable test cases.""",
            llm_config=self.agent_config,
        )

        api_qa_agent = autogen.AssistantAgent(
            name="api_qa_agent",
            system_message=f"""You are an API QA expert responsible for validating API functionalities.

            Your sole responsibility is:
            1. Create API test cases for request/response validation
            2. Verify API performance, security, and error handling
            3. Identify API dependencies and potential integration issues

            Format your output EXACTLY as:
            API_TEST_CASES:
            - Endpoint: [API Endpoint]
            - Test Type: [Functional/Performance/Security]
            - Steps: [List request details and execution steps]
            - Expected Results: [Describe the expected response for each case]
            
            Always provide comprehensive test scenarios.""",
            llm_config=self.agent_config,
        )

        database_qa_agent = autogen.AssistantAgent(
            name="database_qa_agent",
            system_message=f"""You are a database QA specialist ensuring data integrity and correctness.

            Your sole responsibility is:
            1. Validate database schemas, queries, and stored procedures
            2. Test data migrations and edge-case handling
            3. Ensure backend data consistency with test inputs

            Format your output EXACTLY as:
            DB_TEST_CASES:
            - Scenario: [Test Scenario Description]
            - Steps: [List SQL queries and validation steps]
            - Expected Results: [Describe expected database state]
            
            Always ensure thorough validation.""",
            llm_config=self.agent_config,
        )

        system_qa_agent = autogen.AssistantAgent(
            name="system_qa_agent",
            system_message=f"""You are a system QA expert responsible for end-to-end validation.

            Your sole responsibility is:
            1. Design system integration test cases
            2. Validate workflows across multiple systems
            3. Test system performance under various conditions

            Format your output EXACTLY as:
            SYSTEM_TEST_CASES:
            - Title: [Test Case Title]
            - Workflow: [Describe system workflow]
            - Validation Steps: [List validation steps for each stage]
            - Expected Results: [Describe expected outcomes]

            Always include cross-system dependencies.""",
            llm_config=self.agent_config,
        )

        test_case_orchestrator = autogen.AssistantAgent(
            name="test_case_orchestrator",
            system_message=f"""You are a test case orchestrator coordinating inputs from other agents.

            Your sole responsibility is:
            1. Aggregate test cases from all agents
            2. Ensure no requirement is missed
            3. Maintain a clear traceability matrix

            Format your output EXACTLY as:
            TEST_CASE_SUMMARY:
            - Requirement ID: [Requirement Identifier]
            - Test Cases: [Summarize test cases mapped to this requirement]
            - Gaps: [List any gaps or uncovered areas]

            Always ensure completeness and clarity.""",
            llm_config=self.agent_config,
        )

        test_case_editor = autogen.AssistantAgent(
            name="test_case_editor",
            system_message=f"""You are a test case editor responsible for ensuring the quality, accuracy, and completeness of test cases.

            Your focus:
            1. Validate that test cases align with requirements and testing standards
            2. Check for clarity, reproducibility, and proper formatting
            3. Verify that all edge cases are covered
            4. Ensure traceability to requirements or specifications
            5. Return improved and finalized test cases

            Format your responses as follows:
            - Start critiques with 'FEEDBACK:'
            - Provide specific improvement suggestions with 'SUGGEST:'
            - Return finalized test cases with 'EDITED_TEST_CASES:' in the same structure as provided
            
            Always provide actionable feedback and detailed improvements.
            """,
            llm_config=self.agent_config,
        )

        test_plan_creator = autogen.AssistantAgent(
            name="test_plan_creator",
            system_message=f"""Generate a detailed test plan.

            YOU MUST USE EXACTLY THIS FORMAT FOR EACH TEST CASE - NO DEVIATIONS:

            Test Case 000001 : [Test Case Title]
            Objective: [Purpose of the test case]
            Preconditions: [List of preconditions required before executing the test]
            Test Steps:
            1. [Step 1]
            2. [Step 2]
            3. [Step 3]
            Expected Results: [Expected outcome for this test case]
            Priority: [Low/Medium/High]
            Status: [e.g., Draft, Ready for Execution, Completed]

            [REPEAT THIS EXACT FORMAT FOR ALL TEST CASES]

            Requirements:
            1. EVERY field must be present for EVERY test case.
            2. EVERY test case must have AT LEAST 3 specific Test Steps.
            3. The Expected Results must be precise and measurable.
            4. The format must match EXACTLY - including all headings and bullet points.

            Initial Context:
            {initial_prompt}

            START WITH 'TEST PLAN:' AND END WITH 'END OF TEST PLAN'
            """,
            llm_config=self.agent_config,
        )

        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="TERMINATE",
            code_execution_config={
                "work_dir": "testcase_output",
                "use_docker": False
            }
        )

        return {
            "api_qa_agent": api_qa_agent,
            "manual_qa_agent": manual_qa_agent,
            "memory_keeper": memory_keeper,
            "test_case_orchestrator": test_case_orchestrator,
            "test_case_editor": test_case_editor,
            "user_proxy": user_proxy,
            "test_plan_creator": test_plan_creator
        }
