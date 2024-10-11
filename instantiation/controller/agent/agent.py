# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import Dict, List

from instantiation.controller.prompter.agent_prompter import (
    ActionPrefillPrompter, FilterPrompter)
from ufo.agents.agent.basic import BasicAgent


class FilterAgent(BasicAgent):
    """
    The Agent to evaluate the instantiated task is correct or not.
    """

    def __init__(
        self,
        name: str,
        process_name: str,
        is_visual: bool,
        main_prompt: str,
        example_prompt: str,
        api_prompt: str,
    ):
        """
        Initialize the FilterAgent.
        :param name: The name of the agent.
        :param process_name: The name of the process.
        :param is_visual: The flag indicating whether the agent is visual or not.
        :param main_prompt: The main prompt.
        :param example_prompt: The example prompt.
        :param api_prompt: The API prompt.
        """

        self._step = 0
        self._complete = False
        self._name = name
        self._status = None
        self.prompter: FilterPrompter = self.get_prompter(
            is_visual, main_prompt, example_prompt, api_prompt
        )
        self._process_name = process_name

    def get_prompter(self, is_visual, main_prompt, example_prompt, api_prompt) -> str:
        """
        Get the prompt for the agent.
        :return: The prompt.
        """

        return FilterPrompter(is_visual, main_prompt, example_prompt, api_prompt)

    def message_constructor(self, request: str, app: str) -> List[str]:
        """
        Construct the prompt message for the FilterAgent.
        :param request: The request sentence.
        :param app: The name of the operated app.
        :return: The prompt message.
        """

        filter_agent_prompt_system_message = self.prompter.system_prompt_construction(
            app=app
        )
        filter_agent_prompt_user_message = self.prompter.user_content_construction(
            request
        )
        filter_agent_prompt_message = self.prompter.prompt_construction(
            filter_agent_prompt_system_message, filter_agent_prompt_user_message
        )

        return filter_agent_prompt_message

    def process_comfirmation(self) -> None:
        """
        Confirm the process.
        """
        pass


class ActionPrefillAgent(BasicAgent):
    """
    The Agent for task instantialization and action sequence generation.
    """

    def __init__(
        self,
        name: str,
        process_name: str,
        is_visual: bool,
        main_prompt: str,
        example_prompt: str,
        api_prompt: str,
    ):
        """
        Initialize the ActionPrefillAgent.
        :param name: The name of the agent.
        :param process_name: The name of the process.
        :param is_visual: The flag indicating whether the agent is visual or not.
        :param main_prompt: The main prompt.
        :param example_prompt: The example prompt.
        :param api_prompt: The API prompt.
        """

        self._step = 0
        self._complete = False
        self._name = name
        self._status = None
        self.prompter: ActionPrefillPrompter = self.get_prompter(
            is_visual, main_prompt, example_prompt, api_prompt
        )
        self._process_name = process_name

    def get_prompter(self, is_visual, main_prompt, example_prompt, api_prompt) -> str:
        """
        Get the prompt for the agent.
        :param is_visual: The flag indicating whether the agent is visual or not.
        :param main_prompt: The main prompt.
        :param example_prompt: The example prompt.
        :param api_prompt: The API prompt.
        :return: The prompt.
        """

        return ActionPrefillPrompter(is_visual, main_prompt, example_prompt, api_prompt)

    def message_constructor(
        self,
        dynamic_examples: str,
        given_task: str,
        reference_steps: List[str],
        doc_control_state: Dict[str, str],
        log_path: str,
    ) -> List[str]:
        """
        Construct the prompt message for the ActionPrefillAgent.
        :param dynamic_examples: The dynamic examples retrieved from the self-demonstration and human demonstration.
        :param given_task: The given task.
        :param reference_steps: The reference steps.
        :param doc_control_state: The document control state.
        :param log_path: The path of the log.
        :return: The prompt message.
        """

        action_prefill_agent_prompt_system_message = (
            self.prompter.system_prompt_construction(dynamic_examples)
        )
        action_prefill_agent_prompt_user_message = (
            self.prompter.user_content_construction(
                given_task, reference_steps, doc_control_state, log_path
            )
        )
        appagent_prompt_message = self.prompter.prompt_construction(
            action_prefill_agent_prompt_system_message,
            action_prefill_agent_prompt_user_message,
        )

        return appagent_prompt_message

    def process_comfirmation(self) -> None:
        """
        Confirm the process.
        """
        pass
