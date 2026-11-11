Workshop Energy Cost Estimator
What it does
This Python program helps a workshop owner see how much electricity each machine uses and what it costs. You enter each machine's name, power in watts and hours used per day, plus your local tariff. The program then calculates daily and monthly energy in kWh and the cost for each machine and for the whole workshop.
How to run it
Install Python 3, then run:
python workshop_energy_estimator.py
On Android you can paste the code into an app such as Pydroid 3 and press Run.
Sample output
Inputs used: tariff N225 per kWh, 26 working days, three machines.
WORKSHOP ENERGY COST REPORT
============================================================
Tariff: N225.00 per kWh | Working days per month: 26

Machine              Watts  Hrs/day  kWh/day  kWh/month   Cost/month
--------------------------------------------------------------------
Lathe                1,500      8.0    12.00     312.00    70,200.00
Welding Machine      4,000      6.0    24.00     624.00   140,400.00
Air Compressor       2,200      5.0    11.00     286.00    64,350.00
--------------------------------------------------------------------
TOTAL                                  47.00    1222.00   274,950.00
Daily cost: N10,575.00
Monthly cost: N274,950.00

RANKING BY MONTHLY COST (my own twist)
--------------------------------------------------------------------
1. Welding Machine: 51.1% of the bill
2. Lathe: 25.5% of the bill
3. Air Compressor: 23.4% of the bill

Biggest consumer: Welding Machine - it uses more than half of your energy bill.
Tip: using it 1 hour less per day would save about N23,400.00 per month.

Report saved to workshop_energy_report.txt
My own twist
Besides the required calculations, I added:
Cost ranking: machines are sorted from most to least expensive, with each one's percentage share of the bill.
Saving tip: the program finds the biggest consumer and shows how much money one hour less use per day would save each month.
Saved report: the full report is written to workshop_energy_report.txt so it can be kept or shared.
Input checking: the program keeps asking until the input is valid. It rejects letters, zero, negative numbers and more than 24 hours per day.
What I learned
Using try and except stops the program from crashing when someone types a letter where a number is expected.
Splitting the work into small functions (like daily_energy_kwh and energy_cost) makes the code easier to test and to read.
Author
Monsuur Kehinde Aderibigbe, ND Mechatronics Engineering, Yaba College of Technology (YabaTech).
