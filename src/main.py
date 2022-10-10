import argparse

from src.dag_reader import DAGReader


def option_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--dag_dir",
                            required=True,
                            type=str,
                            help="path to dag directory")
    args = arg_parser.parse_args()

    return args.dag_dir


def main(dag_dir):
    dags = DAGReader.read(dag_dir, 'dot')
    pass  # TODO


if __name__ == "__main__":
    dag_dir = option_parser()
    main(dag_dir)
