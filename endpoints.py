from agents.plateRecognizer.extractor import run_platerecognizer_alpr
from agents.ultimateALPR.extractor import run_ultimate_alpr

endpoints = dict()
# endpoints['ultimateALPR'] = run_ultimate_alpr
endpoints['plateRecognizer'] = run_platerecognizer_alpr
