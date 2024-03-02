from fastapi import FastAPI
import logging
from models.bad_boys import RepositoryAnalysisInput
from models.rules_model import ValidationRules
from utils.rules_util import load_rules
from controllers.final_data_model_controller import final_data_controller
from controllers.request_controller import get_bad_behaviour_report
app = FastAPI()


# Set up logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

RULES_FOLDER_PATH = './rules'
RULES_FILE = 'Group10Rules.jsonc'
RULES: ValidationRules = None


@app.on_event("startup")
async def startup_event():
    global RULES
    RULES = load_rules(RULES_FOLDER_PATH, RULES_FILE)


@app.post("/gitbehaviors")
def analyze_repository(request: RepositoryAnalysisInput):
    # Final data model
    data = final_data_controller(request)
    # get_report
    report = get_bad_behaviour_report(data, rules=RULES)
    # return
    return report

@app.get("/test")
def test():
    log.info(RULES)