# CLI 엔트리포인트 (Typer) 
import sys
import typer
from typing import Optional
from pathlib import Path
from . import utils
from .summarizer import summarize_system_seq2seq, format_seq2seq_summary
from .gmail_utils import list_recent_emails, get_email_body
import re

app = typer.Typer(
    name="email-summarizer",
    help="AI 기반 이메일/메시지 요약 CLI 도구 (임베딩/감정분석/키워드 강조 지원)",
    add_completion=False
)

@app.command()
def summarize(
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
    텍스트 파일 또는 입력받은 내용을 AI로 요약합니다. (문맥 기반 요약/감정분석/키워드 강조)
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
    # 본문 길이 체크 (30자 이하일 때 요약 시도 안 함, 공백/특수문자 제외)
    MIN_TEXT_LENGTH = 30
    text_only = re.sub(r'[^\w가-힣a-zA-Z0-9]', '', text)
    if len(text_only.strip()) < MIN_TEXT_LENGTH:
        typer.echo(f"❌ 본문이 너무 짧아 요약을 진행할 수 없습니다. (최소 {MIN_TEXT_LENGTH}자 필요)", err=True)
        raise typer.Exit(1)
    # 문맥 기반 요약 실행
    result = summarize_system_seq2seq(text, max_length=max_length, min_length=min_length)
    if result:
        typer.echo(format_seq2seq_summary(result))
    else:
        typer.echo("❌ 요약에 실패했습니다.", err=True)

@app.command()
def gmail():
    """
    Gmail API로 최근 10개 메일을 불러오고, 선택한 메일을 요약합니다.
    """
    typer.echo("Gmail에서 최근 메일을 불러오는 중...")
    try:
        emails = list_recent_emails(10)
        if not emails:
            typer.echo("📭 최근 메일이 없습니다.")
            raise typer.Exit(0)
        typer.echo("\n[최근 메일 목록]")
        for idx, mail in enumerate(emails, 1):
            typer.echo(f"{idx}. [{mail['date']}] {mail['from']} - {mail['subject']}")
        idx = typer.prompt("요약할 메일 번호를 입력하세요", type=int)
        if not (1 <= idx <= len(emails)):
            typer.echo("❌ 잘못된 번호입니다.", err=True)
            raise typer.Exit(1)
        mail_id = emails[idx-1]['id']
        body = get_email_body(mail_id)
        # 디버깅: 추출된 본문 출력 (제거)
        # typer.echo("\n[추출된 본문 디버그 출력]\n" + body + "\n[본문 끝]\n", err=True)
        if not body.strip():
            typer.echo("❌ 본문이 비어있거나 텍스트를 추출할 수 없습니다.", err=True)
            raise typer.Exit(1)
        # 본문 길이 체크 (30자 이하일 때 요약 시도 안 함, 공백/특수문자 제외)
        MIN_TEXT_LENGTH = 30
        body_only = re.sub(r'[^\w가-힣a-zA-Z0-9]', '', body)
        if len(body_only.strip()) < MIN_TEXT_LENGTH:
            typer.echo(f"❌ 본문이 너무 짧아 요약을 진행할 수 없습니다. (최소 {MIN_TEXT_LENGTH}자 필요)", err=True)
            raise typer.Exit(1)
        typer.echo("\n[메일 본문 요약 결과]")
        result = summarize_system_seq2seq(body)
        typer.echo(format_seq2seq_summary(result))
    except Exception as e:
        typer.echo(f"❌ Gmail API 오류: {e}", err=True)
        raise typer.Exit(1)

@app.command()
def gmail_logout():
    """
    Gmail 인증 토큰 파일(token.json, token.pickle 등)을 삭제하여 계정 연결을 해제합니다.
    """
    import os
    deleted = False
    for fname in ["token.json", "token.pickle"]:
        if os.path.exists(fname):
            try:
                os.remove(fname)
                typer.echo(f"✅ {fname} 파일을 삭제했습니다. (계정 연결 해제 완료)")
                deleted = True
            except Exception as e:
                typer.echo(f"❌ {fname} 파일 삭제 중 오류: {e}", err=True)
    if not deleted:
        typer.echo("ℹ️ 삭제할 인증 토큰 파일(token.json, token.pickle)이 없습니다.")

if __name__ == "__main__":
    app() 