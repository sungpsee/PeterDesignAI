import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(page_title="Peter Design AI", page_icon="🏥", layout="wide")

st.title("🏥 Peter Design AI")
st.caption("✅ v4 - 산돌고딕 / 고해상도 / 흰 영역 레이아웃")
st.write("강남베드로병원 홍보물 자동 생성 플랫폼")
st.divider()

title = st.text_input("포스터 제목", "난치성 뇌전증 환자\n치료 컨퍼런스")
date = st.text_input("일시", "2026년 7월 7일 (화) 오후 5시")
place = st.text_input("장소", "신관 지하2층 세미나실")
target = st.text_input("대상", "신경과, 신경외과 의료진\n신경과 간호사, 뇌파기사")
notice = st.text_input("하단 안내문구", "대상자는 필수 참석이며, 관심있는 의료진 분들의 참석을 바랍니다.")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FONT_REGULAR = BASE_DIR / "fonts" / "Pretendard-Regular.otf"
FONT_BOLD = BASE_DIR / "fonts" / "Pretendard-Bold.otf"
FONT_BLACK = BASE_DIR / "fonts" / "Pretendard-Black.otf"

def get_font(size, weight="regular"):
    font_paths = {
        "regular": FONT_REGULAR,
        "bold": FONT_BOLD,
        "black": FONT_BLACK,
    }

    font_path = font_paths.get(weight, FONT_REGULAR)
    return ImageFont.truetype(str(font_path), size)

def draw_bold_text(draw, xy, text, font, fill, stroke=4):
    x, y = xy

    for dx in range(-stroke, stroke + 1):
        for dy in range(-stroke, stroke + 1):
            if dx != 0 or dy != 0:
                draw.text(
                    (x + dx, y + dy),
                    text,
                    font=font,
                    fill=fill
                )

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )

def center_text(draw, text, y, font, fill, width, gap, bold=False):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (width - tw) / 2

        if bold:
            draw_bold_text(draw, (x, y + i * gap), line, font, fill, stroke=2)
        else:
            draw.text((x, y + i * gap), line, font=font, fill=fill)

def draw_label(draw, x, y, label, font_size):
    navy = (18, 45, 120)
    white = (255, 255, 255)

    w = int(font_size * 3.8)
    h = int(font_size * 1.9)

    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=int(font_size * 0.35),
        fill=navy
    )

    font = get_font(font_size)
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    draw_bold_text(
        draw,
        (x + (w - tw) / 2, y + (h - th) / 2 - 4),
        label,
        font,
        white,
        stroke=1
    )

def draw_info(draw, y, label, value, width, font_size, bold=False):
    label_x = int(width * 0.14)
    text_x = int(width * 0.32)

    draw_label(draw, label_x, y, label, font_size)

    font = get_font(
        int(font_size * 1.18),
        "bold" if bold else "regular"
    )

    lines = value.split("\n")
    line_gap = int(font_size * 1.65)

    for i, line in enumerate(lines):
        if bold:
            draw_bold_text(
                draw,
                (text_x, y + int(font_size * 0.18) + i * line_gap),
                line,
                font,
                (20, 20, 20),
                stroke=1
            )
        else:
            draw.text(
                (text_x, y + int(font_size * 0.18) + i * line_gap),
                line,
                font=font,
                fill=(20, 20, 20)
            )

def make_poster():
    # 여기서 2배 고해상도로 생성
    scale = 2

    bg = Image.open("poster_bg.jpg").convert("RGB")
    w, h = bg.size
    bg = bg.resize((w * scale, h * scale), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(bg)
    width, height = bg.size

    navy = (18, 45, 120)
    gray = (185, 185, 185)
    pink = (232, 202, 226)
    black = (20, 20, 20)

    # 배경 이미지 비율 기준
    header_end = int(height * 0.18)
    footer_start = int(height * 0.90)

    content_top = header_end
    content_bottom = footer_start
    content_h = content_bottom - content_top

    # 글씨 크기
    title_font = get_font(int(width * 0.078), "black")
info_font_size = int(width * 0.030)
notice_font = get_font(int(width * 0.026), "regular")

    # 위치
    title_y = content_top + int(content_h * 0.08)
    line_y = content_top + int(content_h * 0.34)
    info_y1 = content_top + int(content_h * 0.405)
    info_gap = int(content_h * 0.105)
    notice_y = content_top + int(content_h * 0.72)

    # 제목
    center_text(
        draw,
        title,
        title_y,
        title_font,
        navy,
        width,
        gap=int(width * 0.095),
        bold=True
    )

    # 구분선
    draw.line(
        (int(width * 0.08), line_y, int(width * 0.92), line_y),
        fill=gray,
        width=max(4, int(width * 0.004))
    )

    # 정보
    draw_info(draw, info_y1, "일 시", date, width, info_font_size)
    draw_info(draw, info_y1 + info_gap, "장 소", place, width, info_font_size)
    draw_info(draw, info_y1 + info_gap * 2, "대 상", target, width, info_font_size, bold=True)

    # 안내 박스
    box_x1 = int(width * 0.08)
    box_x2 = int(width * 0.92)
    box_h = int(height * 0.035)

    draw.rectangle((box_x1, notice_y, box_x2, notice_y + box_h), fill=pink)

    bbox = draw.textbbox((0, 0), notice, font=notice_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    draw.text(
        ((width - tw) / 2, notice_y + (box_h - th) / 2 - 4),
        notice,
        font=notice_font,
        fill=black
    )

    return bg

if st.button("포스터 생성하기"):
    poster = make_poster()

    st.success("포스터가 생성되었습니다!")

    preview = poster.copy()
    preview.thumbnail((900, 1300))
    st.image(preview, caption="생성된 포스터 미리보기", use_container_width=True)

    buffer = BytesIO()
    poster.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="고해상도 PNG 다운로드",
        data=buffer,
        file_name="peter_design_ai_poster.png",
        mime="image/png"
    )