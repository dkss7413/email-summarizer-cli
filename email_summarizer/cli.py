# CLI 엔트리포인트 (Typer) 
import sys
import typer
from typing import Optional

app = typer.Typer(help="AI 기반 이메일/메시지 요약 CLI 도구")

@app.callback()
def main():
    """
    AI 기반 이메일/메시지 요약 CLI 도구
    """
    pass

@app.command(name="summarize")
def summarize_command(
    input: Optional[str] = typer.Option(None, "--input", "-i", help="입력 파일 경로. 생략 시 표준입력 사용."),
    length: str = typer.Option("short", "--length", "-l", help="요약 길이: short 또는 long", show_default=True),
    language: str = typer.Option("ko", "--language", "-lang", help="요약 언어: ko 또는 en", show_default=True),
    highlight: bool = typer.Option(False, "--highlight", "-hl", help="키워드 강조 출력 여부", show_default=True),
):
    """
    입력 파일 또는 표준입력으로부터 텍스트를 받아 요약 결과를 출력합니다.
    """
    # TODO: 요약 로직 연동
    typer.echo(f"[DEBUG] input={input}, length={length}, language={language}, highlight={highlight}")
    if input:
        try:
            with open(input, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            typer.echo(f"[오류] 파일을 찾을 수 없습니다: {input}", err=True)
            raise typer.Exit(code=1)
    else:
        if sys.stdin.isatty():
            typer.echo("[오류] 입력 파일을 지정하거나 파이프로 텍스트를 전달하세요.", err=True)
            raise typer.Exit(code=1)
        text = sys.stdin.read()
    # TODO: 요약 함수 호출 및 결과 출력
    typer.echo(f"[입력 텍스트 일부]: {text[:100]} ...") 