import os
import json
import argparse
from parser import extract_text
from analyzer import analyze_resume
from scorer import compute_score
from reporter import generate_pdf_report

OUTPUT_DIR = "./outputs"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_resume(file_path, save_json=True, compute_scores=True, json_only=False):
    print(f"Analyzing: {file_path}")

    try:
        raw_text = extract_text(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    try:
        analysis = analyze_resume(raw_text)
    except Exception as e:
        print(f"Error during LLM analysis: {e}")
        return

    if compute_scores:
        score_breakdown = compute_score(analysis)
        analysis["score_breakdown"] = score_breakdown
    else:
        score_breakdown = None

    print("\nStructured Analysis:")
    print(json.dumps(analysis, indent=2))

    if save_json:
        ensure_output_dir()
        out_name = os.path.splitext(os.path.basename(file_path))[0]
        out_path = os.path.join(OUTPUT_DIR, f"{out_name}_analysis.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)
        print(f"\nAnalysis saved to: {out_path}")

        report_path = os.path.join(OUTPUT_DIR, f"{out_name}_report.pdf")
        generate_pdf_report(out_path, report_path)

    if not json_only and compute_scores:
        print(f"\nFinal Score: {score_breakdown['total_score']}/100")

def main():
    parser = argparse.ArgumentParser(
        description="Resume Analyzer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--resume", "-r", required=True,
                        help="Path to resume file (PDF, DOCX, or TXT)")
    parser.add_argument("--json-only", action="store_true",
                        help="Only output the raw analysis, skip printing score")
    parser.add_argument("--skip-score", action="store_true",
                        help="Skip computing resume score")
    parser.add_argument("--no-save", action="store_true",
                        help="Do not save analysis to file")

    args = parser.parse_args()

    process_resume(
        file_path=args.resume,
        save_json=not args.no_save,
        compute_scores=not args.skip_score,
        json_only=args.json_only
    )

if __name__ == "__main__":
    main()
