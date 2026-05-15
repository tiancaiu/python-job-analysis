import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Python实习岗位分析", layout="wide")
st.title("Python 实习岗位数据分析")
st.write("基于招聘网站真实薪资与技能需求数据，辅助求职定位。")

# ── 技能过滤（排除前端技能和泛化术语） ──
SKILL_BLACKLIST = {
    "Vue", "React", "React Native", "Angular", "jQuery", "CSS", "HTML",
    "HTML5", "CSS3", "JavaScript", "TypeScript", "Node.js",
    "数据分析", "数据挖掘", "数据可视化",
}

# ── 加载数据 ──
df = pd.read_csv("jobs.csv")
df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2

# ── 侧边筛选 ──
with st.sidebar:
    st.header("筛选条件")
    cities = st.multiselect("城市", df["city"].unique(), default=list(df["city"].unique()))
    educations = st.multiselect("学历", df["education"].unique(), default=list(df["education"].unique()))

mask = df["city"].isin(cities) & df["education"].isin(educations)
filtered = df[mask]

# ── 核心指标 ──
st.subheader("核心指标")
c1, c2, c3, c4 = st.columns(4)
c1.metric("岗位总数", len(filtered))
c2.metric("平均最低薪资", f"{filtered['salary_min'].mean():.1f}K")
c3.metric("平均最高薪资", f"{filtered['salary_max'].mean():.1f}K")
c4.metric("城市覆盖", filtered["city"].nunique())

# ── 图表行 1 ──
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("各城市薪资对比")
    city_salary = filtered.groupby("city").agg(
        avg_min=("salary_min", "mean"),
        avg_max=("salary_max", "mean"),
        count=("title", "count"),
    ).reset_index().sort_values("count", ascending=False)

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="最低薪资(K)", x=city_salary["city"], y=city_salary["avg_min"].round(1),
                          text=city_salary["avg_min"].round(1), textposition="outside"))
    fig1.add_trace(go.Bar(name="最高薪资(K)", x=city_salary["city"], y=city_salary["avg_max"].round(1),
                          text=city_salary["avg_max"].round(1), textposition="outside"))
    fig1.update_layout(barmode="group", xaxis_title="城市", yaxis_title="薪资 (K/月)",
                       xaxis=dict(tickangle=0), yaxis=dict(tickangle=0))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("学历要求分布")
    edu_counts = filtered["education"].value_counts()
    fig2 = px.pie(values=edu_counts.values, names=edu_counts.index, title="学历要求占比")
    fig2.update_traces(textinfo="value+percent")
    st.plotly_chart(fig2, use_container_width=True)

# ── 图表行 2 ──
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("岗位类型分布")
    title_counts = filtered["title"].value_counts().head(10)
    if not title_counts.empty:
        title_counts = title_counts.iloc[::-1]
        fig3 = px.bar(x=title_counts.values, y=title_counts.index, orientation="h",
                      labels={"x": "岗位数", "y": ""}, title="Top 10 岗位类型",
                      text_auto=".0f")
        fig3.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=10), yaxis=dict(tickangle=0))
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.write("暂无数据")

with col_d:
    st.subheader("热门技能需求 Top 20")
    all_skills_raw = filtered["skills"].str.split(", ").explode()
    all_skills_raw = all_skills_raw[~all_skills_raw.isin(SKILL_BLACKLIST)]
    skills_counts = all_skills_raw.value_counts().head(20)

    if not skills_counts.empty:
        skills_counts = skills_counts.iloc[::-1]
        fig4 = px.bar(x=skills_counts.values, y=skills_counts.index, orientation="h",
                      labels={"x": "出现次数", "y": ""}, title="Top 20 技能需求",
                      text_auto=".0f")
        fig4.update_layout(height=500, margin=dict(l=10, r=10, t=40, b=10), yaxis=dict(tickangle=0))
        fig4.update_traces(textposition="outside")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.write("暂无数据")

# ── 图表行 3 ──
st.subheader("城市 × 薪资散点图")
fig5 = px.scatter(
    filtered, x="salary_min", y="salary_max", color="city",
    size="salary_avg", hover_data=["title", "company_size"],
    title="各城市岗位薪资分布",
    labels={"salary_min": "最低薪资(K)", "salary_max": "最高薪资(K)"},
)
fig5.update_layout(xaxis=dict(tickangle=0), yaxis=dict(tickangle=0))
st.plotly_chart(fig5, use_container_width=True)

# ── 结论 ──
st.subheader("分析结论")
top_city = city_salary.iloc[0]
# 过滤后重新算 top skill
all_skills_for_conclusion = filtered["skills"].str.split(", ").explode()
all_skills_for_conclusion = all_skills_for_conclusion[~all_skills_for_conclusion.isin(SKILL_BLACKLIST)]
skills_top = all_skills_for_conclusion.value_counts()
top_skill = skills_top.index[0] if len(skills_top) > 0 else "Python"
top3 = skills_top.head(3).index.tolist()
st.markdown(f"""
- **就业城市**：岗位集中在 **{top_city['city']}**（{top_city['count']} 岗），平均薪资 {top_city['avg_min']:.1f}K ~ {top_city['avg_max']:.1f}K/月
- **学历门槛**：{filtered['education'].value_counts().idxmax()} 占比最高，{'机会对本科及以上学历最友好' if '本科' in str(filtered['education'].value_counts().idxmax()) else '多种学历层次均有对应岗位'}
- **技能需求 Top 3**：**{', '.join(top3)}**，SQL + Python + 数据处理框架是 Python 实习岗位核心要求
- **求职建议**：掌握 Python + SQL + 1个Web框架（Flask/Django）组合，面试通过率最高
""")
