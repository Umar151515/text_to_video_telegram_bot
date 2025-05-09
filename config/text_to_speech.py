from typing import Any
from .paths import text_to_speech_config_path
from .generation_config import GenerationConfig


class TextToSpeech(GenerationConfig):
    config_path = text_to_speech_config_path

    @property
    def models(self) -> list[str]:
        return self.get_models()
    
    @property
    def selected_model(self) -> str:
        return self.get_selected_model()
    
    def has_models(self, tool:str|None = None) -> bool:
        if not tool:
            tool = self.selected_tool
        return "models" in self.get_tool_config(tool)
    
    def _validate_has_models(self, tool:str|None = None):
        if not self.has_models(tool):
            raise ValueError(f"The tool '{tool or 'current'}' contains no models.")

    def _model_check(self, tool:str|None = None, model:str|None = None):
        self._validate_has_models(tool)
        super()._model_check(tool, model)

    def get_models(self, tool:str|None = None) -> list[str]:
        self._validate_has_models(tool)
        return super().get_models(tool)

    def add_model(self, model: str, tool:str|None = None):
        self._validate_has_models(tool)
        super().add_model(model, tool)

    def delete_model(self, model: str, tool:str|None = None):
        self._validate_has_models(tool)
        super().delete_model(model, tool)
        
    def get_selected_model(self, tool:str|None = None) -> str:
        self._validate_has_models(tool)
        return super().get_selected_model(tool)
        
    def set_selected_model(self, model: str, tool:str|None = None):
        self._validate_has_models(tool)
        super().set_selected_model(model, tool)

    @property
    def speakers(self) -> list[str]:
        return self.get_speakers()
    
    @property
    def selected_speaker(self) -> str:
        return self.get_selected_speaker()

    def get_speakers(self, tool:str|None = None, model:str|None = None) -> dict[str, str]:
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)

        if self.has_models(tool):
            if not model:
                model = self.get_selected_model(tool)
            self._model_check(tool, model)
            return self.config["tools_config"][tool]["models_config"][model]["speakers"]
        else:
            return self.config["tools_config"][tool]["speakers"]
        
    def get_description_speaker(self, speaker: str, tool:str|None = None, model:str|None = None) -> tuple[str, str]:
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)

        if self.has_models(tool):
            if not model:
                model = self.get_selected_model(tool)
            self._model_check(tool, model)
            return self.config["tools_config"][tool]["models_config"][model]["speakers"][speaker]
        else:
            return self.config["tools_config"][tool]["speakers"][speaker]
    
    def set_speaker(self, speaker: str, description: str, tool:str|None = None, model:str|None = None):
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)

        if self.has_models(tool):
            if not model:
                model = self.get_selected_model(tool)
            self._model_check(tool, model)
            speakers = self.config["tools_config"][tool]["models_config"][model]["speakers"]
        else:
            speakers = self.config["tools_config"][tool]["speakers"]

        speakers[speaker] = description
        self.save()

    def delete_speaker(self, speaker: str, tool:str|None = None, model:str|None = None):
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)

        if self.has_models(tool):
            if not model:
                model = self.get_selected_model(tool)
            self._model_check(tool, model)
            speakers = self.config["tools_config"][tool]["models_config"][model]["speakers"]
        else:
            speakers = self.config["tools_config"][tool]["speakers"]

        if speaker in speakers:
            speakers.pop(speaker)
            self.save()
        
    def get_selected_speaker(self, tool:str|None = None, model:str|None = None) -> str:
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)
        
        if self.has_models(tool):
            if not model:
                model = self.get_selected_model(tool)
            self._model_check(tool, model)
            return self.config["tools_config"][tool]["models_config"][model]["selected_speaker"]
        else:
            return self.config["tools_config"][tool]["selected_speaker"]
        
    def set_selected_speaker(self, speaker: str, tool:str|None = None, model:str|None = None):
        if not tool:
            tool = self.selected_tool
        self._tool_check(tool)

        if self.has_models(tool):
            if not model:
                model = self.get_selected_model(tool)
            self._model_check(tool, model)
            self.config["tools_config"][tool]["models_config"][model]["selected_speaker"] = speaker
        else:
            self.config["tools_config"][tool]["selected_speaker"] = speaker

        self.save()

    def get_model_config(self, tool:str|None = None, model:str|None = None) -> dict[str, Any]:
        if not tool:
            tool = self.selected_tool
        if not model:
            model = self.get_selected_model(tool)
        self._model_check(tool, model)

        return self.config["tools_config"][tool]["models_config"][model]