import streamlit as st
import pdfplumber
from openai import OpenAI
 
# --- 페이지 설정 ---
st.set_page_config(
    page_title="컬처핏 인터뷰 가이드",
    page_icon="💬",
    layout="wide",
)
 
# --- CSS ---
TOSS_CSS = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');
 
/* 전역 리셋 */
.stApp {
    background-color: #0d1117 !important;
    font-family: 'Pretendard Variable', -apple-system, sans-serif !important;
}
 
/* 메인 컨테이너 여백 */
.block-container {
    max-width: 960px !important;
    padding: 3rem 1.5rem 4rem !important;
}
 
/* 히어로 섹션 */
.hero-section {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
}
.hero-section h1 {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.03em;
    line-height: 1.3;
    margin-bottom: 0.75rem;
}
.hero-section .subtitle {
    font-size: 1.05rem;
    color: #8b95a1;
    font-weight: 400;
    line-height: 1.6;
}
.hero-section .accent {
    color: #3182f6;
    font-weight: 600;
}
 
/* 카드 스타일 */
.toss-card {
    background: #1b1f27;
    border: 1px solid #2c313a;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s ease;
}
.toss-card:hover {
    border-color: #3182f6;
}
.toss-card h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.toss-card .card-desc {
    font-size: 0.88rem;
    color: #6b7684;
    margin-bottom: 1.2rem;
}
 
/* 구분선 */
.toss-divider {
    border: none;
    border-top: 1px solid #2c313a;
    margin: 2rem 0;
}
 
/* 결과 카드 */
.result-card {
    background: #1b1f27;
    border: 1px solid #2c313a;
    border-radius: 20px;
    padding: 2.5rem;
    margin-top: 1.5rem;
}
.result-card h2 {
    color: #ffffff;
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
}
 
/* 성공 배지 */
.success-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(49, 130, 246, 0.12);
    color: #3182f6;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
 
/* Streamlit 위젯 커스텀 */
.stTextArea textarea {
    background: #161b22 !important;
    border: 1px solid #2c313a !important;
    border-radius: 14px !important;
    color: #e6edf3 !important;
    font-family: 'Pretendard Variable', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: #3182f6 !important;
    box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.15) !important;
}
 
/* 파일 업로더 */
[data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 2px dashed #2c313a !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #3182f6 !important;
}
 
/* 버튼 - 토스 블루 */
.stButton > button {
    background: #3182f6 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Pretendard Variable', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    letter-spacing: -0.01em !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #1b6ff4 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(49, 130, 246, 0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
 
/* 다운로드 버튼 */
.stDownloadButton > button {
    background: transparent !important;
    color: #3182f6 !important;
    border: 1.5px solid #3182f6 !important;
    border-radius: 14px !important;
    font-family: 'Pretendard Variable', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    padding: 0.7rem 1.5rem !important;
    transition: all 0.15s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(49, 130, 246, 0.08) !important;
}
 
/* 라디오 버튼 */
.stRadio > div {
    gap: 0.5rem !important;
}
.stRadio label {
    color: #e6edf3 !important;
    font-weight: 500 !important;
}
 
/* 스피너 */
.stSpinner > div {
    border-top-color: #3182f6 !important;
}
 
/* 에러/성공 메시지 */
.stAlert {
    border-radius: 14px !important;
}
 
/* 마크다운 결과 텍스트 */
.result-card .stMarkdown h1,
.result-card .stMarkdown h2,
.result-card .stMarkdown h3 {
    color: #ffffff !important;
}
.result-card .stMarkdown p,
.result-card .stMarkdown li {
    color: #c9d1d9 !important;
    line-height: 1.7 !important;
}
 
/* 스크롤바 */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #0d1117;
}
::-webkit-scrollbar-thumb {
    background: #2c313a;
    border-radius: 3px;
}
 
/* Streamlit 기본 헤더/푸터 숨김 */
header[data-testid="stHeader"] {
    background: transparent !important;
}
.stDeployButton {
    display: none !important;
}
 
