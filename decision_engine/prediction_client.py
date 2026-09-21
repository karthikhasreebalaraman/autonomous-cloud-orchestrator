def get_prediction(current_cpu, memory, predicted_cpu):
    """
    Prediction client.

    Later, predicted_cpu will come from Member 2's ML model.
    """

    return {
        "current_cpu": current_cpu,
        "memory": memory,
        "predicted_cpu": predicted_cpu
    }


if __name__ == "__main__":

    predicted_cpu = float(
        input("Enter predicted CPU (%): ")
    )

    result = get_prediction(
        current_cpu=50,
        memory=65,
        predicted_cpu=predicted_cpu
    )

    print("\nPrediction Result")
    print("=================")
    print(result)