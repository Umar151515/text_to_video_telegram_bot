import json, os
from typing import Any


class GenerationConfig:
    _instance = {}
    config_path: str

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(GenerationConfig, cls).__new__(cls)
        return cls._instance[cls]
    
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config: dict = None
            self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as config_file:
            self.config = json.load(config_file)

    def _tool_check(self, tool:str|None = None):
        if not tool:
            tool = self.selected_tool

        if tool not in self.tools:
            raise ValueError(f"Tool '{tool}' is not in available tools")
        
    def _model_check(self, tool:str|None = None, model:str|None = None):
        if not tool:
            tool = self.selected_tool
        if not model:
            model = self.get_selected_model(tool)
        self._tool_check(tool)
        
        if model not in self.config["tools_config"][tool]["models"]:
            raise ValueError(f"model '{model}' is not in models for '{tool}'")

    @property
    def tools(self) -> list[str]:
        return self.config.get("tools")
    
    @property
    def selected_tool(self) -> str:
        return self.config.get("selected_tool")
    
    @selected_tool.setter
    def selected_tool(self, tool: str):
        self.config["selected_tool"] = tool
        self._tool_check(tool)
        self.save()

    @property
    def models(self) -> list[str]:
        return self.get_models()
    
    @property
    def selected_model(self) -> str:
        return self.get_selected_model()

    @property
    def tool_config(self) -> dict[str, Any]:
        return self.get_tool_config()

    def get_models(self, tool:str|None = None) -> list[str]:
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        return self.config["tools_config"][tool]["models"]
    
    def add_model(self, model: str, tool:str|None = None):
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        models = self.config["tools_config"][tool]["models"]
        if model not in models:
            models.append(model)
            self.save()

    def delete_model(self, model: str, tool:str|None = None):
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        models = self.config["tools_config"][tool]["models"]
        if model in models:
            models.remove(model)
            self.save()
        
    def get_selected_model(self, tool:str|None = None) -> str:
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        return self.config["tools_config"][tool]["selected_model"]
        
    def set_selected_model(self, model: str, tool:str|None = None):
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        self.config["tools_config"][tool]["selected_model"] = model
        
        self.save()

    def get_tool_config(self, tool:str|None = None) -> dict[str, Any]:
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        return self.config["tools_config"][tool]
    
    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as config_file:
            json.dump(self.config, config_file, ensure_ascii=False, indent=4)