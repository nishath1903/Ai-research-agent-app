from agent import ResearchAgent, export_review

def main():
    """The main CLI for the Research Assistant Agent."""
    
    agent = ResearchAgent()
    
    print("\n--- 🤖 AI Research Assistant Activated ---")
    print("Goal: Academic Content Retrieval, Summarization, and Literature Review.")
    print("-" * 50)
    
    past_topics = agent.get_history()
    if past_topics:
        print("💡 Past Researched Topics:")
        for topic in past_topics:
            print(f"- {topic}")
        print("-" * 50)

    topic = input("❓ Enter your research topic (e.g., Explainable AI for Drug Discovery): \n> ").strip()
    
    if not topic:
        print("No topic entered. Exiting.")
        return

    # Run the core agent process
    final_output = agent.run_research(topic, paper_limit=1)
    
    if final_output:
        # Display the Overview to the user in the console
        print("\n--- Review Output (Overview) ---")
        try:
            # Print up to the Paper Summaries section
            overview_section = final_output['markdown_review'].split('## 2. Paper Summaries')[0]
            print(overview_section)
        except:
            print("Overview could not be displayed, check data/output.json for full structured output.")
        
        # CLI for Export
        export_choice = input("\nDo you want to export the full review (Markdown/JSON)? (m/j/n): ").lower()
        
        if export_choice == 'm':
            export_review(final_output, format_type='md')
        elif export_choice == 'j':
            export_review(final_output, format_type='json')
        else:
            print("Export skipped.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred in main: {e}")