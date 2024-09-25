from site_sense_lib.lib.site_sense import SiteSense


def main():
    emily: SiteSense = SiteSense(model="gpt-3.5-turbo", temp=0.4)  # NOQA

    while True:
        question = input("Site Sense: ")
        if question.lower() == 'q':
            emily.clear_history()
            break

        response = emily.chat_bot(question)
        print(f"Emily: {response['response']}")

if __name__ == "__main__":
    main()
