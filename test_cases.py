from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

def test_dh11_voltage():
    assert query_and_validate(
        question=" how many volts does the DH11 sensor require to run?",
        expected_response="The DHT11 sensor requires a minimum of 3V and can work up to 5.5V. Therefore, it typically operates at 5V.",
    )

def test_ultrasonic_detection_angle():
    assert query_and_validate(
        question="What is the detection angle of the ultrasonic sensor",
        expected_response="30°",
    )

def test_ultrasonic_voltage():
    assert query_and_validate(
        question="What is the voltage of the ultrasonic sensor",
        expected_response="5V",
    )

def test_ultrasonic_current():
    assert query_and_validate(
        question="What is the current of the ultrasonic sensor",
        expected_response="15mA",
    )

def test_ultrasonic_range():
    assert query_and_validate(
        question="What is the range of the ultrasonic sensor",
        expected_response="1.2 in – 13 ft(3 cm – 4 m) Ultrasonic",
    )

def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )