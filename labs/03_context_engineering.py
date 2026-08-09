from common import build_case, select_context

if __name__ == "__main__":
    context = select_context("Can I get a refund?", {"refund": "Refunds require order id within 30 days.", "shipping": "3-5 days.", "marketing": "Summer sale."})
    case = build_case("Can I get a refund?", context)
    print(case.model_dump_json(indent=2)); assert case.evidence == context
