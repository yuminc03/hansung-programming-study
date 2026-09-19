"""사내 IT 헬프데스크 문의 자동 배정 대시보드.

01_고객문의_자동배정_토큰화_임베딩_의미공간.ipynb 의 흐름을 그대로 옮긴 Streamlit 앱이다.
문의 문장을 임베딩으로 바꾸고, FAQ 12건과 코사인 유사도를 재서 가장 비슷한 FAQ의
담당팀을 배정한다. 최고 유사도가 기준값보다 낮으면 사람에게 넘긴다.

FAQ 표만 바꾸면 다른 업무에도 그대로 쓸 수 있다. 지금은 사내 IT 헬프데스크용이다.

실행: streamlit run app.py
"""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------------------------
# 1. 상수 — 노트북과 동일한 설정
# ----------------------------------------------------------------------------

MODEL_NAME = "BAAI/bge-m3"      # 노트북과 같은 다국어 임베딩 모델 (1,024차원)
DEFAULT_THRESHOLD = 0.55        # 기준값. 이보다 낮으면 사람이 확인한다
UNASSIGNED = "담당자 확인"       # 기준값 미만일 때 표시할 값
TOP_K = 3                       # 문의 1건당 보여 줄 유사 FAQ 개수

# 비교 기준: 사내 IT 헬프데스크 FAQ 12건. 한 줄이 [질문, 답변, 담당팀]이다.
FAQ_DATA = [
    ["사내 시스템 비밀번호를 잊어버렸어요.", "포털 로그인 화면의 '비밀번호 재설정'에서 사번과 휴대폰 인증을 거쳐 새 비밀번호를 설정합니다.", "계정관리팀"],
    ["신규 입사자 계정을 만들어 주세요.", "부서장 승인 후 인사 시스템에 등록되면 다음 영업일에 사번 계정과 사내 메일 주소가 발급됩니다.", "계정관리팀"],
    ["공유 폴더에 들어가면 권한이 없다고 나옵니다.", "그룹웨어 > 권한 신청에서 대상 폴더와 사유를 적어 올리면 데이터 담당자 승인 후 권한이 부여됩니다.", "계정관리팀"],
    ["사무실 와이파이가 자꾸 끊깁니다.", "회의실 구간은 접속 인원이 많을 때 불안정합니다. 유선 포트 사용을 권하며, 반복되면 AP 점검을 접수합니다.", "네트워크팀"],
    ["재택근무 중인데 VPN 연결이 안 됩니다.", "VPN 클라이언트가 최신 버전인지, OTP 시각이 맞는지 확인해 주세요. 그래도 안 되면 접속 로그를 확인해 드립니다.", "네트워크팀"],
    ["노트북이 갑자기 켜지지 않습니다.", "전원 어댑터와 배터리 상태를 먼저 확인하고, 증상이 계속되면 대여 장비를 드린 뒤 입고 수리합니다.", "PC지원팀"],
    ["프린터에서 인쇄가 되지 않습니다.", "대기 문서를 모두 지우고 드라이버를 다시 설치하면 대부분 해결되며, 토너 부족은 자동으로 교체 신청됩니다.", "PC지원팀"],
    ["모니터나 키보드 같은 주변기기를 받고 싶습니다.", "자산 신청 시스템에서 품목을 고르고 부서장 승인을 받으면 재고 확인 후 지급됩니다.", "PC지원팀"],
    ["출처가 의심스러운 메일을 받았습니다.", "첨부파일과 링크를 열지 말고 메일 상단의 신고 버튼을 눌러 주세요. 분석 후 차단 여부를 회신합니다.", "보안팀"],
    ["USB로 자료를 옮기려는데 차단됩니다.", "외부 저장매체는 기본 차단이며, 반출 승인 절차를 거치면 지정된 기간 동안만 허용됩니다.", "보안팀"],
    ["사내 메일함 용량이 가득 찼습니다.", "오래된 메일을 보관함으로 옮기거나 용량 증설을 신청하면 반영까지 약 10분이 걸립니다.", "협업도구팀"],
    ["화상회의에서 소리나 화면이 나오지 않습니다.", "회의 앱의 장치 설정에서 마이크와 카메라를 다시 선택하고, 사내망에서는 유선 연결을 권장합니다.", "협업도구팀"],
]

