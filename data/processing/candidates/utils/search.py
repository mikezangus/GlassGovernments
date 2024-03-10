from selenium import webdriver


def search(driver: webdriver.Firefox, query: str) -> None:
    url = f"https://duckduckgo.com/?q={query}"
    driver.get(url)
    return
