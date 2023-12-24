from utils import template


def main():
    template(
        data_dir_name="data_dir_3",
        serial_number_name="serial_number_3",
        disc_title="本番試行2",
        disc_remind="こちらは本番試行2です。練習ではありません。",
        debug=False,
    )
    

if __name__ == "__main__":
    main()