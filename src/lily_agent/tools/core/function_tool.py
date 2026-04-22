import inspect
from pydantic import BaseModel, create_model, ValidationError
from typing import Optional, Type, Callable, Dict, Any, Tuple ,get_type_hints, cast
from ..base.tool_exceptions import ToolRuntimeError, ToolValidationError
from ..base.tool_base import Tool


class FunctionTool(Tool):
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
        
        if func is None:
            raise ToolRuntimeError("No function has been passed onto the tool!")
        self.func: Callable = func
        self._async = inspect.iscoroutinefunction(func)

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

    def execute(self, **kwargs):
        '''
        ### Definition
        - Used to execute the function defined in this tool in a synchronous manner.
        - It validates incomming arguments using pydantic's validation
        ### Arguments
        - ****kwargs**: dict
          - Keyword arguments that should be passed to the tool's function
          - These keywords are validated with pydantic schema before execution.
        ### Raises
        - **ToolValidationError**
          - If argument validation fails
        - **ToolRuntimeError**
          - If any runtime errors are throwed during the execution.
        '''
        if self._async:
            raise ToolRuntimeError(
                self.name,
                "Cannot call async tool in sync context. consider using 'aexecute' instead"
            )
        
        try:
            if self.parameters is not None:
                validated = self.parameters(**kwargs)
                kwargs = validated.model_dump()

            return self.func(**kwargs)

        except ValidationError as e:
            raise ToolValidationError(self.name, e.errors())

        except Exception as e:
            raise ToolRuntimeError(self.name, str(e))
        
    async def aexecute(self, **kwargs):
        '''
        ### Definition
        - Used to execute the function defined in this tool in a asynchronous manner.
        - It validates incomming arguments using pydantic's validation
        ### Arguments
        - ****kwargs**: dict
          - Keyword arguments that should be passed to the tool's function
          - These keywords are validated with pydantic schema before execution.
        ### Raises
        - **ToolValidationError**
          - If argument validation fails
        - **ToolRuntimeError**
          - If any runtime errors are throwed during the execution.
        '''
        try:
            if self.parameters is not None:
                    validated = self.parameters(**kwargs)
                    kwargs = validated.model_dump()

            if self._async:
                return await self.func(**kwargs)
            else:
                return self.func(**kwargs)

        except ValidationError as e:
            raise ToolValidationError(self.name, e.errors())

        except Exception as e:
            raise ToolRuntimeError(self.name, str(e))

    
    def __repr__(self) -> str:
        return f'Tool(name="{self.name}", params={list(self.parameters.model_fields.keys())})'
    
    def __str__(self) -> str:
        return self.name

    @property
    def input_schema(self) -> Dict[str, Any]:
        if self.parameters is None:
            return {}
        return self._schema_process(self.parameters.model_json_schema())
        