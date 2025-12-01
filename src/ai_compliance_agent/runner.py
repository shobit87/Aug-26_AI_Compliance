"""CLI entry-point for running the LangGraph workflow."""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from ai_compliance_agent.state import ensure_defaults
from ai_compliance_agent.workflow import build_workflow_app

cli = typer.Typer(add_completion=False)
console = Console()


@cli.command()
def run(
    request: str = typer.Argument(..., help="Compliance request to process"),
    document_path: Optional[str] = typer.Option(
        None,
        "--document-path",
        "-d",
        help="Optional path to a PDF, DOCX, or text file to review.",
    ),
):
    """Execute the workflow on a request."""
    workflow = build_workflow_app()
    initial_state = {"request": request, "document_path": document_path}
    result = workflow.invoke(initial_state)
    ensure_defaults(result)

    console.print(Panel.fit(result.get("documentation") or "No documentation produced."))
    if result.get("document_tone") or result.get("grammar_score") is not None:
        console.print("\n[bold]Document Quality[/bold]")
        if result.get("document_tone"):
            console.print(f"- Tone: {result['document_tone']}")
        if result.get("grammar_score") is not None:
            console.print(f"- Grammar Score: {result['grammar_score']:.2f}")

    if result.get("document_recommendations"):
        console.print("\n[bold]Document Recommendations[/bold]")
        for rec in result["document_recommendations"]:
            console.print(f"- {rec}")

    if result.get("corrected_document"):
        console.print("\n[bold]AI Corrected Document[/bold]")
        console.print(
            Panel.fit(result["corrected_document"], title="Corrected Draft", width=100)
        )

    console.print("\n[bold]Compliance Gaps[/bold]")
    for gap in result.get("compliance_gaps", []):
        console.print(f"- {gap}")
    if not result.get("compliance_gaps"):
        console.print("- None")

    console.print("\n[bold]History[/bold]")
    for entry in result.get("history", []):
        console.print(f"- {entry}")


def main():
    cli()


if __name__ == "__main__":
    main()
