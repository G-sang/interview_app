import streamlit as st
import pdfplumber
from openai import OpenAI

# --- 기본 리더십 원칙 예시 ---
DEFAULT_PRINCIPLES = """
핵심 가치 3.1
이 가치를 지키며 일할 때, 토스의 훌륭한 팀원(high performer)들은 더 좋은 성과를 낼 수 있고 동료의 인정을 받을 수 있습니다. 또한 이 가치를 통해 토스는 시장에서 승리할 수 있고 혁신을 지속할 수 있습니다.

Mission over Individual 개인의 목표보다 토스팀의 미션을 우선한다
토스팀원은 개인보다 소속 팀, 소속 팀보다는 토스팀의 미션 달성을 우선순위에 둔다. 토스팀에는 탁월한 동료들과 일하며 배우고, 그들의 존경을 얻고, 멋진 변화를 함께 만들고 시장을 혁신하는 일이 안정을 추구하는 것보다 중요한 사람들이 모여 있으며, 이들이 서로 같은 목표를 추구할 때 더 강력한 조직이 됨을 기억한다.

Aim Higher 더 높은 수준을 추구하라*
토스팀에서 탁월한 업무 처리의 수준은, 주어진 일을 잘 수행하는 데 그치지 않고, 업무 퀄리티와 판단력, 성과의 새로운 기준을 만들어내는 것이다. 이를 통해 주변 사람들에게 존경을 얻어내고 본인의 신뢰와 역할을 확장해 나간다. 주어진 일을 잘 수행하려면 단순히 1시간을 더 일하는 것보다, 새로운 기준을 만들 수 있어야 한다.
* 변경 전 버전: Go the Extra-mile. ‘Extra’라는 말에서 비롯한 의미 혼동을 덜고, 더 높은 수준을 추구해야 함을 직관적으로 담음.

Focus on Impact 하면 좋을 10가지보다, 임팩트를 만드는 데 집중한다
임팩트란 토스팀의 미션 관점에서 더 많은 사람들의 삶을 바꾸는 변화를 마침내 이끌어내는 것이다. 그 첫 번째 단계는, 하면 좋을 10가지 일을 하지 말아야 할 일로 규정하는 것이다. 산재한 모든 문제를 풀고 싶은 마음이 들더라도, 가장 중요한 일 한 가지를 의도적으로 정하고 집중하라. 한 번에 많은 일을 목표하는 것, 멀티태스킹, 바쁜 삶은 뿌듯함을 안겨줄 수는 있지만 임팩트를 대변하지는 못한다.

Question Every Assumption 모든 기본 가정에 근원적 물음을 제기한다
문제를 다른 관점에서 바라보고 해결하는 제일 좋은 방법은 모든 가정에 근원적인 물음을 제기하는 것이다. 이미 기본적으로 가정하고 실행 중인 안이라도, 그것을 바꾸면 어떨지 더 나은 길은 없을지 끊임없이 추구한다. 이때, 다른 레퍼런스나 유추가 창의적인 사고를 가로막지 않도록 주의한다. 토스팀 혁신의 역사는 당연한 것에 물음표를 던지면서 시작되었다.

Execution over Perfection 완벽해지려 하기보다 실행에 집중하라*
빠른 실행과 실험이 많은 회의와 완벽한 전략을 이긴다. 한 번에 완벽한 기획은 있을 수 없고, 변하지 않는 제품 전략은 없기에 완벽보다는 빠른 실행을, 논쟁보다는 실험을 우선시한다. 팀원 간 커뮤니케이션은 꼭 필요하고 중요하지만 근본적으로 고객에게 가치를 전달하지는 못한다. 고객에게 가치를 전달하는 활동은 오직 실행뿐임을 인지하여, 결국 중요한 일들을 더 빠르게 시도할 수 있는 방안을 찾고 그것을 실행하는 것이 중요하다.
* 변경 전 버전: Courage to Fail Fast. ‘실패’보다는 ‘실행’을 강조하는 방향으로 변경.

Learn Proactively 주도적으로 학습한다
업무에 관한 지식, 좋은 판단 등 회사의 정보를 주도적으로 학습하고 흡수한다. 우선 내가 무엇을 모르는지를 명확하고 객관적으로 판단한다. 내가 모르는 점을 주변에 용기 있게 드러내고 이를 채울 수단과 방법을 가리지 않고 찾는다. 동료는 가장 좋은 학습 수단이다.

Move with Urgency 신속한 속도로 움직인다
새로운 혁신은 사용자들에게 금세 최소한의 기준이 된다. 따라서 느리게 움직여 기회를 잃는 것보다 실패하더라도 신속하게 시도하는 게 언제나 낫다. 임팩트가 클 것으로 예상될수록 더 빠르게 실험해 본다. 팀원들은 서로가 속도감을 높이는데 필요한 일들을 받쳐주면서, 팀 전체가 신속한 업무 리듬을 유지하고 강화해 나가는 것을 지향한다.

Ask for Feedback 피드백을 자주 구하라*
관리와 지시가 없는 토스팀에서, 더 높은 퀄리티의 결과를 만들어 낼 수 있도록 도움을 주는 건 동료의 솔직한 피드백이다. 한편 솔직한 피드백을 구하는 건 용기가 필요하다. 그 불편함을 피하지 않고 더 많이, 자주 피드백을 구해야 성장할 수 있다. 업무뿐 아니라 모든 영역에 걸친 피드백을 주기적으로 요청하고 그 피드백에 대해 진정으로 받아들이는 태도를 가진다. 피드백을 주는 사람은 동료가 진정으로 성장하길 바라는 마음을 가지고, 이를 기반으로 잘하는 점을 비롯하여 더 잘할 점까지도 솔직하게 이야기한다.
* 변경 전 버전: Radical Candor. 피드백을 주는 사람의 ‘솔직함’보다 피드백을 구하는 사람의 ‘요청’이 보다 활발하고 투명한 피드백 문화에 기여하는 것을 발견. 
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
