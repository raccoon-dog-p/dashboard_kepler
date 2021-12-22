from numpy import NaN
import streamlit as st
import pandas as pd
from PIL import Image

from about_kepler import run_about_kepler
from famous import run_famous
from planet_data import run_planet_data


def main():
    menu = ['홈','케플러 망원경이란?','케플러가 발견한 유명한 행성들은?','행성 데이터']
    st.sidebar.subheader('무엇이 보고 싶나요?')
    choice = st.sidebar.selectbox('메뉴',menu)
    if choice == '홈':
        st.subheader('케플러 망원경을 통해 보는 행성 데이터!')
        st.write('외계 행성에 대하여 궁금하신적이 있으신가요?')
        st.write('이 사이트는 그동안 케플러 망원경이 발견한 데이터를 정리한 사이트입니다.')
        st.write('발견됐던 행성중 가장 뜨거운 행성은 지구에 비해 얼마나 뜨거울까요?')
        st.write('왼쪽의 메뉴를 통하여 여러분들의 궁금증을 해소해보세요!')
        img = Image.open('data/image/scope.png')
        st.image(img)
        st.write('행성과 별에 둘러싸여 있는 케플러 우주망원경 상상도. 나사 제공')
    elif choice =='케플러 망원경이란?':
       run_about_kepler()
    elif choice == '케플러가 발견한 유명한 행성들은?':
       st.sidebar.subheader('보고싶은 행성을 선택해주세요!')
       planets = ['가장 뜨거운 행성','가장 차가운 행성','슈퍼 지구','가장 큰 행성']
       choice_planets = st.sidebar.radio("",planets)
       if choice_planets == '가장 뜨거운 행성':
           run_famous('kepler_13b')
           st.write('Nasa의 kepler_13b의 상상도')
       elif choice_planets == '가장 차가운 행성':
           run_famous('kepler_1536b')
           st.write('Nasa의 kepler_1536b의 상상도') 
       elif choice_planets == '슈퍼 지구':
           run_famous('kepler_22b')
           st.write('Nasa의 kepler22_b 상상도')
           st.write('좀 더 관심 있으신 분들은 링크를 통하여 확인해보세요! https://www.youtube.com/watch?v=E73qIE5xezQ&t=747s ') 
       elif choice_planets == '가장 큰 행성':
           run_famous('kepler_470b')
           st.write('Nasa의 kepler_470b 상상도') 
    elif choice == '행성 데이터':
        st.sidebar.subheader('보고싶은 데이터를 선택해주세요')
        planet_list=['데이터 설명','데이터 프레임 변환','데이터 차트로 보기']
        select_df = st.sidebar.radio('',planet_list)
        if select_df == '데이터 설명':
            run_planet_data('describe')
        elif select_df == '데이터 프레임 변환':
            run_planet_data('frame')
        elif select_df =='데이터 차트로 보기':
            run_planet_data('chart')
if __name__ == '__main__':
    main()