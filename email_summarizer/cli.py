# CLI 엔트리포인트 (Typer) 
import sys
import typer
from typing import Optional
from pathlib import Path
from . import utils
from .summarizer import summarize_system

app = typer.Typer(
    name="email-summarizer",
    help="AI 기반 이메일/메시지 요약 CLI 도구 (임베딩/감정분석/키워드 강조 지원)",
    add_completion=False
)

@app.command()
def main(
    file: Optional[Path] = typer.Option(
        None, "--file", "-f", help="요약할 텍스트 파일 경로"
    ),
    length: str = typer.Option(
        "normal", "--length", "-l", help="요약 길이 (short|normal|long)", case_sensitive=False
    ),
    highlight: bool = typer.Option(
        True, "--highlight/--no-highlight", help="키워드 강조 표시 여부"
    )
):
    """
    AI 기반 이메일/메시지 요약 CLI 도구 (임베딩/감정분석/키워드 강조)
    """
    # 입력 텍스트 읽기
    if file:
        if not file.exists():
            typer.echo(f"❌ 파일을 찾을 수 없습니다: {file}", err=True)
            raise typer.Exit(1)
        try:
            text = file.read_text(encoding="utf-8")
        except Exception as e:
            typer.echo(f"❌ 파일 읽기 오류: {e}", err=True)
            raise typer.Exit(1)
    else:
        typer.echo("📥 표준 입력에서 텍스트를 읽는 중... (Ctrl+D로 입력 완료)")
        try:
            text = sys.stdin.read()
        except Exception as e:
            typer.echo(f"❌ 표준 입력 읽기 오류: {e}", err=True)
            raise typer.Exit(1)
    # 요약 실행 (summarize_system은 내부에서 print로 결과 출력)
    result = summarize_system(text, length_option=length, highlight=highlight)
    if result:
        from .summarizer import format_summary_output
        typer.echo(format_summary_output(result))
    else:
        typer.echo("❌ 요약에 실패했습니다.", err=True)

if __name__ == "__main__":
    app() 