def report(step, stage, result):
    icon = "✔" if result.success else "✘"

    print(f"  {icon} {stage}: {step.name}")

    if result.output:
        for line in result.output.splitlines():
            print(f"    {line}")

    return result.success
