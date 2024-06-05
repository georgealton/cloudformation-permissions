import click

from ..bootstrap import bootstrap
from ..domain import commands


@click.group()
@click.option(
    "--template-source",
    required=True,
    help="""
    StackId ARN, ChangeSet ARN, Local File, or stdin
    """,
)
@click.pass_context
def cli(ctx, template_source: str) -> None:
    ctx.ensure_object(dict)
    ctx.obj["template_source"] = template_source


@cli.command(
    help="""
    List permissions required to manage Stacks of this Template
    """,
)
@click.pass_context
def permissions(ctx) -> None:
    template_source = ctx.obj["template_source"]
    command = commands.ListPermissions(
        TemplateSource=template_source,
    )
    handler = bootstrap()[type(command)]
    handler(command)


@cli.command(
    help="""
    Verify the --role-arn can manage Stacks of this Template
    """,
)
@click.option(
    "--role-arn",
    help="""
    IAM Role ARN to verify it can manage stacks for this template. When this is
    not set the current Identity will be used.
    """,
)
@click.pass_context
def verify(ctx, role_arn: str | None = None) -> None:
    template_source = ctx.obj["template_source"]
    command = commands.VerifyPermissions(
        TemplateSource=template_source,
        Role=role_arn,
    )
    handler = bootstrap()[type(command)]
    handler(command)
