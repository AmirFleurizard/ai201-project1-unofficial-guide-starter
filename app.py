# app.py
# Gradio web interface for the UNC Charlotte Dining Unofficial Guide.

import gradio as gr
from generate import ask


def handle_query(question: str):
    """Handle a user query and return answer + sources."""
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    # Format sources as a bulleted list
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return result["answer"], sources


# ── Gradio Interface ───────────────────────────────────────────
with gr.Blocks(title="UNCC Dining Unofficial Guide") as demo:
    gr.Markdown("""
    # 🍴 UNC Charlotte Dining — Unofficial Guide
    Ask anything about campus dining at UNC Charlotte.
    Answers are grounded in real student reviews, guides, and official sources.
    """)

    with gr.Row():
        with gr.Column(scale=3):
            question_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g. Is the meal plan worth it? What are the best dining options near campus?",
                lines=2
            )
            ask_btn = gr.Button("Ask", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### Example Questions")
            gr.Markdown("""
            - What dining halls are available?
            - Does SoVi have vegan options?
            - Is the meal plan worth it?
            - What do students say about food quality?
            - What restaurants are near campus?
            """)

    with gr.Row():
        answer_output = gr.Textbox(
            label="Answer",
            lines=10,
            interactive=False
        )

    with gr.Row():
        sources_output = gr.Textbox(
            label="Retrieved From",
            lines=4,
            interactive=False
        )

    # Trigger on button click or Enter key
    ask_btn.click(
        handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output]
    )
    question_input.submit(
        handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output]
    )

demo.launch()