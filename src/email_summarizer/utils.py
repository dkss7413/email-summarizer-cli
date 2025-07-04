# 보조 함수 (utils) 

import sys
import os
from typing import Optional, Tuple
from pathlib import Path


def read_text_file(file_path: Path) -> str:
    """
    파일에서 텍스트를 읽어옵니다.
    
    Args:
        file_path: 읽을 파일 경로 (Path 객체)
        
    Returns:
        str: 텍스트 내용
        
    Raises:
        FileNotFoundError: 파일을 찾을 수 없는 경우
        PermissionError: 파일 읽기 권한이 없는 경우
        UnicodeDecodeError: 파일 인코딩을 읽을 수 없는 경우
    """
    # 파일 존재 여부 확인
    if not file_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    
    # 파일 크기 확인 (100MB 제한)
    file_size = file_path.stat().st_size
    if file_size > 100 * 1024 * 1024:  # 100MB
        raise ValueError(f"파일이 너무 큽니다: {file_size / (1024*1024):.1f}MB (최대 100MB)")
    
    # 다양한 인코딩으로 파일 읽기 시도
    encodings = ['utf-8', 'cp949', 'euc-kr', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # 빈 파일 확인
            if not content.strip():
                raise ValueError("파일이 비어있습니다.")
                
            return content
            
        except UnicodeDecodeError:
            continue  # 다음 인코딩 시도
    
    # 모든 인코딩 시도 실패
    raise UnicodeDecodeError(f"파일 인코딩을 읽을 수 없습니다. 지원되는 인코딩: {', '.join(encodings)}")


def validate_text(text: str, min_length: int = 10) -> bool:
    """
    텍스트 내용을 검증합니다.
    
    Args:
        text: 검증할 텍스트
        min_length: 최소 길이
        
    Returns:
        bool: 유효성 여부
    """
    if not text:
        return False
    
    if len(text.strip()) < min_length:
        return False
    
    # 특수 문자만 있는 경우 확인
    import re
    if re.match(r'^[\s\W]+$', text):
        return False
    
    return True


def read_file_content(file_path: str) -> Tuple[str, Optional[str]]:
    """
    파일에서 텍스트를 읽어옵니다.
    
    Args:
        file_path: 읽을 파일 경로
        
    Returns:
        Tuple[str, Optional[str]]: (텍스트 내용, 오류 메시지)
    """
    try:
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            return "", f"파일을 찾을 수 없습니다: {file_path}"
        
        # 파일 크기 확인 (100MB 제한)
        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:  # 100MB
            return "", f"파일이 너무 큽니다: {file_size / (1024*1024):.1f}MB (최대 100MB)"
        
        # 다양한 인코딩으로 파일 읽기 시도
        encodings = ['utf-8', 'cp949', 'euc-kr', 'latin-1']
        content = ""
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break  # 성공하면 루프 종료
            except UnicodeDecodeError:
                continue  # 다음 인코딩 시도
        
        if not content:
            return "", f"파일 인코딩을 읽을 수 없습니다. 지원되는 인코딩: {', '.join(encodings)}"
            
        # 빈 파일 확인
        if not content.strip():
            return "", "파일이 비어있습니다."
            
        return content, None
        
    except PermissionError:
        return "", f"파일 읽기 권한이 없습니다: {file_path}"
    except Exception as e:
        return "", f"파일 읽기 중 오류가 발생했습니다: {str(e)}"


def read_stdin_content() -> Tuple[str, Optional[str]]:
    """
    표준입력에서 텍스트를 읽어옵니다.
    
    Returns:
        Tuple[str, Optional[str]]: (텍스트 내용, 오류 메시지)
    """
    try:
        # 표준입력이 터미널인지 확인
        if sys.stdin.isatty():
            return "", "표준입력이 터미널입니다. 파일을 지정하거나 파이프로 텍스트를 전달하세요."
        
        # 표준입력 읽기 (바이너리로 읽은 후 디코딩)
        try:
            # 먼저 텍스트 모드로 시도
            content = sys.stdin.read()
        except UnicodeDecodeError:
            # 실패하면 바이너리로 읽어서 디코딩 시도
            import io
            sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
            content = sys.stdin.read()
        
        # 빈 입력 확인
        if not content.strip():
            return "", "입력된 텍스트가 없습니다."
            
        return content, None
        
    except Exception as e:
        return "", f"표준입력 읽기 중 오류가 발생했습니다: {str(e)}"


def validate_text_content(text: str, min_length: int = 10) -> Tuple[bool, Optional[str]]:
    """
    텍스트 내용을 검증합니다.
    
    Args:
        text: 검증할 텍스트
        min_length: 최소 길이
        
    Returns:
        Tuple[bool, Optional[str]]: (유효성, 오류 메시지)
    """
    if not text:
        return False, "텍스트가 비어있습니다."
    
    if len(text.strip()) < min_length:
        return False, f"텍스트가 너무 짧습니다. 최소 {min_length}자 이상이어야 합니다."
    
    # 특수 문자만 있는 경우 확인
    import re
    if re.match(r'^[\s\W]+$', text):
        return False, "텍스트에 의미 있는 내용이 없습니다."
    
    return True, None


def get_input_source_info(input_path: Optional[str]) -> str:
    """
    입력 소스 정보를 반환합니다.
    
    Args:
        input_path: 입력 파일 경로
        
    Returns:
        str: 입력 소스 정보
    """
    if input_path:
        file_size = os.path.getsize(input_path)
        return f"파일: {input_path} ({file_size:,} bytes)"
    else:
        return "표준입력"


def format_text_preview(text: str, max_length: int = 200) -> str:
    """
    텍스트 미리보기를 포맷합니다.
    
    Args:
        text: 원본 텍스트
        max_length: 최대 길이
        
    Returns:
        str: 포맷된 미리보기
    """
    if len(text) <= max_length:
        return text
    
    # 문장 단위로 자르기
    sentences = text[:max_length].split('.')
    if len(sentences) > 1:
        preview = '.'.join(sentences[:-1]) + '.'
    else:
        preview = text[:max_length]
    
    return f"{preview}... (총 {len(text):,}자)" 