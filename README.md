# Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Analyze resumes using a LLM to extract structure, assess content, and generate a breakdown of resume quality. Outputs structured JSON data as well as a polished, shareable PDF report.

## 1. Runthrough Guide

### **Installing dependencies**
Simply enter
```sh
pip install -r requirements.txt
```


### **Getting an API Key**

This project uses [OpenRouter](https://openrouter.ai/) to access Meta’s LLaMA 3.3 70B Instruct model.

* Visit [https://openrouter.ai/settings/keys](https://openrouter.ai/settings/keys) to create an API key.
* Copy the key and save it in a `.env` file in the project root:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
```


### **Analyzing a Resume**

* The tool extracst text from `.pdf`, `.docx`, or `.txt` resumes.
* The resume is sent to the LLM for analysis.
* Outputs:

  * `*.json`: structured analysis + extracted data
  * `*.pdf`: printable analysis report

```sh
python main.py --resume ./data/sample_resume.pdf
```

#### Optional flags:

| Flag           | Description                           |
| -------------- | ------------------------------------- |
| `--json-only`  | Don't print the score to console      |
| `--no-save`    | Don't save the result to `./outputs/` |
| `--skip-score` | Skip scoring (just extract data)      |


#### Details:

**LLM response includes:**

* Detected and missing sections
* Well-written section highlights
* Improvement suggestions
* Skill sentiment summary
* Resume structured into: `personal_info`, `education`, `experience`, `skills`, `projects`
* A detailed score breakdown based on:
  * Section completeness
  * Content richness
  * Clarity and professionalism
  * Resume strength for role + experience

The scoring is fully handled by the LLM and returned as JSON.

**Example output in `./outputs/`:**

```
sample_resume_analysis.json
sample_resume_report.pdf
```


## 2. Results & Outputs

* Full analysis is printed and saved as JSON
* PDF report includes score, strengths, weaknesses, and structured summary
* Output is clean, printable, and readable across systems
* All scoring is handled by LLM, based on prompt-defined rubric


## 3. Possible Next Steps

* Add support for multiple resume batch evaluation
* Export structured data into `.csv` for comparison
* Build a web interface around this CLI
* Extend prompt for matching with job descriptions
---

Thank you for reading! Feel free to fork, contribute, or suggest enhancements via issues or pull requests.