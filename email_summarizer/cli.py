# CLI 엔트리포인트 (Typer) 
import sys
import typer
from typing import Optional
from pathlib import Path
from . import utils
from . import summarizer

app = typer.Typer(
    name="email-summarizer",
    help="AI 기반 이메일/메시지 요약 CLI 도구",
    add_completion=False
)

@app.command()
def main(
    file: Optional[Path] = typer.Argument(
        None,
        help="요약할 텍스트 파일 경로 (지정하지 않으면 표준입력 사용)"
    ),
    length: str = typer.Option(
        "short",
        "--length", "-l",
        help="요약 길이 (short/long)",
        case_sensitive=False
    ),
    language: str = typer.Option(
        "auto",
        "--language", "--lang",
        help="언어 설정 (ko/en/mixed/auto) - auto는 자동 감지",
        case_sensitive=False
    ),
    highlight: bool = typer.Option(
        False,
        "--highlight", "-h",
        help="키워드 강조 표시 (색상 및 굵기)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="상세 정보 출력"
    )
):
    """
    AI 기반 이메일/메시지 요약 CLI 도구
    
    파일에서 텍스트를 읽어 요약을 생성합니다.
    자동 언어 감지 기능을 지원합니다.
    """
    try:
        # 입력 텍스트 읽기
        if file:
            if verbose:
                typer.echo(f"📁 파일 읽는 중: {file}")
            
            text = utils.read_text_file(file)
            if verbose:
                typer.echo(f"✅ 파일 읽기 완료 ({len(text)}자)")
        else:
            if verbose:
                typer.echo("📝 표준입력에서 텍스트 읽는 중...")
            
            text = sys.stdin.read()
            if verbose:
                typer.echo(f"✅ 표준입력 읽기 완료 ({len(text)}자)")
        
        # 텍스트 검증
        if not utils.validate_text(text):
            typer.echo("❌ 유효하지 않은 텍스트입니다.", err=True)
            raise typer.Exit(1)
        
        if verbose:
            typer.echo(f"🔍 텍스트 검증 완료")
            typer.echo(f"📊 요약 설정: 길이={length}, 언어={language}, 강조={highlight}")
        
        # 요약 생성
        if verbose:
            typer.echo("🤖 AI 요약 생성 중...")
        
        summary_result = summarizer.summarize_text(text, length, language)
        
        if verbose:
            typer.echo("✅ 요약 생성 완료")
        
        # 결과 출력
        formatted_output = summarizer.format_summary_output(summary_result, highlight)
        typer.echo(formatted_output)
        
    except FileNotFoundError:
        typer.echo(f"❌ 파일을 찾을 수 없습니다: {file}", err=True)
        raise typer.Exit(1)
    except PermissionError:
        typer.echo(f"❌ 파일에 접근할 권한이 없습니다: {file}", err=True)
        raise typer.Exit(1)
    except UnicodeDecodeError as e:
        typer.echo(f"❌ 파일 인코딩 오류: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ 오류가 발생했습니다: {e}", err=True)
        if verbose:
            import traceback
            typer.echo(traceback.format_exc(), err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 