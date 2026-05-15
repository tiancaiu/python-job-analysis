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

# 岗位 → 技能映射（确保技能与岗位相关）
JOB_SKILLS = {
    "Python开发实习生":       ["Python", "Django", "Flask", "MySQL", "Linux", "Git", "Docker", "Redis", "REST API"],
    "数据分析实习生":         ["Python", "SQL", "Pandas", "NumPy", "Excel", "Jupyter", "ETL", "Tableau", "MySQL"],
    "Python后端实习生":       ["Python", "Flask", "Django", "MySQL", "Redis", "Linux", "Docker", "Git", "REST API"],
    "数据挖掘实习生":         ["Python", "SQL", "Pandas", "Scikit-learn", "Spark", "Hadoop", "NumPy", "ETL"],
    "机器学习实习生":         ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "NumPy", "Pandas", "Linux", "Docker"],
    "Python爬虫实习生":       ["Python", "Scrapy", "MySQL", "MongoDB", "Redis", "Linux", "Git", "Docker"],
    "BI数据分析实习生":       ["SQL", "Excel", "Tableau", "Python", "ETL", "MySQL", "Pandas"],
    "Python测试实习生":       ["Python", "Linux", "Git", "Docker", "MySQL", "Jupyter"],
    "数据工程实习生":         ["Python", "Spark", "Hadoop", "ETL", "SQL", "Linux", "Docker", "AWS"],
    "AI算法实习生":           ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "Linux", "Docker", "NumPy", "Pandas"],
}

job_titles = list(JOB_SKILLS.keys())

industries = [
    "互联网", "金融", "电商", "教育", "医疗",
    "人工智能", "游戏", "汽车", "物流", "房地产",
]

rows = []
for _ in range(N):
    city, base_min, base_max = random.choices(cities, weights=[c[1] for c in cities])[0]
    min_k = round(random.uniform(base_min * 0.8, base_min * 1.2), 1)
    max_k = round(min_k * random.uniform(1.3, 2.0), 1)

    title = random.choice(job_titles)
    skills_pool = JOB_SKILLS[title]

    # 选 4~7 个技能，核心技能高概率出现
    n = random.randint(4, 7)
    weights = [0.8 if s in ["Python", "SQL", "MySQL", "Linux"] else 0.5 for s in skills_pool]
    chosen = list(np.random.choice(skills_pool, size=min(n, len(skills_pool)), replace=False, p=np.array(weights)/sum(weights)))

    rows.append({
        "title": title,
        "city": city,
        "salary_min": min_k,
        "salary_max": max_k,
        "education": random.choice(["本科", "本科及以上", "大专", "硕士"]),
        "experience": random.choice(["不限", "应届生", "1年以下", "1-3年"]),
        "company_size": random.choice(["15-50人", "50-150人", "150-500人", "500-2000人", "2000人以上"]),
        "industry": random.choice(industries),
        "skills": ", ".join(chosen),
    })

df = pd.DataFrame(rows)
df.to_csv("jobs.csv", index=False, encoding="utf-8-sig")
print(f"Generated {N} jobs -> jobs.csv")
print(df.groupby("city")["title"].count().sort_values(ascending=False).to_string())
print()
print("Skills per job type:")
for jt in job_titles:
    s = df[df["title"] == jt]["skills"].str.split(", ").explode().value_counts()
    print(f"  {jt}: {s.index.tolist()}")
