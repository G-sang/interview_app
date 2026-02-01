import streamlit as st
import pdfplumber
from openai import OpenAI

# --- 기본 리더십 원칙 예시 ---
DEFAULT_PRINCIPLES = """
비전 & 경쟁력
Connect & Unlock Value
세상에 없던 새로운 가치를 발굴하며 앞선 기술력으로 경계없는 확장을 만들어 갑니다.
평균수명 상승과 동시에 자산관리에 대한 인식이 점점 높아지고 있는 현시대에 발맞추어 두나무는 블록체인, 증권 분야 등에서 최초의 서비스들을 세상에 내보였고 업계 선두를 달리고 있습니다. 두나무의 모든 서비스는 ‘이용자 편의’와 ‘안정성’을 최우선으로 고려하여 만들고 있기 때문에 이용자들의 높은 ‘신뢰성’을 쌓을 수 있었고 이것이 곧 두나무의 경쟁력이 되었습니다.
앞으로도 두나무는 변화의 기류를 포착하고 ‘앞선 기술력’과 ‘안정성’을 기반으로 세상에 없던 새로운 가치를 발굴하고 확장해 나갈 것입니다.

   

핵심가치
Trust
두나무의 모두는 각 분야의 전문가입니다. 서비스에 대한 신뢰를 최우선으로 생각하고, 서로의 전문성을 인정하며 의견과 결정을 존중합니다. 편리하고 안전하게 이용할 수 있는 서비스를 만들고, 신뢰를 바탕으로 수평적인 소통을 합니다.

Drive
선두에 있지만 더 빠르게 나아갑니다. 기회를 놓치지 않고, 실패를 두려워하지 않으며, 목표에 몰입하고, 혁신을 주도합니다.
모든 의사 결정의 중심은 고객입니다. 항상 고객을 위해 해야 할 일을 고민하고, 발견하며, 실행합니다. 의사결정권자는 수평적인 소통을 바탕으로 빠르고 정확한 결정을 내립니다.

   

인재상 2.0
Passion & Performance-Oriented (열정과 성과지향)
최고의 성과를 목표로 도전합니다.
변화의 흐름을 예측하고, 고객의 관심사를 끊임 없이 탐구하며, 실패의 경험도 기회로 삼는 열정 가득한 인재입니다.

Diversity & Decisiveness (다양성과 결단력)
서로 다른 경험과 지식을 이해하고 다양한 의견을 주고 받으며
때로는 건설적인 대안을 제시하면서 최선의 결정을 내릴 수 있도록 합니다. 정해진 결정을 수용하고 적극적으로 실행합니다.

Respectful & Considerate (존중과 배려)
존중과 배려의 중요성을 이해합니다.
회사 동료 및 파트너사와 협업 과정에서 겸손한 태도를 갖고 상대의 업무, 경험, 일 하는 방식을 존중합니다.

Integrity & Completeness (진정성과 책임감)
서비스를 향한 진심으로, 주어진 일의 시작부터 끝까지 책임감을 갖고 임합니다.
회사와 서비스를 위해 무엇이 최선인지 동료들과 함께 고민하고 토론하여 신뢰와 성실이 고객에게 전해질 수 있도록 노력합니다.
"""

# --- PDF 또는 텍스트 파일에서 텍스트 추출 ---
def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    # PDF인 경우
    if uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text

    # 그 외 (txt 등)
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""

# --- LLM 호출: 리더십별 인터뷰 가이드 생성 ---
def generate_interview_guide(leadership_text, resume_text, language):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # 언어별 규칙 & 포맷 예시
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
    else:  # English
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
- 각 리더십 원칙을 실제 업무 행동으로 검증할 수 있는 질문 생성
- 지원자의 이력서 내용과 연결된 맞춤형 질문 생성
- 뻔한 질문이나 일반적인 교과서 질문 금지
- 리더십 원칙별로 “지원자의 경험을 검증하는 질문 + 구체적 follow-up 질문 + 평가 기준” 생성
- 모든 리더십 원칙을 빠짐없이 반영

📌 중요한 원칙
1) **이력서 기반 질문**  
   - 이력서에서 실제 성과, 프로젝트, 맥락을 찾아 질문을 연결하세요.  
   - “~했다고 했는데, 그 과정에서 어떤 지표를 개선했나요?” 같은 follow-up 포함.  

2) **행동 중심 질문 (Behavioral Questions)**  
   - “Tell me about a time when…” 또는  
     “구체적으로 어떤 행동을 했는지 단계별로 설명해 주세요” 형태 포함.  

3) **리더십 원칙 검증 초점**  
   - 질문은 원칙을 직접적으로 검증해야 함  
   - 예: Dive Deep → “데이터 깊이 파고들어 근본 원인을 찾은 사례”  

4) **Red Flags는 진짜 면접 평가처럼**  
   - 애매한 역할, 주도성 부족, 숫자 미제시, 책임 회피 등 명확하게 제시  
   - 실제 테크기업 면접관이 쓰는 기준 활용  

5) **질문은 실무자 레벨이 아닌 ‘시니어 인터뷰어 수준’의 난이도**  
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

# --- Streamlit UI ---
st.set_page_config(page_title="리더십 원칙 기반 인터뷰 가이드", layout="wide")
st.title("🚀 리더십 원칙 기반 인터뷰 가이드 생성기")

st.markdown(
    "리더십 원칙과 이력서를 기반으로, 면접관이 바로 쓸 수 있는 "
    "**리더십별 인터뷰 질문 & 확인 포인트**를 자동 생성합니다."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 리더십 원칙")
    leadership_text = st.text_area(
        "회사 리더십 원칙을 붙여넣으세요.",
        value=DEFAULT_PRINCIPLES,
        height=300,
    )

    # 언어 선택
    language = st.radio(
        "인터뷰 가이드 언어 선택",
        ["한국어", "English"],
        index=0,
        horizontal=True,
    )

with col2:
    st.subheader("2. 이력서 업로드")
    resume_file = st.file_uploader(
        "PDF 또는 텍스트 파일을 올리세요.",
        type=["pdf", "txt"],
    )
    if resume_file:
        st.caption(f"업로드된 파일: {resume_file.name}")

st.divider()

if st.button("📄 인터뷰 가이드 생성하기", type="primary"):
    if not leadership_text.strip():
        st.error("리더십 원칙을 입력해주세요.")
    elif not resume_file:
        st.error("이력서를 업로드해주세요.")
    else:
        with st.spinner("LLM으로 인터뷰 가이드를 생성하는 중입니다..."):
            resume_text = extract_text_from_file(resume_file)
            if not resume_text.strip():
                st.error("이력서 텍스트를 추출하지 못했습니다. 다른 형식으로 시도해 주세요.")
            else:
                guide_markdown = generate_interview_guide(
                    leadership_text, resume_text, language
                )
                st.success("생성 완료!")

                st.subheader("📄 인터뷰 가이드 미리보기")
                st.markdown(guide_markdown)

                # 다운로드용
                md_bytes = guide_markdown.encode("utf-8")
                st.download_button(
                    label="📥 Markdown 파일로 다운로드",
                    data=md_bytes,
                    file_name="interview_guide.md",
                    mime="text/markdown",
                )
