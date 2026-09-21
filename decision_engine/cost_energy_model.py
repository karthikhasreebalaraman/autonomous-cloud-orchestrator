def calculate_cost(running_containers, cost_per_container_hour=0.05):
    """
    Estimate infrastructure cost per hour.
    """
    return round(
        running_containers * cost_per_container_hour,
        4
    )


def calculate_energy(running_containers, energy_per_container=50):
    """
    Estimate energy consumption in watts.
    """
    return running_containers * energy_per_container


def calculate_cost_and_energy(running_containers):
    """
    Calculate current cost and energy consumption.
    """
    return {
        "running_containers": running_containers,
        "estimated_cost_per_hour": calculate_cost(running_containers),
        "estimated_energy_watts": calculate_energy(running_containers)
    }


def compare_scaling_options(running_containers):
    """
    Compare the current infrastructure with
    possible scale-up and scale-down states.
    """

    current = running_containers
    scale_up = running_containers + 1
    scale_down = max(2, running_containers - 1)

    return {
        "current": {
            "containers": current,
            "cost_per_hour": calculate_cost(current),
            "energy_watts": calculate_energy(current)
        },

        "scale_up": {
            "containers": scale_up,
            "cost_per_hour": calculate_cost(scale_up),
            "energy_watts": calculate_energy(scale_up)
        },

        "scale_down": {
            "containers": scale_down,
            "cost_per_hour": calculate_cost(scale_down),
            "energy_watts": calculate_energy(scale_down)
        }
    }


if __name__ == "__main__":

    running_containers = 3

    result = compare_scaling_options(running_containers)

    print("Cost and Energy Comparison")
    print("==========================")

    print("\nCurrent:")
    print(result["current"])

    print("\nScale Up:")
    print(result["scale_up"])

    print("\nScale Down:")
    print(result["scale_down"])