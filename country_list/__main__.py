try:
    from .cli import cli

    click_installed = True
except ImportError:
    click_installed = False


def main():
    if click_installed:  # pragma: no cover
        cli(prog_name="country_list")
    else:
        print("ERROR!!")
        print("click package missing")
        print("Install click by running:")
        print("  pip install click")
        print("Or by reinstalling country_list with cli")
        print("  pip install country_list[cli]")
        exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