/* 서브헤더 숨김 (카드로 대체) */
.stSubheader {
    display: none !important;
}
 
/* 파일 업로드 캡션 */
.stCaption {
    color: #6b7684 !important;
}
 
/* 탭/컬럼 간격 */
[data-testid="stHorizontalBlock"] {
    gap: 1.5rem !important;
}
</style>
"""
 
# --- 기본 리더십 원칙 ---
DEFAULT_PRINCIPLES = """
여기에 회사의 핵심가치 OR 리더십 원칙 OR 일하는 방식 등을 넣어주세요
"""
 
# --- PDF/텍스트 추출 ---
def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""
 
# --- LLM 호출 ---
def generate_interview_guide(leadership_text, resume_text, language):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
 
    if language == "한국어":
        lang_instruction = """
모든 내용을 100% 한국어로만 작성하세요.
영어 단어나 문장을 넣지 마세요.
"""
        format_instruction = """
아래와 같은 한국어 Markdown 형식을 사용하세요:
 
# 인터뷰 가이드
 
## [리더십 원칙 이름]
 
- 한 줄 요약: ...
- 핵심 질문 1: ...
  - 들어야 할 포인트:
    - ...
    - ...
  - 주의할 Red flag:
    - ...
    - ...
- 핵심 질문 2: ...
  - 들어야 할 포인트:
    - ...
  - 주의할 Red flag:
    - ...
 
각 리더십 원칙마다 2개의 질문을 작성하세요.
"""
    else:
        lang_instruction = """
Write 100% in English only.
Do NOT include any Korean words or sentences.
"""
        format_instruction = """
Use the following Markdown structure in English:
 
# Interview Guide
 
## [Leadership Principle Name]
 
- One-line summary: ...
- Key question 1: ...
  - What to listen for:
    - ...
    - ...
  - Red flags:
    - ...
    - ...
- Key question 2: ...
  - What to listen for:
    - ...
  - Red flags:
    - ...
 
Create 2–3 questions for each leadership principle.
"""
 
    system_prompt = f"""
당신은 글로벌 테크 기업의 시니어 인터뷰어입니다.
당신의 역할은 "리더십 원칙 기반 행동면접 질문(Behavioral Interview Questions)"을 생성하고,
지원자의 경력과 경험에 기반해 깊이 있는 검증 질문을 만들어 내는 것입니다.
 
🎯 목표
- 각 코어밸류와 리더십 원칙을 실제 업무 행동으로 검증할 수 있는 질문 생성
- 지원자의 이력서 내용과 연결된 맞춤형 질문 생성
- 뻔한 질문이나 일반적인 교과서 질문 금지
- 리더십 원칙별로 "지원자의 경험을 검증하는 질문 + 구체적 follow-up 질문 + 평가 기준" 생성
- 모든 리더십 원칙을 빠짐없이 반영
 
📌 중요한 원칙
1) **이력서 기반 질문**
   - 이력서에서 실제 성과, 프로젝트, 맥락을 찾아 질문을 연결하세요.
   - "~했다고 했는데, 그 과정에서 어떤 지표를 개선했나요?" 같은 follow-up 포함.
 
2) **행동 중심 질문 (Behavioral Questions)**
   - "Tell me about a time when…" 또는
     "구체적으로 어떤 행동을 했는지 단계별로 설명해 주세요" 형태 포함.
 
3) **리더십 원칙 검증 초점**
   - 질문은 원칙을 직접적으로 검증해야 함
   - 예: Dive Deep → "데이터 깊이 파고들어 근본 원인을 찾은 사례"
 
4) **Red Flags는 진짜 면접 평가처럼**
   - 애매한 역할, 주도성 부족, 숫자 미제시, 책임 회피 등 명확하게 제시
   - 실제 테크기업 면접관이 쓰는 기준 활용
 
5) **질문은 실무자 레벨이 아닌 '시니어 인터뷰어 수준'의 난이도**
   - 표면적 설명 X
   - Trade-off, 문제 해결 방식, 지표 정의, 협업 갈등, 의사결정 기준 등 깊은 검증
 
