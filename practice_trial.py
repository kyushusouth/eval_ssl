from utils import template


def main():
    template(
        data_dir_name="data_dir_1",
        serial_number_name="serial_number_1",
        disc_title="練習試行",
        disc_remind="こちらは本番試行の前に行う練習のための実験です。",
        debug=False,
    )
    
    
if __name__ == "__main__":
    main()