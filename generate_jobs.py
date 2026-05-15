import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

N = 200

cities = [
    ("北京", 15, 40), ("上海", 12, 38), ("深圳", 10, 35),
    ("杭州", 8, 30), ("广州", 6, 28), ("成都", 5, 25),
    ("南京", 4, 22), ("武汉", 4, 20), ("苏州", 3, 18),
    ("西安", 3, 15),
]

skills_pool = [
    "Python", "SQL", "Pandas", "NumPy", "MySQL", "Flask", "Django",
    "Linux", "Git", "Docker", "Redis", "MongoDB", "Spark", "Hadoop",
    "TensorFlow", "PyTorch", "Scikit-learn", "Tableau", "Excel",
    "Jupyter", "REST API", "Vue", "React", "AWS", "数据分析",
    "数据挖掘", "爬虫", "ETL", "数据可视化",
]

job_titles = [
    "Python开发实习生", "数据分析实习生", "Python后端实习生",
    "数据挖掘实习生", "机器学习实习生", "Python爬虫实习生",
    "BI数据分析实习生", "Python测试实习生", "数据工程实习生",
    "AI算法实习生",
]

industries = [
    "互联网", "金融", "电商", "教育", "医疗",
    "人工智能", "游戏", "汽车", "物流", "房地产",
]

rows = []
for _ in range(N):
    city, base_min, base_max = random.choices(cities, weights=[c[1] for c in cities])[0]
    min_k = random.uniform(base_min * 0.8, base_min * 1.2)
    max_k = min_k * random.uniform(1.3, 2.0)
    salary_min = round(min_k, 1)
    salary_max = round(max_k, 1)

    n_skills = random.randint(3, 8)
    skills = ", ".join(random.sample(skills_pool, n_skills))

    rows.append({
        "title": random.choice(job_titles),
        "city": city,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "education": random.choice(["本科", "本科及以上", "大专", "硕士"]),
        "experience": random.choice(["不限", "应届生", "1年以下", "1-3年"]),
        "company_size": random.choice(["15-50人", "50-150人", "150-500人", "500-2000人", "2000人以上"]),
        "industry": random.choice(industries),
        "skills": skills,
    })

df = pd.DataFrame(rows)
df.to_csv("jobs.csv", index=False, encoding="utf-8-sig")
print(f"Generated {N} jobs -> jobs.csv")
print(df.groupby("city")["title"].count().sort_values(ascending=False).to_string())
