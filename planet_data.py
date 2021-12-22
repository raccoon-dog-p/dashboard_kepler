from os import name
from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
def run_planet_data(target):
    # 히스토그램 함수.
    def hist_make(column):
        a= df_condition[column].hist(color='#008B8B',edgecolor= 'whitesmoke',linewidth=2.0)
        b= plt.xlabel(column, labelpad=15, weight='bold', size=12)
        c= plt.ylabel('count',labelpad=15, weight='bold', size=12)
        d= plt.title(f'{column}_hist',weight='bold',size=15)
        # 격자 제거
        e = plt.grid(False)
        return a,b,c,d,e
    def describe_make(column):
        if st.checkbox('데이터 통계보기'):
             st.dataframe(df_condition[column].describe())
    df = pd.read_csv('data/kepler.csv')
    # 1. 데이터 프레임 가공
    # 내가 쓰고 싶은 컬럼은 'kepler_name','koi_score',
    # 'koi_period','koi_prad','koi_teq','koi_slogg','koi_srad' 이다.
    df = df[['kepler_name','koi_score','koi_period','koi_prad','koi_teq','koi_srad']]
    # df.isna().sum() 을 통하여 보니 kepler_name 과 koi_score 에 
    # Nan 값을 확인하고 Nan이 들어있는 데이터는 제거함.
    df = df[df['kepler_name'].notna()]
    df = df[df['koi_score'].notna()]
    # df.isna().sum() 을 통하여 확인 => Nan 값 0
    # 1-1 컬럼명을 직관적으로 변경해줌
    df.columns=['name','confidence','period','radius','temperature','star size']
    # 1-2 데이터 프레임에 지구(earth) 정보 넣기
    earth = {'name':'earth','confidence':1,'period':365,'radius':1,'temperature':255,'star size':1}
    df = df.append(earth,ignore_index=True)
    # 1-2 숫자인 데이터 프레임 뽑아내기.
    df_num = df.iloc[:,1:]
    if target == 'describe':
        st.subheader('케플러 망원경의 데이터 프레임')
        st.dataframe(df)
        st.subheader('다음은 각 컬럼 설명입니다.')
        st.write('confidence : 관측결과의 신뢰도를 의미합니다. 0~1로 표현')
        st.write('period : 모항성을 기준으로 한 공전일수를 의미합니다. day로 표현')
        st.write('radious : 각 행성의 반지름을 의미합니다. 지구 반지름 비례값. 1=6400km')
        st.write('temperature: 행성의 평형 온도를 의미합니다. K로 표현')
        st.write('star size : 행성이 속해있는 모항성의 반지름을 의미합니다. 1 = 태양의 반지름')
        st.write('원본 데이터 : https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=koi')
    elif target == 'frame':
        st.subheader('케플러 망원경의 데이터 프레임')

        # 매 컬럼마다 min,max 뽑아서 slider 만들기가 귀찮다..
        # 함수로 만들어야겠다.
        # 다 쓰기 귀찮으니까 함수로 만들자.
        def condition_set(column):
            column_min = df[column].min()
            column_max = df[column].max()
            # double ended slider 로 받을경우 결과는 튜플로 받는다
            condition_column = st.sidebar.slider(column,column_min,column_max,value=[column_min,column_max])
            # 따라서 인덱스로 접근하여 최소값 변수와 최대값 변수를 받는다.
            # 받는김에 조건도 같이 받아버리자.
            condition = (condition_column[0] <= df[column]) & (df[column] <= condition_column[1])
            return condition
        df_condition = (df[condition_set('confidence') & condition_set('period') & condition_set('radius') & condition_set('temperature') & condition_set('star size')])
        st.subheader('단위변환')
        units=['K => C (켈빈을 섭씨로)','radius를 km로 바꾸기','star size를 km로 바꾸기']
        select_list = st.multiselect('단위 바꿔서 보기',units)
        if units[0] in select_list:
            df_condition['temperature']= df_condition['temperature'] - 231.5
        
        if units[1] in select_list:
            df_condition['radius'] = df_condition['radius'] * 6400

        if units[2] in select_list:
            df_condition['star size'] = df_condition['star size'] * 700000
        
        st.dataframe(df_condition)

        st.subheader('행성 이름으로 검색하기')
        user_input = st.text_input('이름을 넣어주세요')
        radio_choice = st.radio('어떤 데이터로 검색할까요?',['원본','수정'])
        if radio_choice == '원본':
            st.dataframe(df[(df['name'].str.lower().str.contains(user_input.lower()))])
        elif radio_choice == '수정':
            st.dataframe(df_condition[(df_condition['name'].str.lower().str.contains(user_input.lower()))])
        
        if st.checkbox('상관계수 보기'):
            st.dataframe(df_num.corr())

    elif target == 'chart':
         st.subheader("데이터 시각화")
         def condition_set(column):
            column_min = df[column].min()
            column_max = df[column].max()
            # double ended slider 로 받을경우 결과는 튜플로 받는다
            condition_column = st.sidebar.slider(column,column_min,column_max,value=[column_min,column_max])
            # 따라서 인덱스로 접근하여 최소값 변수와 최대값 변수를 받는다.
            # 받는김에 조건도 같이 받아버리자.
            condition = (condition_column[0] <= df[column]) & (df[column] <= condition_column[1])
            return condition
         df_condition = (df[condition_set('confidence') & condition_set('period') & condition_set('radius') & condition_set('temperature') & condition_set('star size')])
         if st.checkbox('데이터 프레임 보기'):
            st.dataframe(df_condition)
         choice =  st.radio('보고 싶은 컬럼을 골라주세요',df_num.columns)
        #  units=['K => C (켈빈을 섭씨로)','radius를 km로 바꾸기','star size를 km로 바꾸기']
        #  select_list = st.multiselect('단위 바꿔서 보기',units)
        #  if units[0] in select_list:
        #     df_condition['temperature']= df_condition['temperature'] - 231.5
        
        #  if units[1] in select_list:
        #     df_condition['radius'] = df_condition['radius'] * 6400

        #  if units[2] in select_list:
        #     df_condition['star size'] = df_condition['star size'] * 700000
         if choice == 'confidence':
            fig1 = plt.figure()
            hist_make('confidence')
            st.pyplot(fig1)
            describe_make('confidence')
         elif choice == 'period':
            fig2 = plt.figure()
            hist_make('period')
            st.pyplot(fig2)
            describe_make('period')
         elif  choice== 'radius':
            if st.checkbox('km로 변환'):
              df_condition['radius'] = df_condition['radius'] * 6400
            fig3 = plt.figure()
            hist_make('radius')
            st.pyplot(fig3)
            describe_make('radius')
         elif choice == 'temperature':
            if st.checkbox('섭씨로 변환'):
              df_condition['temperature']= df_condition['temperature'] - 231.5
            fig5 = plt.figure()
            hist_make('temperature')
            st.pyplot(fig5)  
            describe_make('temperature')
         elif choice == 'star size':
            if st.checkbox('km로 변환'):
              df_condition['star size'] = df_condition['star size'] * 700000
            fig4 = plt.figure()
            hist_make('star size')
            st.pyplot(fig4)
            describe_make('star size')




        # 지구와 비교하는 차트는 group_by bar! (alt_air)
         