from lib.site_sense import SiteSense


def main():
    llm: SiteSense = SiteSense(model="gpt-3.5-turbo", temp=0.4)  # NOQA

    while True:
        question = input("Site Sense: ")
        if question.lower() == 'q':
            llm.clear_history()
            break

        prompt = llm.create_response(question=question)
        llm.stream_response(prompt=prompt)

if __name__ == "__main__":
    main()
