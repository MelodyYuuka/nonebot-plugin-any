import inspect
from typing import Any, Optional, cast

from nonebot.adapters import Event
from nonebot.dependencies import CustomConfig, Param
from nonebot.dependencies.utils import check_field_type
from nonebot.matcher import Matcher
from nonebot.message import event_preprocessor
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.utils import generic_check_issubclass
from pydantic.fields import ModelField, Required
from typing_extensions import Self, override

from . import AnyEvent

ANYEVENT_TARGET = "_any_event"


class AnyEventParam(Param):
    """`AnyEvent` 参数"""
    def __init__(self, *args, validate: bool = False, **kwargs: Any) -> None:
        self.any_cls: type[AnyEvent] = kwargs["checker"].type_
        super().__init__(*args, validate=validate, **kwargs)

    def __repr__(self) -> str:
        return (
            "AnyEventParam("
            + (
                repr(cast(ModelField, checker).type_)
                if (checker := self.extra.get("checker"))
                else ""
            )
            + ")"
        )

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ) -> Optional[Self]:
        if generic_check_issubclass(param.annotation, AnyEvent):
            checker: Optional[ModelField] = None
            if param.annotation is not AnyEvent:
                checker = ModelField(
                    name=param.name,
                    type_=param.annotation,
                    class_validators=None,
                    model_config=CustomConfig,
                    default=None,
                    required=True,
                )
            return cls(Required, checker=checker)

    @override
    async def _solve(self, state: T_State, **kwargs: Any) -> Any:
        return state[ANYEVENT_TARGET]

    @override
    async def _check(self, event: "Event", state: T_State, **kwargs: Any) -> Any:
        if not (any_event := state[ANYEVENT_TARGET]):
            any_event = state[ANYEVENT_TARGET] = self.any_cls.solve(event)
        if checker := self.extra.get("checker", None):
            check_field_type(checker, any_event)


@event_preprocessor
async def _(state: T_State):
    state[ANYEVENT_TARGET] = None


Matcher.HANDLER_PARAM_TYPES += (AnyEventParam,)
Rule.HANDLER_PARAM_TYPES.append(AnyEventParam)
