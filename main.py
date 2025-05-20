from preswald import connect, get_df, query, table, text, plotly, sidebar
import plotly.express as px

# Optional import for LLM
try:
    from preswald import llm
    LLM_ENABLED = True
except ImportError:
    LLM_ENABLED = False

# Sidebar with branding

# Load dataset
connect()
df = get_df("my_dataset")

if df.empty:
    text("⚠️ Dataset 'my_dataset' is empty. Check data/data.csv or preswald.toml.")
else:
    # Filter for positive sentiment
    sql = "SELECT * FROM my_dataset WHERE Sentiment = 'positive'"
    positive_df = query(sql, "my_dataset")

    # Main UI
    text("# Financial Sentiment Analysis App")
    table(positive_df, title="Positive Sentiment News")

    # Visualization
    fig = px.histogram(df, x="Sentiment", title="Distribution of Sentiment in Financial News")
    plotly(fig)

    # LLM Summary
    text("## 🧠 AI Summary of Positive Financial News")
    sentences = positive_df["Sentence"].tolist()[:10]
    sample_text = "\n".join(sentences)

    if LLM_ENABLED:
        try:
            summary = llm.complete(
                f"Summarize the following financial news headlines into 3 bullet points:\n\n{sample_text}",
                model="gpt-4"
            )
            text(summary)
        except Exception as e:
            text(f"⚠️ LLM error: {e}")
    else:
        text("⚠️ LLM module not available.")
        text("🔹 Sample headlines:\n\n" + sample_text)

text("✅ App finished loading")
