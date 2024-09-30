import re
import whois


def extract_domain(text):
    # Regular expression to match domains
    match = re.search(r'([a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,})', text)
    if match:
        return match.group(0)  # Return the matched domain
    return None


def whois_lookup(text: str) -> str:
    domain = extract_domain(text)

    if domain is None:
        return "No valid domain found in the input."

    try:
        w = whois.whois(domain)
        if w.status is not None:
            return f"The domain {domain} is already registered."
    except Exception:  # NOQA
        return f"The domain {domain} is Available!"



if __name__ == '__main__':
    user_input = input("You: ")

    for domain in [".com", ".net", ".edu"]:
        if domain in user_input.lower():
            results = whois_lookup(user_input)
            response = f"Results: {results}"

    print(response)
