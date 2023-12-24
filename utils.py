import streamlit as st
from IPython.display import Audio
import datetime


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
    return data_path_list


def finish(
    conn,
    bucket_name,
    data_dir,
    result_dir,
    label1_list,
    label2_list,
    label3_list,
    label4_list,
    label5_list,
    ans_nat_list,
    ans_int_list,
    ans_dic_list,
):
    st.session_state.finished = True
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    conn.fs.mkdirs(f"{bucket_name}/{data_dir}/{result_dir}", exist_ok=True)
    with conn.fs.open(f"{bucket_name}/{data_dir}/{result_dir}/{formatted_time}.txt", "w") as f:
        for label1, label2, label3, label4, label5, ans_nat, ans_int, ans_dic in zip(
            label1_list, label2_list, label3_list, label4_list, label5_list, ans_nat_list, ans_int_list, ans_dic_list
        ):
            f.write(f"{label1},{label2},{label3},{label4},{label5},{ans_nat},{ans_int},{ans_dic}\n")