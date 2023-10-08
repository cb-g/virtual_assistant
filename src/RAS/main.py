from template import template
from schedule import schedule
import os

def main():
    t = template()
    t.create()

    if input("exclude preselected activities? (y/n): ").lower() == "y":
        exclude = True
    else:
        exclude = False
    print("\n")

    s = schedule(exclude=exclude)
    s.save_data()
    os.system("clear")
    s.schedule()
    s.save_history()

if __name__ == "__main__":
    main()