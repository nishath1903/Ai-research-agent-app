import time
import os
import json
from typing import Dict, Any, List
from retriever import retrieve_academic_papers
from summarizer import generate_summary, LiteratureReviewOutput
from memory import load_memory, save_memory, save_output

class ResearchAgent:
    """
    The main agent orchestrator for academic content retrieval, summarization, 
    and literature review generation using Gemini and Semantic Scholar.
    """
    def __init__(self):
        self.history = load_memory()
        print(f"📝 Agent Initialized. Loaded {len(self.history)} past topics from memory.")

    def _update_memory(self, topic: str):
        """Adds the current topic to the agent's memory."""
        new_entry = {
            "topic": topic,
            "date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(new_entry)
        save_memory(self.history)
        print("💾 Memory updated.")

    def _generate_markdown_review(self, structured_review: LiteratureReviewOutput) -> str:
        """
        Takes the structured Pydantic output and formats it into a human-readable 
        Markdown literature review document.
        """
        md_content = f"# Literature Review: {structured_review.topic}\n\n"
        md_content += f"**Date Generated:** {time.strftime('%Y-%m-%d')}\n\n"
        md_content += "---\n\n"
        
        # 1. Overview
        md_content += f"## 1. Topic Overview\n\n"
        md_content += f"{structured_review.overview}\n\n"
        
        # 2. Individual Summaries
        md_content += "## 2. Paper Summaries\n\n"
        
        for i, paper in enumerate(structured_review.individual_summaries):
            md_content += f"### 2.{i+1}. {paper.title}\n"
            md_content += f"**Source:** [View Paper]({paper.original_url})\n\n"
            md_content += f"**Summary:** {paper.summary}\n\n"
            
            md_content += "**Key Findings:**\n"
            for finding in paper.key_findings:
                md_content += f"* {finding}\n"
            
            md_content += f"\n**Relevance:** {paper.relevance_to_topic}\n\n"
            md_content += "---\n\n"

        return md_content.strip()


    def run_research(self, topic: str, paper_limit: int = 1) -> Dict[str, Any] | None:
        """
        Runs the full RAG process for a given research topic.
        """
        print(f"\n--- Starting Research for: **{topic}** ---\n")
        
        # Step 1: Tool-calling Simulation (Retrieval)
        paper_metadata = retrieve_academic_papers(topic, paper_limit)
        
        if not paper_metadata:
            print("🛑 Process halted: Could not retrieve papers.")
            return None
            
        # Step 2: Summarization & Structured Output (RAG Core)
        structured_review = generate_summary(paper_metadata, topic)
        
        if not structured_review:
            print("🛑 Process halted: Could not generate structured review.")
            return None
            
        # Step 3: Combined Literature Review Generation (Markdown)
        markdown_review = self._generate_markdown_review(structured_review)
        
        # Step 4: Final Consolidation and Persistence
        final_output = {
            "topic": topic,
            "structured_json": structured_review.model_dump(), 
            "markdown_review": markdown_review
        }
        
        save_output(final_output)
        self._update_memory(topic) 
        
        print("\n🎉 Research Complete!")
        print(f"Results saved to: **data/output.json** (Structured JSON)")

        return final_output


    # In agent.py (around line 125)

    def get_history(self) -> List[Dict[str, Any]]: # <-- Change return type hint
        """Returns a list of previously researched topics."""
        return self.history # <-- Return the full history list (list of dictionaries)


def export_review(final_output: Dict[str, Any], format_type: str = 'md'):
    """Exports the generated review to a file in the output/ directory."""
    topic_slug = final_output['topic'].lower().replace(' ', '_').replace('-', '_').replace('.', '')
    
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True) 
    
    if format_type == 'md':
        filename = os.path.join(output_dir, f"{topic_slug}_review.md")
        content = final_output['markdown_review']
    elif format_type == 'json':
        filename = os.path.join(output_dir, f"{topic_slug}_structured.json")
        content = final_output['structured_json'] 
    else:
        print(f"Unsupported export format: {format_type}")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if format_type == 'json':
                json.dump(content, f, indent=4)
            else:
                f.write(content)

        print(f"📝 Successfully exported to: **{filename}**")
        
    except IOError as e:
        print(f"Error exporting file {filename}: {e}")