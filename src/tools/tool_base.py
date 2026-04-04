import warnings
import inspect
from pydantic import BaseModel, create_model
from typing import Optional, Type, Callable, Dict, Any, Tuple ,get_type_hints, cast


class Tool():
    """
    Base Class for defining a tool.
    - This Class wraps a callable function and converts that into a structured tool with JSON Schema
    - This can be reused for AI

    ### Constructor
    - **func**: `Callable`  (passed manually or via a decorator)
    - **description**: `Optional[str]` ((description of what the tool does and when it should be used)
    - **parameters**: `Type[BaseModel]` (pydantic class model for input type definitions)
    """
    def __init__(self, func: Callable , description: Optional[str], parameters: Optional[Type[BaseModel]], strict: bool=True) -> None:
        
        self.func: Callable = func

        if description is None:
            warnings.warn(f"Tool {func.__name__} has no description. Please define a description", stacklevel=2)

        if parameters is None:
            self.parameters: Type[BaseModel] = self._model_builder(func)
        else:
            self.parameters: Type[BaseModel] = parameters

        self.schema = {
            "type" : "function",
            "name" : func.__name__,
            "description" : description,
            "parameters" : self._schema_process(self.parameters.model_json_schema()),
            "strict": strict
        }

    def _model_builder(self, func: Callable) -> type[BaseModel]:
        signature: inspect.Signature = inspect.signature(func)
        typings: Dict[str, Any] = get_type_hints(func)

        fields: Dict[str, Tuple[Type[Any], Any]] = {}

        for name, param in signature.parameters.items():
            if name == "self":
                continue

            if param.annotation is inspect._empty:
                warnings.warn(f"parameter {name} has no type annotation in {func.__name__} skipping.....")
                continue

            param_type = typings.get(name, param.annotation)

            if param.default is inspect.Parameter.empty:
                fields[name] = (param_type, ...)
            else:
                fields[name] = (param_type, param.default)

        return create_model(
            f"parameters",
            **cast(Any, fields)
        )

    def _schema_process(self, schema: dict) -> dict:
        schema.pop("title", None)

        for properities in schema.get("properties", {}).values():
            properities.pop("title", None)

        return schema

    def __call__(self, *args, **kwargs):
      return self.func(*args, **kwargs)
        