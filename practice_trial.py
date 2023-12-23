import streamlit as st
from st_files_connection import FilesConnection
from IPython.display import Audio
import random
import datetime

DEBUG = False


class MyAudio(Audio):
    def _repr_html_(self):
        src = """
        <audio {element_id} controls="controls" controlsList="nodownload" {autoplay}>
            <source src="{src}" type="{type}" />
            Your browser does not support the audio element.
        </audio>
        """
        return src.format(
            src=self.src_attr(),
            type=self.mimetype,
            autoplay=self.autoplay_attr(),
            element_id=self.element_id_attr(),
        )


@st.cache_data
def load_data(_conn, bucket_name, data_dir):
    data_path_list = _conn.fs.glob(f"{bucket_name}/{data_dir}/**/*.csv")
    data_path_list = random.sample(data_path_list, len(data_path_list))
    return data_path_list


def main():
    if "finished" not in st.session_state:
        st.session_state.finished = False
        
    conn = st.connection("s3", type=FilesConnection)
    bucket_name = st.secrets["bucket_name"]
    data_dir = st.secrets["data_dir_practice"]
    result_dir = st.secrets["result_dir"]
    data_path_list = load_data(conn, bucket_name, data_dir)
    label1_list = []
    label2_list = []
    label3_list = []
    label4_list = []
    label5_list = []
    ans_list = []

    for i, data_path in enumerate(data_path_list):
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

    if not st.session_state.finished and st.button("解答を終える"):
        st.session_state.finished = True
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
        conn.fs.mkdirs(f"{bucket_name}/{data_dir}/{result_dir}", exist_ok=True)
        with conn.fs.open(f"{bucket_name}/{data_dir}/{result_dir}/{formatted_time}.txt", "w") as f:
            for label1, label2, label3, label4, label5, ans in zip(label1_list, label2_list, label3_list, label4_list, label5_list, ans_list):
                f.write(f"{label1},{label2},{label3},{label4},{label5},{ans}\n")
        st.rerun()
    elif st.session_state.finished:
        st.button("解答終了", disabled=True)
        st.write("これで実験は終了です。ありがとうございました。")
        st.write("シリアルコード1は「193048」です。")
        


if __name__ == "__main__":
    main()