import streamlit as st
from st_files_connection import FilesConnection
import random
import functools
from utils import MyAudio, load_data, finish

DEBUG = False


def main():
    conn = st.connection("s3", type=FilesConnection)
    bucket_name = st.secrets["bucket_name"]
    data_dir = st.secrets["data_dir_2"]
    result_dir = st.secrets["result_dir"]
    serial_number = st.secrets["serial_number_2"]
    
    if not "finished" in st.session_state:
        st.session_state.finished = False
        
    if st.session_state.finished:
        st.write("これで実験は終了です。ありがとうございました。")
        st.write(f"シリアル番号2は{serial_number}です。")
        st.stop()
    
    data_path_list = load_data(conn, bucket_name, data_dir)
    if not "data_path_list" in st.session_state:
        st.session_state.data_path_list = random.sample(data_path_list, len(data_path_list))
    
    st.markdown(
        """
        # 音声評価実験
        ## 本番試行1
        
        この度は実験にご協力いただき、誠にありがとうございます。
        
        **こちらは本番試行1です。**
        
        以下、実験内容の説明になりますので、ご確認の程よろしくお願い致します。
        
        ### 行っていただく内容
        1. 音声サンプルの視聴
        2. 音声の自然性、明瞭性について5段階で評価
        
        ### 評価項目
        ここで、評価項目である**自然性**・**明瞭性**は以下のような観点です。
        - **自然性**：音声がどれくらい自然なものになっているか
        - **明瞭性**：音声がどれくらい聞き取りやすいものになっているか
        
        ### 評価方法
        自然性・明瞭性それぞれの観点で5段階評価をお願いします。
        
        5段階評価における目安は以下の通りです。
        1. **非常に悪い**
        2. **悪い**
        3. **普通**
        4. **良い**
        5. **非常に良い**
        
        ### 解答における注意事項
        - 個人の能力を測るものではないため、直感的な解答をお願いします。
        - 各音声サンプルは、何度聞き直していただいても構いません。
        - 解答提出までは、何度解答を変更していただいても構いません。
        - **ページの再読み込みを行いますと問題が並び替えられ、解答は初期化されます。解答開始から提出までは、ページを再読み込みされないようご注意ください。**
        
        ### 解答提出
        1. 全ての解答が終わりましたら、ページ下部の「解答を終える」ボタンをクリックしてください。
        2. シリアル番号が表示されますので、記録をお願いします。
        3. 記録したシリアル番号を、クラウドワークスにて提出してください。
        
        それでは、よろしくお願い致します。
        """
    )
    st.divider()
    
    label1_list = []
    label2_list = []
    label3_list = []
    label4_list = []
    label5_list = []
    ans_list = []
    
    with st.form("evaluation"):
        for i, data_path in enumerate(st.session_state.data_path_list):
            df = conn.read(data_path)
            wav = df["wav"].values
            data_path = data_path.split("/")
            label1 = data_path[-5]
            label2 = data_path[-4]
            label3 = data_path[-3]
            label4 = data_path[-2]
            label5 = data_path[-1]
            st.write(MyAudio(wav, rate=16000))
            ans = st.radio(
                label=f"{label1}_{label2}_{label3}_{label4}_{label5}",
                options=("1:非常に悪い", "2:悪い", "3:普通", "4:良い", "5:非常に良い"),
                key=f"{i}",
                horizontal=True,
                label_visibility="visible" if DEBUG else "collapsed",
                index=None,
            )
            label1_list.append(label1)
            label2_list.append(label2)
            label3_list.append(label3)
            label4_list.append(label4)
            label5_list.append(label5)
            ans_list.append(ans)
            st.divider()
        st.form_submit_button(
            '解答を終える',
            on_click=functools.partial(
                finish,
                conn=conn,
                bucket_name=bucket_name,
                data_dir=data_dir,
                result_dir=result_dir,
                label1_list=label1_list,
                label2_list=label2_list,
                label3_list=label3_list,
                label4_list=label4_list,
                label5_list=label5_list,
                ans_list=ans_list,
            )
        )
        


if __name__ == "__main__":
    main()