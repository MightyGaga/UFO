from instantiation.controller.agent.agent import FilterAgent
from instantiation.controller.config.config import Config

configs = Config.get_instance().config_data


class FilterFlow:
    """
    The class to refine the plan steps and prefill the file.
    """

    def __init__(self, app_name: str) -> None:
        """
        Initialize the follow flow.
        :param app_name: The name of the operated app. Example: "Word"
        """

        self.app_name = app_name
        self.filter_agent = FilterAgent(
            "filter",
            app_name,
            is_visual=True,
            main_prompt=configs["FILTER_PROMPT"],
            example_prompt="",
            api_prompt=configs["API_PROMPT"],
        )
        self.execute_step = 0

    def get_filter_res(self, request: str) -> tuple[bool, str, str]:
        """
        Call the PlanRefine Agent to select files
        :param request: The request message
        :return: The results from the filter agent
        """

        prompt_message = self.filter_agent.message_constructor(request, self.app_name)
        try:
            response_string, cost = self.filter_agent.get_response(
                prompt_message, "filter", use_backup_engine=True, configs=configs
            )
            response_json = self.filter_agent.response_to_dict(response_string)
            judge = response_json["judge"]
            thought = response_json["thought"]
            type = response_json["type"]
            return judge, thought, type

        except Exception as e:
            self.status = "ERROR"
            print(f"Error: {e}")
            return None
