"""
BOSS直聘 / 51job Python实习岗位爬虫
使用 Selenium 自动化浏览器绕过反爬，需安装 chromedriver
"""
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    return webdriver.Chrome(options=options)


def crawl_boss(keyword="Python实习", pages=5):
    driver = create_driver()
    jobs = []

    for page in range(1, pages + 1):
        url = (
            f"https://www.zhipin.com/web/geek/job?"
            f"query={keyword}&city=100010000&page={page}"
        )
        driver.get(url)
        time.sleep(random.uniform(2, 4))

        cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-wrapper")
        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, ".job-name").text
                salary = card.find_element(By.CSS_SELECTOR, ".salary").text
                company = card.find_element(By.CSS_SELECTOR, ".company-name").text
                tags = [t.text for t in card.find_elements(By.CSS_SELECTOR, ".tag-list li")]
                jobs.append({
                    "title": title,
                    "salary": salary,
                    "company": company,
                    "tags": ",".join(tags),
                })
            except Exception:
                continue
        print(f"Page {page}: collected {len(jobs)} jobs so far")

    driver.quit()
    return jobs


def save_csv(jobs, filename="jobs.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["title", "salary", "company", "tags"])
        w.writeheader()
        w.writerows(jobs)
    print(f"Saved {len(jobs)} jobs to {filename}")


if __name__ == "__main__":
    data = crawl_boss()
    save_csv(data)
