from src.agents.executor import run_agent


def main():
    print("Assistant intelligent - Partie 2 (Agents + Tools)")
    print("Tape 'quit' pour quitter.\n")

    while True:
        user_query = input("Vous : ").strip()
        if user_query.lower() in {"quit", "exit"}:
            print("Fin de session.")
            break

        result = run_agent(user_query)
        print("\nAssistant :")
        print(result)
        print()


if __name__ == "__main__":
    main()