from src.agents.executor import run_agent


def main():
    print("Assistant intelligent - Partie 2 (LangChain Agents + Tools)")
    print("Tape 'quit' pour quitter.\n")

    while True:
        try:
            user_query = input("Vous : ").strip()

            if user_query.lower() in {"quit", "exit"}:
                print("Fin de session.")
                break

            result = run_agent(user_query)

            print("\nAssistant :")
            if isinstance(result, dict) and "messages" in result:
                messages = result["messages"]
                if messages:
                    last_message = messages[-1]
                    content = getattr(last_message, "content", None)
                    print(content if content else last_message)
                else:
                    print(result)
            else:
                print(result)
            print()

        except KeyboardInterrupt:
            print("\nFin de session.")
            break
        except Exception as e:
            print("\nErreur :")
            print(e)
            print()


if __name__ == "__main__":
    main()