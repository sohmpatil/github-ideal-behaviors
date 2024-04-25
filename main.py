from fastapi import FastAPI
import logging
from models.repository_io_model import RepositoryAnalysisInput, RepositoryAnalysisIndividualInput
from models.rules_model import ValidationRules
from utils.rules_util import load_rules
from controllers.collaborator_data_model_controller import collaborator_data_controller, collaborator_individual_data_controller
from controllers.request_controller import get_bad_behaviour_report, get_bad_behaviour_report_verbose, get_bad_behaviour_report_individual
app = FastAPI()


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

RULES_FOLDER_PATH = './rules'
RULES_FILE = 'Group10Rules.jsonc'
RULES: ValidationRules = None


@app.on_event("startup")
async def startup_event():
    """
    Load validation rules at application startup.
    """
    global RULES
    RULES = load_rules(RULES_FOLDER_PATH, RULES_FILE)


@app.post("/gitbehaviors")
def analyze_repository(request: RepositoryAnalysisInput):
    """
    Analyze repository behavior based on input data.

    Parameters:
    - request (RepositoryAnalysisInput): The input data for repository analysis.

    Returns:
    - report: A report on the repository's behavior.
    """
    data = collaborator_data_controller(request)
    report = get_bad_behaviour_report(data, rules=RULES)
    return report


@app.post("/gitbehaviorsverbose")
def analyze_repository(request: RepositoryAnalysisInput):
    """
    Analyze repository behavior with verbose output based on input data.

    Parameters:
    - request (RepositoryAnalysisInput): The input data for repository analysis.

    Returns:
    - report: A detailed report on the repository's behavior.
    """
    data = collaborator_data_controller(request)
    report = get_bad_behaviour_report_verbose(data, rules=RULES)
    return report


@app.post("/gitbehaviorsindividual")
def analyze_repository(request: RepositoryAnalysisIndividualInput):
    """
    Analyze individual collaborator behavior based on input data.

    Parameters:
    - request (RepositoryAnalysisIndividualInput): The input data for individual collaborator analysis.

    Returns:
    - report: A report on the individual collaborator's behavior.
    """
    data = collaborator_individual_data_controller(request)
    report = get_bad_behaviour_report_individual(data, rules=RULES)
    return report


@app.get("/test")
def test():
    """
    A test endpoint to log the loaded validation rules.
    """
    log.info(RULES)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
