from dataclasses import dataclass

class Command: ...

@dataclass
class ListPermissions(Command):
    TemplateSource: str


@dataclass
class VerifyPermissions(Command):
    TemplateSource: str
    Role: str
