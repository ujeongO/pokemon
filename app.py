import streamlit as st


# 페이지 reload 체크
print("page reload")

st.title("포켓몬 도감")

type_emoji_dict = {
    "노말": "⚪",
    "격투": "✊",
    "비행": "🕊",
    "독": "☠️",
    "땅": "🌋",
    "바위": "🪨",
    "벌레": "🐛",
    "고스트": "👻",
    "강철": "🤖",
    "불꽃": "🔥",
    "물": "💧",
    "풀": "🍃",
    "전기": "⚡",
    "에스퍼": "🔮",
    "얼음": "❄️",
    "드래곤": "🐲",
    "악": "😈",
    "페어리": "🧚"
}

initial_pokemons = [
    {
        "name": "피카츄",
        "types": ["전기"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/pikachu.webp"
    },
    {
        "name": "누오",
        "types": ["물", "땅"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/nuo.webp",
    },
    {
        "name": "갸라도스",
        "types": ["물", "비행"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/garados.webp",
    },
    {
        "name": "개굴닌자",
        "types": ["물", "악"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/frogninja.webp"
    },
    {
        "name": "루카리오",
        "types": ["격투", "강철"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/lukario.webp"
    },
    {
        "name": "에이스번",
        "types": ["불꽃"],
        "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/acebun.webp"
    },
]

# 예시 데이터
example_pokemon = {
    "name": "알로라 디그다",
    "types": ["땅", "강철"],
    "image_url": "https://storage.googleapis.com/firstpenguine-coding-school/pokemons/alora_digda.webp"
}

# session_state: 페이지가 reload될 때 유지됐으면 하는 데이터 담아두는 공간 -> dictionary 와 비슷함
# session_state에 'pokemons'라는 key가 없으면(페이지 초기에)
if "pokemons" not in st.session_state:
    # (페이지 초기에) initial_pokemons 넣기
    st.session_state.pokemons = initial_pokemons
    

# toggle을 껐다 켰을 때 페이지가 reload 됨 -> 추가한 예시 데이터 사라짐
# >> session_state로 해결!
auto_complete = st.toggle("예시 데이터로 채우기")
# 입력 폼 생성
# clear_on_submit -> True: 사용자가 제출 버튼을 누른 후 양식 내부의 모든 위젯이 기본값으로 재설정됨
with st.form("form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    # name, types -> 한줄로
    with col1:
        name = st.text_input(
            label="포켓몬 이름",
            value=example_pokemon["name"] if auto_complete else ""
        )
    with col2:
        types = st.multiselect(
            label="포켓몬 속성",
            options=list(type_emoji_dict.keys()),
            max_selections=2,
            default=example_pokemon["types"] if auto_complete else []
        )
    image_url = st.text_input(
        label="포켓몬 이미지",
        value=example_pokemon["image_url"] if auto_complete else ""
    )
    submit = st.form_submit_button("Submit")
    # 제출 버튼 눌렀을 때
    if submit:
        # 예외처리
        if not name:
            st.error("포켓몬의 이름을 입력해주세요!")
        elif not types:
            st.error("포켓몬의 타입을 선택해주세요!")
        elif not image_url:
            st.error("포켓몬의 이미지 url을 입력해주세요!")
        else:
            # st.success("추가 가능!")
            # session_state.pokemons에 입력한 포켓몬 추가
            # >> 페이지가 reload 되더라도 추가한 데이터 유지됨
            st.session_state.pokemons.append({
                "name": name,
                "types": types,
                "image_url": image_url
            })
            

for i in range(0, len(st.session_state.pokemons), 3):
    row_pokemons = st.session_state.pokemons[i : i+3]
    cols = st.columns(3)
    for j in range(len(row_pokemons)):
        pokemon = row_pokemons[j]
        with cols[j]:
            # expander: 박스모양, 접었다 폈다 가능
            with st.expander(
                # **: 두껍게
                # f 스트링을 ""로 감싸면 안에는 "" 사용 불가 => ''로 사용해야 함
                label=f"**{i+j+1}. {pokemon['name']}**", 
                expanded=True
            ):
                st.image(pokemon["image_url"])
                emoji_types = [f"{type_emoji_dict[x]} {x}" for x in pokemon["types"]]
                st.text(" / ".join(emoji_types))
                # 삭제 버튼 생성
                # key: 몇 번째 데이터를 선택했는지 알려주기 위함
                # use_container_width: 칸에 맞춰 크기 조정
                delete_buttom = st.button("삭제", key=(i+j), use_container_width=True)
                if delete_buttom:
                    # key에 해당하는 데이터 제거
                    del st.session_state.pokemons[i + j]
                    # rerun: 페이지 다시 실행
                    st.rerun()







