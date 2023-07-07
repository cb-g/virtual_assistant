from template import template
from schedule import schedule

t = template()
t.create()

if input("Exclude preselected activities? (y/n): ").lower() == "y":
    exclude = True
else:
    exclude = False
print("\n")

s = schedule(exclude=exclude)
s.save_data()
s.schedule()
s.save_history()
