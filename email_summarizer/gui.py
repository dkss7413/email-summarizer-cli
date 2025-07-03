import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import re
from pathlib import Path
from typing import Optional

from .summarizer import summarize_system_seq2seq, format_seq2seq_summary
from .gmail_utils import list_recent_emails, get_email_body


# 이메일 요약 GUI 전체를 관리하는 클래스입니다.
class EmailSummarizerGUI:
    # GUI 창을 초기화하고 UI를 구성합니다.
    def __init__(self, root):
        self.root = root
        self.root.title("이메일 요약 도구")
        self.root.geometry("800x600")
        
        # 변수들
        self.current_text = tk.StringVar()
        self.max_length = tk.IntVar(value=150)
        self.min_length = tk.IntVar(value=40)
        self.highlight_keywords = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
    # 메인 UI 레이아웃과 위젯을 배치합니다.
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="📧 AI 이메일 요약 도구", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 입력 방식 선택
        input_frame = ttk.LabelFrame(main_frame, text="입력 방식", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 버튼들
        ttk.Button(input_frame, text="📁 파일에서 불러오기", 
                  command=self.load_file).grid(row=0, column=0, padx=5)
        ttk.Button(input_frame, text="📧 Gmail에서 불러오기", 
                  command=self.load_gmail).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="🧹 텍스트 지우기", 
                  command=self.clear_text).grid(row=0, column=2, padx=5)
        
        # 텍스트 입력 영역
        text_frame = ttk.LabelFrame(main_frame, text="텍스트 입력", padding="10")
        text_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.text_input = scrolledtext.ScrolledText(text_frame, height=10, width=80)
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 설정 프레임
        settings_frame = ttk.LabelFrame(main_frame, text="요약 설정", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 최대/최소 길이 설정
        ttk.Label(settings_frame, text="최대 길이:").grid(row=0, column=0, padx=(0, 5))
        ttk.Spinbox(settings_frame, from_=20, to=500, textvariable=self.max_length, width=10).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(settings_frame, text="최소 길이:").grid(row=0, column=2, padx=(0, 5))
        ttk.Spinbox(settings_frame, from_=10, to=200, textvariable=self.min_length, width=10).grid(row=0, column=3, padx=(0, 20))
        
        ttk.Checkbutton(settings_frame, text="키워드 강조", 
                       variable=self.highlight_keywords).grid(row=0, column=4)
        
        # 요약 버튼
        self.summarize_btn = ttk.Button(main_frame, text="🚀 요약 시작", 
                                       command=self.start_summarization)
        self.summarize_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
        # 진행 상황 표시
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 결과 출력 영역
        result_frame = ttk.LabelFrame(main_frame, text="요약 결과", padding="10")
        result_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=80)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(6, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
    # 파일에서 텍스트를 불러옵니다.
    def load_file(self):
        """파일에서 텍스트 불러오기"""
        file_path = filedialog.askopenfilename(
            title="텍스트 파일 선택",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(1.0, text)
                messagebox.showinfo("성공", f"파일을 성공적으로 불러왔습니다: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("오류", f"파일 읽기 실패: {str(e)}")
    
    # Gmail에서 이메일을 불러옵니다.
    def load_gmail(self):
        # Gmail API 호출 및 이메일 선택 다이얼로그를 실행하는 스레드 함수입니다.
        def gmail_thread():
            try:
                self.progress.start()
                self.summarize_btn.config(state='disabled')
                
                emails = list_recent_emails(10)
                if not emails:
                    messagebox.showinfo("알림", "최근 메일이 없습니다.")
                    return
                
                # 이메일 선택 다이얼로그
                dialog = GmailSelectionDialog(self.root, emails)
                if dialog.result:
                    selected_email = dialog.result
                    body = get_email_body(selected_email['id'])
                    
                    if not body.strip():
                        messagebox.showerror("오류", "본문이 비어있거나 텍스트를 추출할 수 없습니다.")
                        return
                    
                    # 본문 길이 체크
                    MIN_TEXT_LENGTH = 30
                    body_only = re.sub(r'[^\w가-힣a-zA-Z0-9]', '', body)
                    if len(body_only.strip()) < MIN_TEXT_LENGTH:
                        messagebox.showerror("오류", f"본문이 너무 짧아 요약을 진행할 수 없습니다. (최소 {MIN_TEXT_LENGTH}자 필요)")
                        return
                    
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, body)
                    messagebox.showinfo("성공", f"Gmail에서 이메일을 불러왔습니다: {selected_email['subject']}")
                    
            except Exception as e:
                messagebox.showerror("오류", f"Gmail API 오류: {str(e)}")
            finally:
                self.progress.stop()
                self.summarize_btn.config(state='normal')
        
        threading.Thread(target=gmail_thread, daemon=True).start()
    
    # 입력/결과 텍스트를 모두 지웁니다.
    def clear_text(self):
        """텍스트 지우기"""
        self.text_input.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
    
    # 입력된 텍스트를 요약합니다.
    def start_summarization(self):
        # 실제 요약 처리를 백그라운드에서 실행하는 스레드 함수입니다.
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("경고", "요약할 텍스트를 입력해주세요.")
            return
        
        # 본문 길이 체크
        MIN_TEXT_LENGTH = 30
        text_only = re.sub(r'[^\w가-힣a-zA-Z0-9]', '', text)
        if len(text_only.strip()) < MIN_TEXT_LENGTH:
            messagebox.showerror("오류", f"본문이 너무 짧아 요약을 진행할 수 없습니다. (최소 {MIN_TEXT_LENGTH}자 필요)")
            return
        
        def summarize_thread():
            try:
                self.progress.start()
                self.summarize_btn.config(state='disabled')
                
                result = summarize_system_seq2seq(
                    text, 
                    max_length=self.max_length.get(),
                    min_length=self.min_length.get()
                )
                
                if result:
                    formatted_result = format_seq2seq_summary(result)
                    self.result_text.delete(1.0, tk.END)
                    self.result_text.insert(1.0, formatted_result)
                else:
                    messagebox.showerror("오류", "요약에 실패했습니다.")
                    
            except Exception as e:
                messagebox.showerror("오류", f"요약 중 오류 발생: {str(e)}")
            finally:
                self.progress.stop()
                self.summarize_btn.config(state='normal')
        
        threading.Thread(target=summarize_thread, daemon=True).start()


# Gmail 이메일 선택 다이얼로그를 관리하는 클래스입니다.
class GmailSelectionDialog:
    # 다이얼로그 창을 초기화하고 이메일 목록을 표시합니다.
    def __init__(self, parent, emails):
        self.result = None
        self.emails = emails
        
        # 새 창 생성
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Gmail 이메일 선택")
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # UI 구성
        ttk.Label(self.dialog, text="요약할 이메일을 선택하세요:", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # 이메일 목록
        list_frame = ttk.Frame(self.dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 트리뷰 생성
        columns = ('번호', '날짜', '보낸사람', '제목')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column('보낸사람', width=150)
        self.tree.column('제목', width=250)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 이메일 데이터 추가
        for idx, email in enumerate(emails, 1):
            self.tree.insert('', tk.END, values=(
                idx,
                email['date'],
                email['from'][:30] + '...' if len(email['from']) > 30 else email['from'],
                email['subject'][:50] + '...' if len(email['subject']) > 50 else email['subject']
            ))
        
        # 버튼들
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="선택", command=self.select_email).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="취소", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # 더블클릭 이벤트
        self.tree.bind('<Double-1>', lambda e: self.select_email())
        
        # 창 중앙 정렬
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # 모달 대기
        self.dialog.wait_window()
    
    # 사용자가 이메일을 선택했을 때 호출됩니다.
    def select_email(self):
        """이메일 선택"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            idx = item['values'][0] - 1  # 0-based index
            self.result = self.emails[idx]
        self.dialog.destroy()
    
    # 다이얼로그를 취소(닫기)합니다.
    def cancel(self):
        """취소"""
        self.dialog.destroy()


# GUI를 실행하는 진입점 함수입니다.
def run_gui():
    """GUI 실행"""
    root = tk.Tk()
    app = EmailSummarizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui() 