from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Medicine:
    name: str
    type: str
    breakfast: float
    lunch: float
    dinner: float
    start: datetime
    end: datetime
    delay: Optional[int] = 0

    def __repr__(self):
        return(f"Medicine:\n"
               f"  Name:      {self.name}\n"
               f"  Type:      {self.type}\n"
               f"  Breakfast: {'-' if self.breakfast == 0 else self.breakfast}\n"
               f"  Lunch:     {'-' if self.lunch == 0 else self.lunch}\n"
               f"  Dinner:    {'-' if self.dinner == 0 else self.dinner}\n"
               f"  From:      {self.start.strftime('%d %B, %Y - %H:%M:%S')}\n"
               f"  To:        {self.end.strftime('%d %B, %Y - %H:%M:%S')}\n"
               f"  Delay:     {self.delay}\n"
               )

    def weekly_demand(self):
        return sum([self.breakfast, self.lunch, self.dinner])*7


@dataclass
class Therapy:
    medication_list: list[Medicine] = field(default_factory=list)

    def __repr__(self):
        return(f"Therapy:\n"
               f"{self.medication_list}")


if __name__ == "__main__":

    # kortison = Medicine("kortison 25mg", 3, )
    first_week_start = datetime(2021, 9, 21, 1)
    first_week_end = datetime(2021, 9, 27, 1)
    print(f"take med fro {first_week_start} to {first_week_end}")

    medicine1 = Medicine("aprednisol 25mg", "pills", 3, 0, 0, first_week_start, first_week_end)

    second_week_start = datetime(2021, 9, 28, 1)
    second_week_end = datetime(2021, 10, 4, 1)

    medicine2 = Medicine("aprednisol 25mg", "pills", 2.5, 0, 0, second_week_start, second_week_end)
    medicine3 = Medicine("aprednisol 25mg", "pills", 2, 0, 0, second_week_start, second_week_end)
    medicine4 = Medicine("aprednisol 25mg", "pills", 1.5, 0, 0, second_week_start, second_week_end, delay=-1)

    therapy = Therapy()
    therapy.medication_list += [medicine1, medicine2, medicine3, medicine4]

    print(therapy)

    filtered = filter(lambda medicine: (1.5 <= medicine.breakfast <= 2.5), therapy.medication_list)
    print(list(filtered))

