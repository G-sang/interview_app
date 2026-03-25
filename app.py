import streamlit as st
import pdfplumber
from openai import OpenAI

# --- 기본 리더십 원칙 예시 ---
DEFAULT_PRINCIPLES = """
01최고 수준의 안전과 품질
Safety and Quality
우리는 안전과 품질에 있어 절대 타협하지 않습니다.
•	안전과 품질은 고객과의 첫번째 약속이기 때문이죠.
•	우리는 어떠한 선택에서도 안전을 최우선으로 고민하고,
•	최고의 안전은 최고의 품질을 통해 실현할 수 있다고 믿습니다.
•	우리에게 있어 품질은, 제품 품질은 물론 업무의 품질까지 나아갑니다.
•	우리는 모든 일하는 매 순간 디테일까지 고민하며 업무 품질을 높입니다.

02집요함
Tenacity
'적당히'로는 고객을 만족시킬 수 없습니다.
•	우리의 과제가 점점 더 복잡해지고 어려워지고 있기 때문이죠.
•	문제의 난이도가 높을수록 끝까지 핵심을 파고드는 집요함이 필요합니다.
•	집요함은 곧 책임감입니다.
•	우리는 어떤 어려운 상황에도 본질을 꿰뚫는 몰입을 통해 반드시 문제를 해결해냅니다. 
도전적 실행Challenge
새로운 내일은
오늘의 도전에서 시작된다

03
시도와 발전

Progress

수 만 번의 시도와 도전이 혁신을 만듭니다.

우리는 작은 시도를 통해 아이디어의 가능성을 확인합니다.
때로는 기대한 만큼의 결과를 이루지 못할 수도 있죠.
그럼에도 우리는 그 속에서 배움을 얻고,
과감한 도전을 위한 준비를 합니다.
가장 중요한 것은 멈추지 않고 꾸준히 앞으로 나아가는 것,
끊임없이 시도와 도전을 반복하며 발전합니다.

04민첩한 실행
Agility
불확실성의 시대에서 계획을 완벽하게 실행하기란 불가능합니다.
•	예상하지 못한 변수가 끊임없이 발생하기 때문이죠.
•	우리는 100%를 준비하기 위해 적절한 타이밍을 놓치기 보단,
•	실행 속에서 변화에 빠르게 대응하며 100%, 120%를 만들어 나갑니다.
•	선제적 준비와 민첩한 실행력을 함께 겸비할 때
•	고객에서 최고의 모빌리티 솔루션을 제공할 수 있습니다.

05협업
Alignment
자동차의 타이어를 한 방향으로 조절하는 것처럼
우리 모두는 한 방향을 바라보며 일합니다.
•	각기 다른 사람과 조직이 함께 일할 때,
•	같은 목표를 공유하고 공감대를 형성하는 것에서 부터 협업이 시작됩니다.
•	공동의 목표를 위해 어떻게 기여할 것인가 치열하게 논의하고
•	결정된 사항에 대해 최고의 시너지를 만들어가죠.
•	하나의 방향으로 함께 나아가는 것이 우리가 지향하는
•	진짜 협업의 모습입니다.

06회복탄력성
Resilience
도전에 있어 시련은 있어도 실패는 없습니다.
•	새롭고 어려운 시도일수록 한 번에 성공하기란 어렵습니다.
•	심지어 혼자 한다면 더욱 어렵겠죠.
•	실패에 좌절하지 않고 다시 일어설 수 있는 건강한 체질의
•	조직이 되기 위해, 우리는 언제나 서로 격려하고 힘을 실어줍니다.
•	그리고 함께 다시 한 번 도전합니다.

07다양성 포용

Diversity and Inclusion

다양성이 높을수록 조직의 역량이 높아지며,
새로운 아이디어와 혁신을 이끄는 원동력이 됩니다.

우리는 다양한 문화, 국가, 생각, 경험의 사람들이 모여 함께 일하고 있습니다.
서로 다를 수 있음을 인정하고 편견없이 경청합니다.
다양한 시각과 경험이 모여 새로운 관점에서 문제를 해결합니다.
서로 다름을 연결하는 과정 속에서 새로운 가치를 발견합니다.

08전문성

Expertise

기술을 모르는 비즈니스, 비즈니스를 모르는 기술은
고객을 감동시킬 수 없습니다.

우리는 각자 분야의 전문가로서 깊이 있는 지식과 실력을 쌓아 갑니다.
더 나아가 시장의 니즈, 기술과 데이터까지 함께 보며 나의 영역을 넓혀 나갑니다.
종합적 사고를 통해 더욱 발전하고 성장합니다.
나의 영역, 우리의 영역을 끊임없이 확장합니다.

09윤리준수
Integrity
우리는 사람들의 안전하고 자유로운 이동을
도와주는 일을 하고 있습니다.
•	이에 옳은 일을 한다는 자부심을 갖고, 정직하고 투명하게 일합니다.
•	우리는 우리 일의 가치를 기억하며 규정과 원칙을 철저히 지킵니다.
•	새로운 기술의 등장, 높아지는 사회적 기대에도 끊임없이 발전하며
•	옳은 일을 옳은 방식으로 해냅니다.


10데이터 기반 사고
Data-Driven Thinking
데이터 기반 사고는 미래를 선제적으로 준비하고
성공 확률을 높일 수 있는 가장 강력한 무기입니다.
•	특히 복잡하게 얽힌 글로벌 시장에서
•	변화를 미리미리 예측하고 대비하기 위해서는 데이터 활용이 필수죠.
•	우리는 과거 경험이나 직감만으로 의사결정하지 않습니다.
•	신뢰할 수 있는 데이터를 활용해
•	현상을 분석하고 인사이트를 도출, 문제를 해결합니다.

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
st.set_page_config(page_title="리더십 기반 인터뷰 가이드", layout="wide")
st.title("🚀 컬처핏 기반 인터뷰 가이드 생성기")

st.markdown(
    "핵심가치과 이력서를 기반으로, 면접관이 바로 쓸 수 있는 "
    "**항목별 인터뷰 질문 & 확인 포인트**를 자동 생성합니다."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 리더십 원칙")
    leadership_text = st.text_area(
        "회사 핵심 가치을 붙여넣으세요.",
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
