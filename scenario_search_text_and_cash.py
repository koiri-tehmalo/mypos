from core.config_loader import load_config
from core.app_context import AppContext
from flows.retail_flow import RetailFlow
from flows.payment_flow import PaymentFlow

def main():
    config = load_config()
    ctx = AppContext(window_title_regex=config["GLOBAL"]["WINDOW_TITLE"])

    retail = RetailFlow(config, ctx)
    payment = PaymentFlow(config, ctx)

    retail.search_by_text_and_go_payment()
    payment.pay_cash()

if __name__ == "__main__":
    main()
