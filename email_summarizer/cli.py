# CLI 엔트리포인트 (Typer) 
import sys
import typer
from typing import Optional
from . import utils
from . import summarizer

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
    verbose: bool = typer.Option(False, "--verbose", "-v", help="상세 정보 출력", show_default=True),
):
    """
    입력 파일 또는 표준입력으로부터 텍스트를 받아 요약 결과를 출력합니다.
    """
    # 입력 텍스트 읽기
    text, error = "", None
    
    if input:
        # 파일에서 읽기
        text, error = utils.read_file_content(input)
        if error:
            typer.echo(f"[오류] {error}", err=True)
            raise typer.Exit(code=1)
    else:
        # 표준입력에서 읽기
        text, error = utils.read_stdin_content()
        if error:
            typer.echo(f"[오류] {error}", err=True)
            raise typer.Exit(code=1)
    
    # 텍스트 검증
    is_valid, validation_error = utils.validate_text_content(text)
    if not is_valid:
        typer.echo(f"[오류] {validation_error}", err=True)
        raise typer.Exit(code=1)
    
    # 상세 정보 출력 (verbose 모드)
    if verbose:
        source_info = utils.get_input_source_info(input)
        typer.echo(f"[정보] 입력 소스: {source_info}")
        typer.echo(f"[정보] 텍스트 길이: {len(text):,}자")
        typer.echo(f"[정보] 요약 설정: 길이={length}, 언어={language}, 강조={highlight}")
        typer.echo(f"[정보] 텍스트 미리보기: {utils.format_text_preview(text)}")
        typer.echo("─" * 50)
    
    # 요약 실행
    try:
        summary_result = summarizer.summarize_text(text, length=length, language=language)
        
        # 요약 결과 출력
        formatted_output = summarizer.format_summary_output(summary_result, highlight=highlight)
        typer.echo(formatted_output)
        
    except Exception as e:
        typer.echo(f"[오류] 요약 처리 중 오류가 발생했습니다: {str(e)}", err=True)
        raise typer.Exit(code=1) 