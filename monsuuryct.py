

# ---------- Input helpers (each one keeps asking until the input is valid) ----------

def get_positive_float(prompt, maximum=None):
    """Ask for a number greater than 0 (and not above maximum, if given)."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)  # convert text to a decimal number
        except ValueError:
            print("  Please type a number, for example 1500 or 2.5.")
            continue
        if value <= 0:
            print("  The number must be greater than zero.")
        elif maximum is not None and value > maximum:
            print(f"  The number cannot be more than {maximum}.")
        else:
            return value


def get_positive_int(prompt, minimum, maximum):
    """Ask for a whole number between minimum and maximum."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)  # convert text to a whole number
        except ValueError:
            print("  Please type a whole number, for example 5.")
            continue
        if value < minimum or value > maximum:
            print(f"  Enter a number from {minimum} to {maximum}.")
        else:
            return value


def get_name(prompt):
    """Ask for a machine name; it cannot be empty."""
    while True:
        name = input(prompt).strip()
        if name:
            return name
        print("  The name cannot be empty.")


# ---------- Calculation functions ----------

def daily_energy_kwh(power_watts, hours_per_day):
    """Return energy used per day in kWh: (watts x hours) / 1000."""
    return power_watts * hours_per_day / 1000


def energy_cost(energy_kwh, tariff):
    """Return the cost of the given energy at the tariff (cost per kWh)."""
    return energy_kwh * tariff


def usage_message(share):
    """Return a message describing how much one machine dominates the bill."""
    if share > 50:
        return "uses more than half of your energy bill"
    elif share > 30:
        return "is a major part of your energy bill"
    else:
        return "is spread fairly evenly with your other machines"


# ---------- Report building ----------

def build_report(machines, tariff, days, currency):
    """Build the full report as a list of text lines and return it."""
    lines = []
    lines.append("WORKSHOP ENERGY COST REPORT")
    lines.append("=" * 60)
    lines.append(f"Tariff: {currency}{tariff:,.2f} per kWh | Working days per month: {days}")
    lines.append("")
    lines.append(f"{'Machine':<18}{'Watts':>8}{'Hrs/day':>9}{'kWh/day':>9}{'kWh/month':>11}{'Cost/month':>13}")
    lines.append("-" * 68)

    total_daily_kwh = 0
    total_monthly_kwh = 0
    total_monthly_cost = 0

    # Loop through every machine and add up the totals
    for m in machines:
        total_daily_kwh += m["daily_kwh"]
        total_monthly_kwh += m["monthly_kwh"]
        total_monthly_cost += m["monthly_cost"]
        lines.append(
            f"{m['name'][:17]:<18}{m['watts']:>8,.0f}{m['hours']:>9.1f}"
            f"{m['daily_kwh']:>9.2f}{m['monthly_kwh']:>11.2f}{m['monthly_cost']:>13,.2f}"
        )

    lines.append("-" * 68)
    lines.append(f"{'TOTAL':<18}{'':>8}{'':>9}{total_daily_kwh:>9.2f}{total_monthly_kwh:>11.2f}{total_monthly_cost:>13,.2f}")
    lines.append(f"Daily cost: {currency}{energy_cost(total_daily_kwh, tariff):,.2f}")
    lines.append(f"Monthly cost: {currency}{total_monthly_cost:,.2f}")

    # ----- My own twist: ranking, cost share and saving tip -----
    ranked = sorted(machines, key=lambda m: m["monthly_cost"], reverse=True)
    lines.append("")
    lines.append("RANKING BY MONTHLY COST (my own twist)")
    lines.append("-" * 68)
    for position, m in enumerate(ranked, start=1):
        share = m["monthly_cost"] / total_monthly_cost * 100
        lines.append(f"{position}. {m['name']}: {share:.1f}% of the bill")

    top = ranked[0]
    top_share = top["monthly_cost"] / total_monthly_cost * 100
    one_hour_saving = energy_cost(daily_energy_kwh(top["watts"], 1), tariff) * days
    lines.append("")
    lines.append(f"Biggest consumer: {top['name']} - it {usage_message(top_share)}.")
    lines.append(
        f"Tip: using it 1 hour less per day would save about "
        f"{currency}{one_hour_saving:,.2f} per month."
    )
    return lines


# ---------- Main program ----------

def main():
    print("=== Workshop Energy Cost Estimator ===\n")

    currency = input("Currency symbol (press Enter for N): ").strip() or "N"
    tariff = get_positive_float(f"Your tariff ({currency} per kWh): ")
    days = get_positive_int("Working days per month (1-31): ", 1, 31)
    count = get_positive_int("How many machines do you want to enter? (1-20): ", 1, 20)

    machines = []  # list that stores one dictionary per machine

    for number in range(1, count + 1):
        print(f"\nMachine {number} of {count}")
        name = get_name("  Name: ")
        watts = get_positive_float("  Power in watts: ")
        hours = get_positive_float("  Hours used per day (max 24): ", maximum=24)

        daily_kwh = daily_energy_kwh(watts, hours)
        monthly_kwh = daily_kwh * days
        machines.append({
            "name": name,
            "watts": watts,
            "hours": hours,
            "daily_kwh": daily_kwh,
            "monthly_kwh": monthly_kwh,
            "monthly_cost": energy_cost(monthly_kwh, tariff),
        })

    report = build_report(machines, tariff, days, currency)
    print("\n" + "\n".join(report))

    # Save the report to a text file (twist)
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(report) + "\n")
        print(f"\nReport saved to {REPORT_FILE}")
    except OSError:
        print("\nSorry, the report could not be saved, but the results are shown above.")


if __name__ == "__main__":
    main()
