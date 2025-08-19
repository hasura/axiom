#!/usr/bin/env python3
"""
Convert a embeddings JSON to CSV for Postgres COPY.
Auto-detects embedding dimension unless --embedding-dim is provided.

CSV columns: id,pdf_id,url,chunk_index,start_pos,title,text,embedding_text
embedding_text is formatted as pgvector text: [0.1, -0.2, ...]
"""

import argparse, json, csv, re, sys, math
from typing import Any, Dict, Iterable, List, Optional

ARXIV_RE = re.compile(r"^\d{4}\.\d{5}v\d+\.pdf$")

def to_url(doc_name: str, url_template: Optional[str], infer_arxiv: bool) -> str:
    if url_template:
        return url_template.format(document=doc_name)
    if infer_arxiv and ARXIV_RE.match(doc_name):
        return f"https://arxiv.org/pdf/{doc_name}"
    return doc_name

def fmt_vec_for_pgvector(vec: Iterable[float], precision: int = 7) -> str:
    parts = []
    fmt = f".{precision}g"
    for x in vec:
        if isinstance(x, (int, float)) and not (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
            parts.append(format(float(x), fmt))
        else:
            raise ValueError("Non-numeric encountered in embedding")
    return "[" + ", ".join(parts) + "]"

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def first_valid_dim(vectors: List[Dict[str, Any]]) -> Optional[int]:
    for item in vectors:
        vec = item.get("vector", None)
        if isinstance(vec, list) and all(isinstance(x, (int, float)) for x in vec) and len(vec) > 0:
            return len(vec)
    return None

def main() -> None:
    p = argparse.ArgumentParser(description="Convert embeddings JSON to CSV for Postgres COPY.")
    p.add_argument("--input", "-i", required=True, help="Path to embeddings JSON")
    p.add_argument("--output", "-o", required=True, help="Path to output CSV (e.g., initdb/import/chunks.csv)")
    p.add_argument("--url-template", default=None,
                   help="Python format string for URLs, e.g. 'https://bucket/pdfs/{document}'")
    p.add_argument("--infer-arxiv", action="store_true",
                   help="Map names like '2505.24293v1.pdf' to https://arxiv.org/pdf/<document>")
    p.add_argument("--embedding-dim", type=int, default=None,
                   help="Expected embedding dimension; if omitted, auto-detect from first valid vector")
    p.add_argument("--skip-no-embedding", action="store_true",
                   help="Skip rows without a valid numeric embedding")
    p.add_argument("--precision", type=int, default=7,
                   help="Significant digits for embedding output (default: 7)")
    args = p.parse_args()

    data = load_json(args.input)
    vectors = data.get("vectors", [])
    if not isinstance(vectors, list):
        print("JSON does not have a 'vectors' array", file=sys.stderr)
        sys.exit(1)

    # Auto-detect embedding dimension if not provided
    detected_dim = first_valid_dim(vectors)
    expected_dim = args.embedding_dim if args.embedding_dim is not None else detected_dim

    if expected_dim is None:
        print("Warning: Could not detect embedding dimension (no valid numeric vectors found). "
              "Proceeding without dimension checks.", file=sys.stderr)

    out_fields = ["id","pdf_id","url","chunk_index","start_pos","title","text","embedding_text"]
    rows_written = 0
    rows_skipped = 0

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()

        for item in vectors:
            attrs = item.get("attributes", {})
            doc_id = str(item.get("id", "")).strip()
            pdf_id = str(attrs.get("document", "")).strip()
            text = attrs.get("text", "")

            if not doc_id or not pdf_id or text is None:
                rows_skipped += 1
                continue

            url = to_url(pdf_id, args.url_template, args.infer_arxiv)
            chunk_index = attrs.get("chunk_index", 0)
            start_pos = attrs.get("start_position", 0)
            title = attrs.get("title", "")

            embedding_text = ""
            vec = item.get("vector", None)
            valid_vec = isinstance(vec, list) and all(isinstance(x, (int, float)) for x in vec)

            if valid_vec:
                # Validate dimension (if known)
                if expected_dim is not None and len(vec) != expected_dim:
                    print(f"Warning: {doc_id} vector dim={len(vec)} != expected {expected_dim}", file=sys.stderr)
                try:
                    embedding_text = fmt_vec_for_pgvector(vec, precision=args.precision)
                except Exception:
                    if args.skip_no_embedding:
                        rows_skipped += 1
                        continue
                    else:
                        embedding_text = ""
            else:
                if args.skip_no_embedding:
                    rows_skipped += 1
                    continue

            w.writerow({
                "id": doc_id,
                "pdf_id": pdf_id,
                "url": url,
                "chunk_index": int(chunk_index) if chunk_index is not None else 0,
                "start_pos": int(start_pos) if start_pos is not None else 0,
                "title": title if title is not None else "",
                "text": text,
                "embedding_text": embedding_text
            })
            rows_written += 1

    summary_dim = expected_dim if expected_dim is not None else "unknown"
    print(f"Done. Wrote {rows_written} rows to {args.output} (skipped {rows_skipped}). "
          f"Embedding dim: {summary_dim}")

if __name__ == "__main__":
    main()