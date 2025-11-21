import streamlit as st
import pdfplumber
from openai import OpenAI

# --- 기본 리더십 원칙 예시 (쿠팡) ---
DEFAULT_PRINCIPLES = """
Wow the Customer
우리는 고객의 삶을 더 좋게 변화시키기 위해 존재한다. 고객은 언제나 우리가 내리는 모든 결정의 시작과 끝이다.

Company-wide Perspective
리더는 오너처럼 생각하며 회사 전체의 이익을 최우선으로 두고 행동한다. 전체 그림을 보고 자신의 일이 전후 단계와 다른 조직에 미칠 영향까지 모두 고려하며, 자신의 조직만이 아니라 다른 조직이나 업무에 발생한 문제까지도 드러내 이슈를 제기한다. 절대 “내 일에 상관하지 마세요"라거나 “그건 내 일이 아닌데요"라는 말을 하지 않는다.

Think Systematically
리더는 피드백을 빠르게 확인할 수 있는 메커니즘을 통해 큰 규모를 감당할 수 있는 프로세스를 만든다. 단순히 결함을 고치는데 그치지 않고, 비슷한 결함이 반복되지 않도록 한다.

Disagree and Commit
좋은 의사결정 뒤에는 언제나 건설적인 의견 대립이 있다. 리더는 동의하지 않을 때 그 자리에서 공개적으로 이견을 제기하며, 인간관계에 연연하여 타협하지 않는다. 일단 결정이 내려지면 당초 의견을 지지했던 사람이나 반대했던 사람이 구분이 안 될 정도로 성공적인 결과를 위해 함께 모든 역량을 쏟는다.

Deliver Results with Grit
리더는 제때에 수준 높은 성과를 내놓는다. 야근하고 열심히 일한 것을 일의 성과와 혼동하지 않는다. 한번 시작한 일은 반드시 끝을 낸다. 강한 집념과 끈기로 주변 여건이나 환경에 얽매이지 않고 일을 추진하며, 어떤 변명으로도 도중에 포기하거나 중단하지 않는다.

Aim High and Find a Way
우리는 절충안 대신 근본적 해결책을 찾아내고, 고객의 기대를 100배 이상 뛰어넘을 때 진정한 고객감동이 이뤄진다고 믿는다. 오직 비현실적으로 보이는 목표만이 믿기지 않는 결과를 만든다. 합리적 목표는 변화를 겁내는 마음에서 태어나며, 우리의 잠재력을 갉아먹고 세상을 바꿀 기회를 빼앗는다. 진정한 리더는 변화와 혁신 없이는 이룰 수 없는 급진적이고 높은 목표를 제시해 고객을 위한 믿기지 않는 결과를 이뤄낸다.

Demand Excellence
리더는 괜찮은 정도로는 절대 만족하지 않고 오직 탁월한 수준만 인정한다. 스스로에게나 다른 사람들에게도 높은 기준을 적용하고 그 기준을 끊임없이 높여 나간다.

Hate Waste
리더는 적은 것으로 많은 것을 할 수 있는 방법을 찾는다. 단순한 비용 삭감이 아니라 근본적인 비용 절감을 수행한다. 성과나 효율에 부정적 영향을 준다면 제대로 된 비용 절감이 아니다. 푼돈 아끼려다 목돈을 쓰게 되는 어리석은 일은 하지 않는다.

Ruthless Prioritization
우리는 반드시 이겨야만 하는 단 하나의 전투를 위해 다른 전투는 포기할 줄 아는 자신감과 용기를 갖고 있다. 우리는 다각화의 위험을 경계한다. 쉽고 잘 할 수 있는 일부터 하려는 유혹에서 벗어나 어렵고 불편해도 해야만 하는 일부터 우선한다.

Dive Deep
뛰어난 운영은 디테일에 대한 열정을 가진 리더로부터 시작된다. 리더는 어딘가 이상한 부분을 발견하면 사안을 완벽하게 이해할 때까지 모든 단계를 구석구석 파고들어 파악하며 이를 통해 적절한 인재에게 권한을 주고 결과를 만들어낸다. 리더가 굳이 보지 않아도 될 사소한 일이란 없다.

Simplify
복잡함은 스케일과 속도, 고객 경험을 망치는 주범이다. 리더는 자신이 다루는 모든 일을 광적으로 간소화하는 사람이다.

Hire and Develop the Best
리더는 채용과 승진을 통해 조직 전체의 수준을 높여 나간다. 채용은 장기적 관점에서의 필요를 기준으로 한다. 최고의 인재를 알아보고 그들이 잠재력을 완전히 발휘할 수 있도록 투자하며, 내부 조직 이동을 통해 성장을 도모할 수 있도록 한다.

Influence without Authority
리더는 자신의 아이디어를 명확하게 커뮤니케이션함으로써 조직을 이끈다. 데이터와 인사이트를 근거로 사람들을 설득하고 공감대를 형성해 나간다. 지위가 아닌 지식이 권위가 되는 환경을 만든다.

Learn Voraciously
우리는 최고의 아이디어에 목이 마르며, 이런 아이디어를 얻기 위해 자존심은 내려놓고 모든 곳을 뒤진다. 우리는 실수를 합리화하지 않고 스스로를 기꺼이 비판한다.

Move with Urgency
긴박함이란 곧 위기의식이다. 진정한 리더는 항상 “위기 상황” 속에서 살아간다. 우리는 활동이 멈추면 생존의 위협을 느끼고, 계산된 위험은 기꺼이 떠안는다. 우리는 실행 속에서 배우며 비난이 두렵거나 ‘완벽한’ 정답을 찾겠다며 결정을 미루지 않는다.
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
def stream_interview_guide(leadership_text, resume_text, language):
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

        각 리더십 원칙마다 2~3개의 질문을 작성하세요.
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

각 리더십 원칙마다 2~3개의 고난도 질문을 생성하세요.


    {lang_instruction}

    {format_instruction}
    """

    user_prompt = f"""
[Leadership Principles]
{leadership_text}

[Candidate Resume]
{resume_text}
"""

    # 🔥 GPT 스트리밍 (가장 핵심 부분)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
        temperature=0.3,
    )

    # 스트림 결과 yield
    for chunk in response:
        if "content" in chunk.choices[0].delta:
            yield chunk.choices[0].delta["content"]


