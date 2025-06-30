# CLI 엔트리포인트 (Typer) 
import sys
import typer
from typing import Optional
from pathlib import Path
from . import utils
from .summarizer import summarize_system_seq2seq, format_seq2seq_summary

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
    highlight: bool = typer.Option(
        True, "--highlight/--no-highlight", help="키워드 강조 표시 여부"
    ),
    max_length: Optional[int] = typer.Option(
        None, "--max-length", help="요약 최대 길이(토큰 수 기준, seq2seq 전용)", show_default=False
    ),
    min_length: Optional[int] = typer.Option(
        None, "--min-length", help="요약 최소 길이(토큰 수 기준, seq2seq 전용)", show_default=False
    )
):
    """
    AI 기반 이메일/메시지 요약 CLI 도구 (문맥 기반 요약/감정분석/키워드 강조)
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
    # 문맥 기반 요약 실행
    result = summarize_system_seq2seq(text, max_length=max_length, min_length=min_length)
    if result:
        typer.echo(format_seq2seq_summary(result))
    else:
        typer.echo("❌ 요약에 실패했습니다.", err=True)

if __name__ == "__main__":
    app() 