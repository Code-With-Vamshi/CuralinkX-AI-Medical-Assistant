from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET
from flask_cors import CORS
import ollama
import threading
import time

app = Flask(__name__)
CORS(app)

cache = {}
last_query = {}

# ================= SAFE REQUEST
def safe_request(url, params):
    try:
        return requests.get(url, params=params, timeout=3)
    except:
        return None


# ================= QUERY EXPANSION
def expand_query(disease, intent, location, what_if):
    base = f"{intent} related to {disease}"

    if location:
        base += f" in {location}"

    if what_if:
        base += f" considering {what_if}"

    return base + " treatment research clinical trials latest studies"


# ================= LLM SUMMARY
def generate_llm_summary(query, publications, trials, what_if):
    try:
        papers = "\n".join([p["title"] for p in publications[:3]])
        trials_txt = "\n".join([t["title"] for t in trials[:2]])

        prompt = f"""
You are an expert medical AI.

Query: {query}
Scenario: {what_if}

Papers:
{papers}

Trials:
{trials_txt}

Give clear insights, treatment ideas, and risks.
"""

        res = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}],
        )

        return res["message"]["content"]

    except:
        return None


# ================= OPENALEX
def fetch_openalex(query):
    res = safe_request("https://api.openalex.org/works", {
        "search": query,
        "per-page": 10
    })

    results = []

    if res and res.status_code == 200:
        for w in res.json().get("results", []):
            results.append({
                "title": w.get("title"),
                "abstract": "OpenAlex source",
                "year": w.get("publication_year"),
                "source": "OpenAlex",
                "link": w.get("id"),
            })

    return results


# ================= RANK
def rank_publications(query, pubs):
    words = set(query.split())

    for p in pubs:
        score = 0
        text = (p.get("title", "") + p.get("abstract", "")).lower()

        for w in words:
            if w in text:
                score += 2

        p["score"] = score

    return sorted(pubs, key=lambda x: x["score"], reverse=True)


# ================= MAIN API
@app.route("/analyze", methods=["POST"])
def analyze():
    global last_query

    start = time.time()
    data = request.json

    disease = data.get("disease", "")
    intent = data.get("intent", "")
    location = data.get("location", "")
    what_if = data.get("what_if", "")

    query = expand_query(disease, intent, location, what_if).lower()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    if query in cache:
        return jsonify(cache[query])

    pubmed_results = []
    openalex_results = []
    trials_results = []

    # ================= PUBMED
    def get_pubmed():
        try:
            res = safe_request(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                {"db": "pubmed", "term": query, "retmax": 10, "retmode": "json"},
            )

            if not res:
                return

            ids = res.json().get("esearchresult", {}).get("idlist", [])[:5]

            fetch = safe_request(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
                {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"},
            )

            if not fetch:
                return

            root = ET.fromstring(fetch.text)

            for a in root.findall(".//PubmedArticle"):
                pubmed_results.append({
                    "title": a.findtext(".//ArticleTitle"),
                    "abstract": a.findtext(".//AbstractText") or "",
                    "year": a.findtext(".//Year") or "N/A",
                    "source": "PubMed",
                })

        except:
            pass

    # ================= TRIALS (IMPROVED)
    def get_trials():
        try:
            res = safe_request(
                "https://clinicaltrials.gov/api/query/study_fields",
                {
                    "expr": query,
                    "fields": "BriefTitle,OverallStatus",
                    "min_rnk": 1,
                    "max_rnk": 5,
                    "fmt": "json",
                },
            )

            if not res:
                return

            for s in res.json()["StudyFieldsResponse"]["StudyFields"]:
                trials_results.append({
                    "title": s.get("BriefTitle", [""])[0],
                    "status": s.get("OverallStatus", ["N/A"])[0],
                    "info": f"Status: {s.get('OverallStatus', ['N/A'])[0]}"
                })

        except:
            pass

    # THREADS
    t1 = threading.Thread(target=get_pubmed)
    t2 = threading.Thread(target=get_trials)
    t3 = threading.Thread(target=lambda: openalex_results.extend(fetch_openalex(query)))

    t1.start(); t2.start(); t3.start()
    t1.join(); t2.join(); t3.join()

    ranked = rank_publications(query, pubmed_results + openalex_results)

    # ================= WHAT IF
    what_if_text = f"If {what_if}, risk increases and needs careful monitoring." if what_if else ""

    # ================= QUICK INSIGHTS (INSTANT)
    quick = f"Found {len(ranked)} papers and {len(trials_results)} trials for {disease}."

    response = {
        "insights": quick,
        "publications": ranked[:5],
        "clinical_trials": trials_results,
        "what_if": what_if_text,
        "meta": {
            "response_time_ms": int((time.time() - start) * 1000)
        }
    }

    cache[query] = response

    # ================= BACKGROUND AI (WORKING NOW)
    def run_ai():
        ai = generate_llm_summary(query, ranked, trials_results, what_if)
        if ai:
            cache[query]["insights"] = ai

    threading.Thread(target=run_ai).start()

    return jsonify(response)


@app.route("/")
def home():
    return "AI Medical API Running 🚀"


if __name__ == "__main__":
    app.run(port=8000, debug=True)