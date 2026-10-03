"""Print node status and tip height."""

from yada_agent import YadaClient

def main() -> None:
    client = YadaClient()
    print(client.status())
    print(client.latest_block())

if __name__ == "__main__":
    main()
