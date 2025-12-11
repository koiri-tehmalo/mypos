from core.config_loader import load_config
from core.app_context import AppContext
from flows.return_flow import ReturnFlow

def main():
    config = load_config()
    ctx = AppContext(window_title_regex=config["GLOBAL"]["WINDOW_TITLE"])

    ret = ReturnFlow(config, ctx)
    ret.process_all()

if __name__ == "__main__":
    main()