# 예시 채우기 버튼이 넣어 주는 문의 20건. 마지막 1건은 FAQ에 답이 없는 실패 사례다.
EXAMPLE_INQUIRIES = """포털에 로그인하려는데 암호가 기억이 안 나요.
이번에 입사한 신입사원 계정 좀 만들어 주세요.
공유 드라이브에 들어가면 접근 거부라고 뜹니다.
회의실에서 인터넷이 자꾸 끊어져요.
집에서 일하는데 VPN이 연결되지 않습니다.
노트북 전원 버튼을 눌러도 아무 반응이 없어요.
출력 버튼을 눌러도 프린터가 조용합니다.
듀얼 모니터로 쓰게 한 대 더 신청하고 싶습니다.
모르는 사람한테 첨부파일 있는 메일이 왔는데 열어도 되나요?
외장하드에 파일 복사가 막혀 있어요.
메일 용량이 초과됐다고 더 이상 수신이 안 됩니다.
화상회의에 들어갔는데 상대방 소리가 안 들려요.
사번 계정이 잠겨서 로그인이 안 됩니다.
키보드에 안 눌리는 자판이 몇 개 있어요.
랜섬웨어 의심 팝업이 계속 뜹니다.
퇴사자 계정은 언제 삭제되나요?
프린터 토너가 다 떨어진 것 같습니다.
사무실 유선 랜이 연결되지 않아요.
회사 메일을 휴대폰에서도 보고 싶습니다.
구내식당 이번 주 메뉴는 어디서 보나요?"""

COLOR_PASS = "#2E86DE"   # 기준값 이상 — 파랑
COLOR_FAIL = "#C0392B"   # 기준값 미만 — 빨강


# ----------------------------------------------------------------------------
# 2. 자원 로딩 — 무거운 것은 캐시로 한 번만
# ----------------------------------------------------------------------------


def get_faq() -> pd.DataFrame:
    """FAQ 표를 만든다. 모델이 필요 없으므로 캐시 없이 즉시 반환한다."""
    return pd.DataFrame(FAQ_DATA, columns=["faq_질문", "faq_답변", "담당팀"])


@st.cache_resource(show_spinner="임베딩 모델을 불러오는 중입니다. 처음 한 번만 걸립니다.")
def load_model_and_faq_vectors():
    """임베딩 모델과 FAQ 12건의 벡터를 함께 만들어 캐시한다.

    Streamlit은 위젯을 건드릴 때마다 스크립트 전체를 다시 실행한다.
    st.cache_resource 가 없으면 슬라이더를 한 칸 움직일 때마다 모델을 다시 읽는다.
    FAQ는 고정이므로 그 벡터도 여기서 한 번만 계산한다.
    """
    model = SentenceTransformer(MODEL_NAME, device="cpu")
    faq_vectors = model.encode(get_faq()["faq_질문"].tolist())
    return model, faq_vectors


@st.cache_data(show_spinner=False)
def embed_inquiries(texts: tuple) -> np.ndarray:
    """문의 문장들을 한 번에 임베딩한다. 같은 입력이면 다시 계산하지 않는다.

    입력을 튜플로 받는 이유는 캐시 키로 쓰려면 값이 바뀌지 않아야 하기 때문이다.
    덕분에 기준값 슬라이더만 움직일 때는 임베딩이 재사용된다.
    """
    model, _ = load_model_and_faq_vectors()
    return model.encode(list(texts))


# ----------------------------------------------------------------------------
# 3. 배정 로직 — 화면과 분리된 순수 계산
# ----------------------------------------------------------------------------


def parse_inquiries(raw: str) -> list:
    """여러 줄 입력을 문의 목록으로 바꾼다. 앞뒤 공백을 없애고 빈 줄은 버린다."""
    return [line.strip() for line in raw.splitlines() if line.strip()]


