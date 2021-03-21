
.PHONY:
lint:
	-python3 -m flake8 src/; true

.PHONY:
test:
	-python3 -m pytest --disable-pytest-warnings tests/

.PHONY:
fmt:
	black spekulatio/

