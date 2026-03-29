from generator import DochazkaError, Summary


def test_dochazka_error_has_message():
    err = DochazkaError("Не нашёл лист с данными.")
    assert str(err) == "Не нашёл лист с данными."


def test_summary_fields():
    s = Summary(month=3, year=2026, employees={"Novak": 120.0, "Svoboda": 80.0})
    assert s.month == 3
    assert s.year == 2026
    assert s.employees == {"Novak": 120.0, "Svoboda": 80.0}


def test_summary_format_text():
    s = Summary(month=3, year=2026, employees={"Novak": 120.0, "Svoboda": 80.0})
    text = s.format_text()
    assert "Březen 2026" in text
    assert "Novak" in text
    assert "120" in text
    assert "Svoboda" in text
    assert "80" in text
    assert "200" in text  # total
