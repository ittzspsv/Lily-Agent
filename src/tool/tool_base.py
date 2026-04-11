import inspect
from pydantic import BaseModel, create_model, ValidationError
from typing import Optional, Type, Callable, Dict, Any, Tuple ,get_type_hints, cast
from .tool_exceptions import ToolRuntimeError, ToolValidationError


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
    def __init__(self, func: Callable , name: Optional[str] ,description: Optional[str], parameters: Optional[Type[BaseModel]]) -> None:
        
        self.func: Callable = func

        if description is not None:
            self.description = description
        elif func.__doc__:
            self.description = func.__doc__
        else:
            raise ValueError(f"Tool {func.__name__} must have a description.  Please define a description")

        if name is None:
            self.name = func.__name__
        else:
            self.name = name

        if parameters is None:
            self.parameters: Type[BaseModel] = self._model_builder(func)
        else:
            self.parameters: Type[BaseModel] = parameters

    def _model_builder(self, func: Callable) -> type[BaseModel]:
        signature: inspect.Signature = inspect.signature(func)
        typings: Dict[str, Any] = get_type_hints(func)

        fields: Dict[str, Tuple[Type[Any], Any]] = {}

        for name, param in signature.parameters.items():
            if name == "self":
                continue

            if param.annotation is inspect._empty:
                raise TypeError(
                    f"Parameter '{name}' in {func.__name__} must have type annotation"
                )

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
        schema = dict(schema)
        schema.pop("title", None)

        for properities in schema.get("properties", {}).values():
            properities.pop("title", None)

        return schema

    def __call__(self, **kwargs):
        try:
            validate = self.parameters(**kwargs)
        except ValidationError as e:
            raise ToolValidationError(self.name, e.errors())
        
        try:
            data = validate.model_dump()
            return self.func(**data)
        except (ValueError, TypeError, RuntimeError) as e:
            raise ToolRuntimeError(self.name, str(e))
    
    def __repr__(self) -> str:
        return f'Tool(name="{self.name}", params={list(self.parameters.model_fields.keys())})'
    
    def __str__(self) -> str:
        return self.name

    @property
    def input_schema(self) -> Dict[str, Any]:
        return self._schema_process(self.parameters.model_json_schema())
        