def assign_teams(inquiries: list, faq: pd.DataFrame, threshold: float):
    """문의마다 가장 비슷한 FAQ 3개를 찾고 담당팀을 배정한다.

    노트북과 계산은 같고, argmax()로 1등만 고르는 대신 정렬해서 상위 3개를 남긴다.
    반환값은 (결과표, 상위 K개 표) 두 가지이며, 상위 K개 표는 아래쪽 막대그래프가 쓴다.
    """
    _, faq_vectors = load_model_and_faq_vectors()
    inquiry_vectors = embed_inquiries(tuple(inquiries))

    # 문의 N건 × FAQ 12건 유사도 행렬
    similarity = cosine_similarity(inquiry_vectors, faq_vectors)
    # 행마다 점수가 높은 순으로 정렬해 상위 K개의 위치만 남긴다
    ranking = np.argsort(-similarity, axis=1)[:, :TOP_K]

    rows, tops = [], []
    for i, text in enumerate(inquiries):
        positions = ranking[i]
        scores = similarity[i][positions]
        best, best_score = int(positions[0]), float(scores[0])

        # 1등 점수가 기준값에 못 미치면 담당팀을 정하지 않고 사람에게 넘긴다
        team = faq.loc[best, "담당팀"] if best_score >= threshold else UNASSIGNED
        rows.append(
            {
                "번호": f"Q{i + 1}",
                "문의 내용": text,
                "배정 담당팀": team,
                "유사도": round(best_score, 2),
                "가장 비슷한 FAQ": f"F{best + 1}. {faq.loc[best, 'faq_질문']}",
            }
        )
        for rank, (position, score) in enumerate(zip(positions, scores), start=1):
            tops.append(
                {
                    "문의_번호": i,
                    "순위": rank,
                    "faq": f"F{int(position) + 1}. {faq.loc[int(position), 'faq_질문']}",
                    "담당팀": faq.loc[int(position), "담당팀"],
                    "점수": float(score),
                }
            )

    return pd.DataFrame(rows), pd.DataFrame(tops)


def style_result(result: pd.DataFrame):
    """'담당자 확인' 행의 글자를 빨간색 굵게 바꾼다."""

    def paint(row):
        if row["배정 담당팀"] == UNASSIGNED:
            return [f"color: {COLOR_FAIL}; font-weight: 700"] * len(row)
        return [""] * len(row)

    return result.style.apply(paint, axis=1)


