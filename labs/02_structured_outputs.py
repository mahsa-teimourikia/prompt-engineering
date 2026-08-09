from common import CaseBrief, build_case, retrieve

if __name__ == "__main__":
    response = build_case("Where is my shipment?", retrieve("shipping"))
    validated = CaseBrief.model_validate(response.model_dump())
    print(validated.model_dump_json(indent=2)); assert validated.evidence
