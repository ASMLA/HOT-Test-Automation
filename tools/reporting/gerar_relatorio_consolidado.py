from pathlib import Path
import html, re
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
XML = REPORTS / "output.xml"
OUT = REPORTS / "relatorio_consolidado.html"

SCENARIOS = [
    ("HOT-INV-DEF-001", "Defeito Dentro da Garantia e Sem Peça"),
    ("HOT-INV-DEF-002", "Defeito Dentro da Garantia e Com Peça"),
    ("HOT-INV-DEF-003", "Defeito Fora da Garantia + Reparo Aprovado"),
    ("HOT-INV-DEF-004", "Defeito Fora da Garantia + Reparo Reprovado + Máquina Funcional"),
    ("HOT-INV-DEF-005", "Defeito Fora da Garantia + Reparo Reprovado + Máquina Não Funcional"),
]

def read_results():
    result = {sid: {"name": name, "status": "SEM RESULTADO", "elapsed": "-"} for sid, name in SCENARIOS}
    if not XML.exists():
        return result
    try:
        root = ET.parse(XML).getroot()
        for test in root.findall(".//test"):
            tname = test.get("name", "")
            for sid, name in SCENARIOS:
                if sid in tname:
                    st = test.find("status")
                    if st is not None:
                        result[sid]["status"] = st.get("status", "SEM RESULTADO")
                        result[sid]["elapsed"] = st.get("elapsed", "-")
    except Exception:
        pass
    return result

def count_evidence(sid):
    folder = REPORTS / "evidencias" / sid
    return len([p for p in folder.glob("*.png")]) if folder.exists() else 0

def main():
    data = read_results()
    cards = []
    passed = failed = 0
    for sid, name in SCENARIOS:
        d = data[sid]
        st = d["status"]
        if st == "PASS": passed += 1
        if st == "FAIL": failed += 1
        cls = "pass" if st == "PASS" else "fail" if st == "FAIL" else "neutral"
        ev = count_evidence(sid)
        rel = f"evidencias/{sid}/relatorio_cenario.html"
        cards.append(f"""<section class="card">
          <div class="head"><div><div class="sid">{sid}</div><h2>{html.escape(name)}</h2></div><span class="status {cls}">{html.escape(st)}</span></div>
          <div class="stats"><div><small>Evidências</small><strong>{ev}</strong></div><div><small>Duração</small><strong>{html.escape(d["elapsed"])}</strong></div></div>
          <a class="btn" href="{rel}">Abrir relatório completo do cenário</a>
        </section>""")
    overall = "PASS" if passed == len(SCENARIOS) else "FAIL" if failed else "PARCIAL"
    ocls = "pass" if overall == "PASS" else "fail" if overall == "FAIL" else "neutral"
    css = """*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#18212b;font-family:Arial,sans-serif}.wrap{max-width:1150px;margin:auto;padding:30px}.hero,.card{background:white;border:1px solid #dce2e7;border-radius:14px;margin-bottom:18px}.hero{padding:28px}.top,.head{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.kicker,.sid{font-size:12px;font-weight:800;color:#2767ad;letter-spacing:.06em}.status{padding:9px 14px;border-radius:999px;color:white;font-weight:800}.pass{background:#16834b}.fail{background:#b42318}.neutral{background:#66737f}.summary{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}.summary div,.stats div{background:#f7f9fb;border-radius:9px;padding:13px}.summary small,.stats small{display:block;color:#66737f;font-weight:700;margin-bottom:5px}.card{padding:22px}.card h2{margin:5px 0}.stats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:18px 0}.btn{display:inline-block;text-decoration:none;background:#2164aa;color:white;font-weight:700;padding:11px 15px;border-radius:8px}@media(max-width:700px){.summary,.stats{grid-template-columns:1fr}.top,.head{display:block}.status{display:inline-block;margin-top:10px}}"""
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Relatório Consolidado HOT</title><style>{css}</style></head><body><main class="wrap">
<section class="hero"><div class="top"><div><div class="kicker">HOT TEST AUTOMATION</div><h1>Relatório Consolidado de Cenários</h1><p>Execução conjunta dos cenários DEF-001, DEF-002, DEF-003, DEF-004 e DEF-005.</p></div><span class="status {ocls}">{overall}</span></div>
<div class="summary"><div><small>Cenários</small><strong>{len(SCENARIOS)}</strong></div><div><small>Passaram</small><strong>{passed}</strong></div><div><small>Falharam</small><strong>{failed}</strong></div></div></section>
{''.join(cards)}
<footer style="color:#66737f;font-size:12px;text-align:center">Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</footer>
</main></body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print("Relatório consolidado gerado:", OUT)

if __name__ == "__main__":
    main()
