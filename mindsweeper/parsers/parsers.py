import click

@click.group()
def main():
    pass

@main.command()
def run_parser(parser, data):
    print('got here')

if __name__ == '__main__':
    main()