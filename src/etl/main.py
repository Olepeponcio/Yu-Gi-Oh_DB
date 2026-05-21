from src.etl.cli import build_parser
from src.etl.pipeline import run_pipeline


def main():
    args = build_parser().parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()