📄 출력 형식 (이 구조는 반드시 유지)
 
# Interview Guide
 
## [리더십 원칙 이름]
 
- 한 줄 요약: (원칙의 핵심을 한 줄로 요약)
 
- 핵심 질문 1: (지원자 이력서를 기반으로 만든 질문)
  - 들어야 할 포인트:
    - (질문의 의도)
    - (지원자의 강점/행동/데이터 기반 사고 포함)
  - 주의할 Red flag:
    - (부정적 신호)
    - (책임 회피/모호한 설명 등)
  - 이력서 관련 내용:
    - (관련 문구)
 
- 핵심 질문 2:
  - 들어야 할 포인트:
    - ...
  - 주의할 Red flag:
    - ...
  - 이력서 관련 내용:
    - ...
 
각 리더십 원칙마다 2개의 고난도 질문을 생성하세요.
 
{lang_instruction}
{format_instruction}
"""
 
    user_prompt = f"""
[Leadership Principles]
{leadership_text}
 
[Candidate Resume]
{resume_text}
"""
 
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
 
    content = response.choices[0].message.content
    return content
 
 
# ========== UI ==========
 
# CSS 주입
st.markdown(TOSS_CSS, unsafe_allow_html=True)
 
# 히어로
st.markdown("""
<div class="hero-section">
    <h1>💬 컬처핏 인터뷰 가이드</h1>
    <p class="subtitle">
        핵심가치와 이력서를 넣으면<br>
        <span class="accent">항목별 면접 질문과 평가 포인트</span>를 자동으로 만들어드려요
    </p>
</div>
""", unsafe_allow_html=True)
 
# 두 컬럼
col1, col2 = st.columns(2)
 
with col1:
    st.markdown("""
    <div class="toss-card">
        <h3>📋 핵심가치 입력</h3>
        <p class="card-desc">회사의 핵심가치나 리더십 원칙을 붙여넣으세요</p>
    </div>
    """, unsafe_allow_html=True)
 
    leadership_text = st.text_area(
        "핵심가치",
        value=DEFAULT_PRINCIPLES,
        height=320,
        label_visibility="collapsed",
    )
 
    language = st.radio(
        "언어 선택",
        ["한국어", "English"],
        index=0,
        horizontal=True,
    )
 
with col2:
    st.markdown("""
    <div class="toss-card">
        <h3>📄 이력서 업로드</h3>
        <p class="card-desc">지원자의 PDF 또는 텍스트 파일을 올려주세요</p>
    </div>
    """, unsafe_allow_html=True)
 
    resume_file = st.file_uploader(
        "이력서",
        type=["pdf", "txt"],
        label_visibility="collapsed",
    )
    if resume_file:
        st.caption(f"✓ {resume_file.name}")
 
# 구분선
st.markdown('<hr class="toss-divider">', unsafe_allow_html=True)
 
# 생성 버튼
if st.button("인터뷰 가이드 생성하기", type="primary"):
    if not leadership_text.strip():
        st.error("핵심가치를 입력해주세요.")
    elif not resume_file:
        st.error("이력서를 업로드해주세요.")
    else:
        with st.spinner("가이드를 만들고 있어요..."):
            resume_text = extract_text_from_file(resume_file)
            if not resume_text.strip():
                st.error("이력서에서 텍스트를 추출하지 못했어요. 다른 파일로 시도해주세요.")
            else:
                guide_markdown = generate_interview_guide(
                    leadership_text, resume_text, language
                )
 
                # 성공 배지
                st.markdown(
                    '<div class="success-badge">✓ 생성 완료</div>',
                    unsafe_allow_html=True,
                )
 
                # 결과 카드
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(guide_markdown)
                st.markdown('</div>', unsafe_allow_html=True)
 
                # 다운로드
                md_bytes = guide_markdown.encode("utf-8")
                st.download_button(
                    label="📥 Markdown으로 다운로드",
                    data=md_bytes,
                    file_name="interview_guide.md",
                    mime="text/markdown",
                )