def build_top_chart(top_table: pd.DataFrame, inquiry_index: int, threshold: float):
    """고른 문의 1건에 대해 상위 3개 FAQ를 가로 막대로 그린다."""
    picked = top_table[top_table["문의_번호"] == inquiry_index].copy()
    picked["판정"] = np.where(picked["점수"] >= threshold, "기준값 이상", "기준값 미만")
    # 축 라벨이 너무 길면 잘라 준다
    picked["라벨"] = picked["faq"].str.slice(0, 34)
    order = picked["라벨"].tolist()

    base = alt.Chart(picked)
    bars = base.mark_bar().encode(
        x=alt.X("점수:Q", title="코사인 유사도", scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("라벨:N", title=None, sort=order),
        color=alt.Color(
            "판정:N",
            title="판정",
            scale=alt.Scale(
                domain=["기준값 이상", "기준값 미만"],
                range=[COLOR_PASS, COLOR_FAIL],
            ),
        ),
        tooltip=[
            alt.Tooltip("순위:Q", title="순위"),
            alt.Tooltip("faq:N", title="FAQ"),
            alt.Tooltip("담당팀:N", title="담당팀"),
            alt.Tooltip("점수:Q", title="유사도", format=".3f"),
        ],
    )
    labels = base.mark_text(align="left", dx=4, fontSize=12).encode(
        x=alt.X("점수:Q"),
        y=alt.Y("라벨:N", sort=order),
        text=alt.Text("점수:Q", format=".2f"),
    )
    rule = (
        alt.Chart(pd.DataFrame({"기준값": [threshold]}))
        .mark_rule(color=COLOR_FAIL, strokeDash=[6, 4], size=2)
        .encode(x=alt.X("기준값:Q"))
    )
    return (bars + labels + rule).properties(height=160)


# ----------------------------------------------------------------------------
# 4. 화면
# ----------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="사내 IT 헬프데스크 문의 배정", page_icon="🛠️", layout="wide")
    faq = get_faq()

    # --- 왼쪽 사이드바: 기준값 슬라이더와 FAQ 12건 --------------------------
    with st.sidebar:
        st.header("설정")
        threshold = st.slider(
            "기준값 (코사인 유사도)",
            min_value=0.30,
            max_value=0.90,
            value=DEFAULT_THRESHOLD,
            step=0.01,
            help="가장 비슷한 FAQ의 유사도가 이 값보다 낮으면 담당팀을 정하지 않고 '담당자 확인'으로 넘깁니다.",
        )
        st.caption(f"현재 기준값 **{threshold:.2f}** 미만은 '{UNASSIGNED}'으로 표시됩니다.")

        st.header("기준 자료 · FAQ 12건")
        faq_view = faq.copy()
        faq_view.insert(0, "번호", [f"F{i + 1}" for i in range(len(faq_view))])
        st.dataframe(
            faq_view[["번호", "faq_질문", "담당팀"]],
            hide_index=True,
            width="stretch",
        )
        with st.expander("FAQ 답변까지 보기"):
            for i, row in faq.iterrows():
                st.markdown(f"**F{i + 1}. {row['faq_질문']}** · `{row['담당팀']}`")
                st.caption(row["faq_답변"])

    # --- 맨 위: 문의 입력창과 배정 실행 버튼 --------------------------------
    st.title("🛠️ 사내 IT 헬프데스크 문의 배정 대시보드")
    st.caption(
        "문의 문장을 임베딩으로 바꾸고 FAQ 12건과 코사인 유사도를 재서 담당팀을 정합니다. "
        "확신이 낮은 판단은 사람에게 넘깁니다."
    )

    if "inquiry_text" not in st.session_state:
        st.session_state["inquiry_text"] = ""

    def fill_example() -> None:
        st.session_state["inquiry_text"] = EXAMPLE_INQUIRIES

    def clear_input() -> None:
        st.session_state["inquiry_text"] = ""
        st.session_state.pop("inquiries", None)

    st.text_area(
        "문의 입력 — 한 줄에 한 건씩, 여러 줄을 한 번에 붙여 넣을 수 있습니다",
        key="inquiry_text",
        height=180,
        placeholder="예) 노트북이 안 켜져요",
    )

    col_run, col_example, col_clear, _ = st.columns([1, 1, 1, 5])
    run = col_run.button("배정 실행", type="primary", width="stretch")
    col_example.button("예시 20건 채우기", on_click=fill_example, width="stretch")
    col_clear.button("지우기", on_click=clear_input, width="stretch")

    if run:
        st.session_state["inquiries"] = parse_inquiries(st.session_state["inquiry_text"])

    inquiries = st.session_state.get("inquiries", [])

    # --- 입력이 비어 있으면 안내만 하고 멈춘다 -------------------------------
    if not inquiries:
        st.info(
            "문의를 한 줄 이상 입력한 뒤 **배정 실행**을 눌러 주세요. "
            "처음 실행할 때는 임베딩 모델을 불러오느라 시간이 걸립니다."
        )
        st.stop()

    # --- 가운데: 배정 결과표 -----------------------------------------------
    result, top_table = assign_teams(inquiries, faq, threshold)

    st.subheader(f"배정 결과 · {len(result)}건")
    st.dataframe(
        style_result(result),
        hide_index=True,
        width="stretch",
        column_config={
            "유사도": st.column_config.NumberColumn(format="%.2f", width="small"),
            "문의 내용": st.column_config.TextColumn(width="large"),
            "가장 비슷한 FAQ": st.column_config.TextColumn(width="large"),
        },
    )

    checked = int((result["배정 담당팀"] == UNASSIGNED).sum())
    if checked:
        st.warning(
            f"{checked}건은 가장 비슷한 FAQ의 유사도가 기준값 {threshold:.2f}에 못 미쳐 "
            f"'{UNASSIGNED}'으로 넘겼습니다."
        )
    else:
        st.success(f"{len(result)}건 모두 기준값 {threshold:.2f} 이상으로 자동 배정됐습니다.")

    # --- 아래: 문의 하나를 고르면 상위 3개 FAQ를 가로 막대로 ----------------
    st.subheader("판단 근거 보기")
    st.caption("1등과 2등의 점수 차이가 작으면 배정이 아슬아슬했다는 뜻입니다.")

    picked = st.selectbox(
        "문의 선택",
        options=list(range(len(inquiries))),
        format_func=lambda i: f"Q{i + 1}. {inquiries[i]}",
    )
    st.altair_chart(build_top_chart(top_table, picked, threshold), width="stretch")

    # --- 맨 아래: 팀별 건수와 CSV 다운로드 ----------------------------------
    left, right = st.columns([1, 1])
    with left:
        st.subheader("팀별 배정 건수")
        counts = result["배정 담당팀"].value_counts().rename("건수").to_frame()
        counts.index.name = "배정 담당팀"
        st.dataframe(counts.reset_index(), hide_index=True, width="stretch")
    with right:
        st.subheader("결과 내려받기")
        st.caption("엑셀에서 한글이 깨지지 않도록 UTF-8 BOM으로 저장합니다.")
        st.download_button(
            "결과 CSV 다운로드",
            data=result.to_csv(index=False).encode("utf-8-sig"),
            file_name="IT헬프데스크_배정결과.csv",
            mime="text/csv",
            width="stretch",
        )


if __name__ == "__main__":
    main()
