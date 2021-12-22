import streamlit as st
from PIL import Image

def run_about_kepler():
    st.subheader('케플러 망원경이란?')
    st.write('''케플러 우주망원경(Kepler space observatory)은 미국 항공우주국의 외계 지구형 행성 탐사용 우주망원경입니다.
    케플러 계획은 외계 행성이 어머니 항성을 돌면서 항성을 가려 항성의 밝기가 감소하는 것을 감지할 목적으로,
     NASA가 개발한 우주 광도계를 이용하여 9년 6개월 동안 약 53만개의 항성을 발견했습니다.''')
    st.subheader('케플러 망원경의 성과!')
    img = Image.open('data/image/kepler.png')
    st.image(img)