# --- Streamlit UI ---
st.set_page_config(page_title="리더십 원칙 기반 인터뷰 가이드", layout="wide")
st.title("📝 리더십 원칙 기반 인터뷰 가이드 생성기")

st.markdown(
    "리더십 원칙과 이력서를 기반으로 **면접관용 인터뷰 가이드**를 자동 생성합니다."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 리더십 원칙 입력")
    leadership_text = st.text_area(
        "회사의 리더십 원칙을 붙여넣으세요",
        value=DEFAULT_PRINCIPLES,
        height=300,
    )

    language = st.radio(
        "생성 언어 선택",
        ["한국어", "English"],
        index=0,
        horizontal=True,
    )

with col2:
    st.subheader("2. 이력서 업로드")
    resume_file = st.file_uploader(
        "PDF 또는 텍스트 파일 업로드",
        type=["pdf", "txt"],
    )
    if resume_file:
        st.caption(f"업로드된 파일: {resume_file.name}")

st.divider()

# 버튼 컬러 secondary → primary 로 변경
if st.button("🚀 인터뷰 가이드 생성하기", type="primary"):
    if not leadership_text.strip():
        st.error("리더십 원칙을 입력하세요.")
    elif not resume_file:
        st.error("이력서를 업로드하세요.")
    else:
        resume_text = extract_text_from_file(resume_file)
        if not resume_text.strip():
            st.error("이력서에서 텍스트를 추출하지 못했습니다.")
        else:
            st.success("생성 중… 아래에서 실시간 출력됩니다!")

            guide_placeholder = st.empty()
            full_text = ""

            # 스트리밍 시작
            for chunk in stream_interview_guide(leadership_text, resume_text, language):
                full_text += chunk
                guide_placeholder.markdown(full_text)

            # 다운로드 버튼
            st.download_button(
                "📥 인터뷰 가이드 다운로드 (MD)",
                data=full_text.encode("utf-8"),
                file_name="interview_guide.md",
                mime="text/markdown",
            )
