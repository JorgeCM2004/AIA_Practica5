import pytest

from utils.security.F_anonymizer import anonymize_node

ANONYMIZATION_TESTS = [
	("Hi, my name is Laura and I'm pregnant.", ["Laura"]),
	("Please contact me at 600123456 if my blood tests are ready.", ["600123456"]),
	(
		"Send the medical report to maria.perez@gmail.com as soon as possible.",
		["maria.perez@gmail.com"],
	),
	(
		"Patient John Doe, age 32, phone number +34 612 345 678.",
		["John Doe", "+34 612 345 678"],
	),
	(
		"My name is Francisco García and I live in Madrid.",
		["Francisco García", "Madrid"],
	),
	("My doctor, Dr. Robert Smith, prescribed me some vitamins.", ["Robert Smith"]),
	("I checked my patient portal from the IP 192.168.1.1", ["192.168.1.1"]),
	(
		"I am pregnant. I work at Microsoft in New York. My name is Alice.",
		["Microsoft", "New York", "Alice"],
	),
	("My partner David is worried about my blood pressure of 140/90.", ["David"]),
	(
		"Email ana@urjc.es or call my husband at 9123123123.",
		["ana@urjc.es", "9123123123"],
	),
]


@pytest.mark.parametrize("original_text, secrets", ANONYMIZATION_TESTS)
def test_pii_redaction(original_text, secrets):
	safe_text = anonymize_node(original_text)

	for secret in secrets:
		assert secret not in safe_text, (
			f"Fallo de privacidad: Se filtró el dato '{secret}' en el resultado: {safe_text}"
		)


SAFE_TEXT_TESTS = [
	"I am 30 weeks pregnant and my head hurts.",
	"My blood pressure is 120/80 and my temperature is 37.5 C.",
	"I took 400mg of Ibuprofen yesterday.",
]


@pytest.mark.parametrize("text", SAFE_TEXT_TESTS)
def test_no_false_positives(text):
	safe_text = anonymize_node(text)
	assert len(safe_text) >= len(text) * 0.8, (
		f"Falso positivo: Se borró demasiado texto legítimo. Resultado: {safe_text}"
	)
