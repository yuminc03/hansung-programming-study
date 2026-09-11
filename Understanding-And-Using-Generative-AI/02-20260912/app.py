"""고객 문의 자동 배정 대시보드.

01_고객문의_자동배정_토큰화_임베딩_의미공간.ipynb 의 흐름을 그대로 옮긴 Streamlit 앱이다.
문의 문장을 임베딩으로 바꾸고, FAQ 12건과 코사인 유사도를 재서 가장 비슷한 FAQ의
담당팀을 배정한다. 최고 유사도가 기준값보다 낮으면 사람에게 넘긴다.

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

# 비교 기준: FAQ 12건. 한 줄이 [질문, 답변, 담당팀]이다.
FAQ_DATA = [
    ["주문한 상품은 언제 배송되나요?", "결제 완료 후 1~2일 내 출고되며, 출고 후 송장번호가 문자로 발송됩니다.", "배송팀"],
    ["배송지 주소나 연락처를 변경하고 싶어요.", "출고 전이면 마이페이지에서 배송지·수령인 연락처를 직접 바꿀 수 있습니다.", "배송팀"],
    ["주문을 취소하고 환불받고 싶어요.", "출고 전 주문은 즉시 취소되며, 환불은 결제 수단으로 되돌려 드립니다.", "환불팀"],
    ["환불은 며칠 뒤에 입금되나요?", "카드 결제는 취소 후 3~5영업일, 계좌 환불은 2영업일 안에 입금됩니다.", "환불팀"],
    ["카드 결제가 계속 실패해요.", "한도 초과·해외결제 차단·앱카드 미인증이 주된 원인이며, 다른 카드로 재시도해 주세요.", "결제팀"],
    ["무통장 입금은 언제 확인되나요?", "입금 후 10분 안에 자동 확인되며, 입금자명이 다르면 확인이 지연될 수 있습니다.", "결제팀"],
    ["현금영수증이나 세금계산서 발급이 가능한가요?", "주문 상세에서 소득공제용 현금영수증 또는 사업자 세금계산서를 신청할 수 있습니다.", "결제팀"],
    ["비밀번호를 잊어버렸어요.", "로그인 화면의 '비밀번호 찾기'에서 휴대폰 인증 후 새 비밀번호를 설정합니다.", "회원팀"],
    ["휴대폰 번호가 바뀌어서 본인인증이 안 돼요.", "고객센터에 신분증 사본을 보내 주시면 등록된 번호를 새 번호로 바꿔 드립니다.", "회원팀"],
    ["회원 탈퇴는 어떻게 하나요?", "마이페이지 > 회원정보 > 회원 탈퇴에서 계정을 삭제할 수 있으며, 진행 중인 주문이 없어야 합니다.", "회원팀"],
    ["상품이 파손된 채로 도착했어요. 교환이나 반품이 되나요?", "수령 후 7일 안에 파손 사진을 보내 주시면 무상 교환 또는 반품 처리해 드립니다.", "CS팀"],
    ["제품 고장 시 A/S와 보증기간은 어떻게 되나요?", "구매일로부터 1년간 무상 A/S가 제공되며, 제조사 서비스센터 방문 또는 택배 접수가 가능합니다.", "CS팀"],
]

# 예시 채우기 버튼이 넣어 주는 문의 20건. 마지막 1건은 FAQ에 답이 없는 실패 사례다.
EXAMPLE_INQUIRIES = """어제 주문했는데 아직 출발도 안 했네요. 언제쯤 받을 수 있을까요?
주소를 잘못 입력했어요. 아파트 동호수 바꿀 수 있나요?
마음이 바뀌어서 주문 취소하려고요. 돈은 언제 돌려주나요?
환불 신청한 지 일주일이 지났는데 아직 입금이 안 됐어요.
결제 버튼을 누르면 오류가 나면서 승인이 안 돼요.
회사 경비 처리해야 해서 세금계산서 발행 부탁드립니다.
로그인이 안 돼요. 비밀번호 찾기는 어디서 하나요?
더 이상 이용 안 할 건데 계정 삭제하고 싶습니다.
택배 상자를 열었더니 액정이 깨져 있어요.
산 지 두 달 된 청소기가 갑자기 안 켜져요. 수리 가능한가요?
송장번호가 조회가 안 되는데 배송 중인 게 맞나요?
받는 사람 연락처를 바꾸고 싶어요.
취소했는데 환불 금액이 결제 금액보다 적게 들어왔어요.
무통장 입금했는데 주문이 미결제로 떠요.
현금영수증 소득공제용으로 받을 수 있나요?
휴대폰 번호가 바뀌어서 인증이 안 돼요.
냉장고 문이 찌그러져서 왔어요. 교환해 주세요.
제품 보증기간이 얼마나 되나요?
오늘 아침에 주문했는데 새벽배송 되나요?
채용 공고는 어디에서 볼 수 있나요?"""

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
                "고객 문의": text,
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
    st.set_page_config(page_title="고객 문의 자동 배정 대시보드", page_icon="📮", layout="wide")
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
    st.title("📮 고객 문의 자동 배정 대시보드")
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
        "고객 문의 입력 — 한 줄에 한 건씩, 여러 줄을 한 번에 붙여 넣을 수 있습니다",
        key="inquiry_text",
        height=180,
        placeholder="예) 택배가 아직 안 왔어요",
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
            "고객 문의": st.column_config.TextColumn(width="large"),
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
            file_name="고객문의_배정결과.csv",
            mime="text/csv",
            width="stretch",
        )


if __name__ == "__main__":
    main()
