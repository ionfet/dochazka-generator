"""
Генерация книги посещаемости (Docházka) из таблицы часов (Mzdy).
"""

from dataclasses import dataclass, field

CZECH_MONTHS = {
    1: "Leden", 2: "Únor", 3: "Březen", 4: "Duben",
    5: "Květen", 6: "Červen", 7: "Červenec", 8: "Srpen",
    9: "Září", 10: "Říjen", 11: "Listopad", 12: "Prosinec",
}


class DochazkaError(Exception):
    """Ошибка с понятным сообщением для пользователя."""
    pass


@dataclass
class Summary:
    month: int
    year: int
    employees: dict[str, float] = field(default_factory=dict)

    def format_text(self) -> str:
        month_name = CZECH_MONTHS.get(self.month, str(self.month))
        total = sum(self.employees.values())
        lines = [f"{month_name} {self.year}", ""]
        for name in sorted(self.employees):
            lines.append(f"  {name}: {self.employees[name]:g} ч.")
        lines.append(f"\nВсего: {total:g} ч.")
        return "\n".join(lines)
