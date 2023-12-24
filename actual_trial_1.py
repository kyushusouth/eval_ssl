from utils import template


def main():
    template(
        data_dir_name="data_dir_2",
        serial_number_name="serial_number_2",
        disc_title="本番試行1",
        disc_remind="こちらは本番試行1です。練習ではありません。",
        debug=False,
    )
    

if __name__ == "__main__":
    main()