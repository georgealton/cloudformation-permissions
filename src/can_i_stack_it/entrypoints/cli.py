import click

from ..bootstrap import bootstrap
from ..domain import commands


@click.group()
@click.option(
    "--template-source",
    required=True,
    help="StackId ARN, ChangeSet ARN, Local File, or stdin",
)
@click.pass_context
def cli(ctx, template_source) -> None:
    ctx.ensure_object(dict)
    ctx.obj["template_source"] = template_source


@cli.command(help="List permissions required to manage Stacks of this template")
@click.pass_context
def permissions(ctx) -> None:
    template_source = ctx.obj["template_source"]
    command = commands.ListPermissions(
        TemplateSource=template_source,
    )
    handler = bootstrap()[type[command]]
    handler(command)


@cli.command(help="Verify the --role-arn can manage Stacks by this template")
@click.option(
    "--role-arn",
    required=True,
    help="IAM Role ARN to verify it can manage stacks for this template",
)
@click.pass_context
def verify(ctx, role_arn) -> None:
    template_source = ctx.obj["template_source"]
    command = commands.VerifyPermissions(
        TemplateSource=template_source,
        Role=role_arn,
    )
    handler = bootstrap()[type[command]]
    handler(command)
