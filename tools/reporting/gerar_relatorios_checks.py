from pathlib import Path
import html
import xml.etree.ElementTree as ET
from datetime import datetime
from checks_catalog import CHECKS

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
XML = REPORTS / "output.xml"
CONSOLIDATED = REPORTS / "relatorio_consolidado.html"

def node_status(node):
    if node is None:
        return "NÃO EXECUTADO"
    st = node.find("status")
    return st.get("status", "NÃO EXECUTADO") if st is not None else "NÃO EXECUTADO"

def load_tests():
    result = {}
    if not XML.exists():
        return result
    root = ET.parse(XML).getroot()
    for test in root.findall(".//test"):
        name = test.get("name", "")
        for sid in CHECKS:
            if sid in name:
                result[sid] = test
    return result

def keyword_status(test, keyword_name):
    if test is None:
        return "NÃO EXECUTADO"
    matches = [kw for kw in test.iter("kw") if kw.get("name") == keyword_name]
    if not matches:
        return "NÃO EXECUTADO"
    statuses = [node_status(kw) for kw in matches]
    if "FAIL" in statuses:
        return "FAIL"
    if "PASS" in statuses:
        return "PASS"
    return "NÃO EXECUTADO"

def scenario_result(sid, cfg, tests):
    test = tests.get(sid)
    rows = []
    counts = {"PASS": 0, "FAIL": 0, "NÃO EXECUTADO": 0}
    for cid, title, source_kw, expected, evidences in cfg["checks"]:
        st = keyword_status(test, source_kw)
        counts[st] += 1
        rows.append((cid, title, source_kw, expected, evidences, st))
    return node_status(test), rows, counts

def evidence_links(sid, files):
    folder = REPORTS / "evidencias" / sid
    out = []
    for name in files:
        if (folder / name).exists():
            out.append(
                '<figure class="evidence-item">'
                f'<img class="evidence-img" src="{html.escape(name)}" alt="Evidência {html.escape(name)}" loading="lazy">'
                f'<figcaption>{html.escape(name)}</figcaption>'
                '</figure>'
            )
        else:
            out.append(f'<span class="ev missing">{html.escape(name)} — não encontrada</span>')
    return '<div class="evidence-grid">' + "".join(out) + '</div>'

def render_scenario(sid, cfg, test_status, rows, counts):
    folder = REPORTS / "evidencias" / sid
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / "relatorio_cenario.html"

    items = []
    for cid, title, source_kw, expected, evidences, st in rows:
        cls = "pass" if st == "PASS" else "fail" if st == "FAIL" else "neutral"
        items.append(
            '<section class="check">'
            f'<div class="head"><div><div class="cid">{cid}</div><h2>{html.escape(title)}</h2></div><span class="status {cls}">{st}</span></div>'
            f'<p><b>Validação:</b> {html.escape(expected)}</p>'
            f'<p class="tech"><b>Comprovada pela execução:</b> {html.escape(source_kw)}</p>'
            f'<div><b>Evidências relacionadas:</b>{evidence_links(sid, evidences)}</div>'
            '</section>'
        )

    total = len(rows)
    tc = "pass" if test_status == "PASS" else "fail" if test_status == "FAIL" else "neutral"
    css = "*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#17212b;font-family:Arial,sans-serif}.wrap{max-width:1300px;margin:auto;padding:28px}.hero,.check{background:#fff;border:1px solid #dce2e7;border-radius:14px;margin-bottom:16px}.hero,.check{padding:22px}.top,.head{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.status{padding:8px 13px;border-radius:999px;color:#fff;font-weight:800;white-space:nowrap}.pass{background:#16834b}.fail{background:#b42318}.neutral{background:#66737f}.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}.summary div{background:#f7f9fb;border-radius:9px;padding:13px}.summary small{display:block;color:#66737f;font-weight:700}.cid{font-size:12px;font-weight:800;color:#2767ad}.head h2{margin:5px 0}.tech{color:#5b6874;font-size:13px}.evidence-grid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:12px}.evidence-item{margin:0;background:#f7f9fb;border:1px solid #e1e6eb;border-radius:10px;padding:10px}.evidence-img{display:block;width:100%;height:auto;border-radius:7px;border:1px solid #dce2e7}.evidence-item figcaption{margin-top:8px;color:#5b6874;font-size:12px;word-break:break-all}.ev{display:inline-block;margin:8px 8px 0 0;padding:7px 9px;border-radius:7px;background:#edf4fc;color:#205f9e;font-size:12px}.missing{background:#fff1f0;color:#b42318}@media(max-width:720px){.summary{grid-template-columns:1fr 1fr}.top,.head{display:block}}"
    doc = (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        f'<title>{sid} — Checks</title><style>{css}</style></head><body><main class="wrap">'
        f'<section class="hero"><div class="top"><div><div class="cid">HOT TEST AUTOMATION</div><h1>{sid}</h1><p>{html.escape(cfg["name"])}</p></div><span class="status {tc}">CASO: {test_status}</span></div>'
        f'<div class="summary"><div><small>Checks planejados</small><strong>{total}</strong></div><div><small>Checks aprovados</small><strong>{counts["PASS"]}</strong></div><div><small>Checks falhos</small><strong>{counts["FAIL"]}</strong></div><div><small>Não executados</small><strong>{counts["NÃO EXECUTADO"]}</strong></div></div></section>'
        + "".join(items) +
        '</main></body></html>'
    )
    out.write_text(doc, encoding="utf-8")

def render_consolidated(results):
    total_cases = len(CHECKS)
    passed_cases = sum(1 for sid in CHECKS if results[sid][0] == "PASS")
    failed_cases = sum(1 for sid in CHECKS if results[sid][0] == "FAIL")
    total_checks = sum(len(CHECKS[sid]["checks"]) for sid in CHECKS)
    passed_checks = sum(results[sid][2]["PASS"] for sid in CHECKS)
    failed_checks = sum(results[sid][2]["FAIL"] for sid in CHECKS)
    notrun_checks = sum(results[sid][2]["NÃO EXECUTADO"] for sid in CHECKS)

    cards = []
    for sid, cfg in CHECKS.items():
        test_status, rows, counts = results[sid]
        cls = "pass" if test_status == "PASS" else "fail" if test_status == "FAIL" else "neutral"
        cards.append(
            '<section class="card">'
            f'<div class="head"><div><div class="sid">{sid}</div><h2>{html.escape(cfg["name"])}</h2></div><span class="status {cls}">{test_status}</span></div>'
            f'<div class="stats"><div><small>Checks aprovados</small><strong>{counts["PASS"]}/{len(rows)}</strong></div><div><small>Checks falhos</small><strong>{counts["FAIL"]}</strong></div><div><small>Não executados</small><strong>{counts["NÃO EXECUTADO"]}</strong></div></div>'
            f'<a class="btn" href="evidencias/{sid}/relatorio_cenario.html">Abrir caso + checks + evidências</a>'
            '</section>'
        )

    overall = "PASS" if passed_cases == total_cases and passed_checks == total_checks else ("FAIL" if failed_cases or failed_checks else "PARCIAL")
    ocls = "pass" if overall == "PASS" else "fail" if overall == "FAIL" else "neutral"
    css = "*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#18212b;font-family:Arial,sans-serif}.wrap{max-width:1180px;margin:auto;padding:30px}.hero,.card{background:#fff;border:1px solid #dce2e7;border-radius:14px;margin-bottom:18px}.hero,.card{padding:24px}.top,.head{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.kicker,.sid{font-size:12px;font-weight:800;color:#2767ad;letter-spacing:.05em}.status{padding:9px 14px;border-radius:999px;color:white;font-weight:800}.pass{background:#16834b}.fail{background:#b42318}.neutral{background:#66737f}.summary{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:22px}.summary div,.stats div{background:#f7f9fb;border-radius:9px;padding:13px}.summary small,.stats small{display:block;color:#66737f;font-weight:700;margin-bottom:5px}.card h2{margin:5px 0}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:18px 0}.btn{display:inline-block;text-decoration:none;background:#2164aa;color:white;font-weight:700;padding:11px 15px;border-radius:8px}.note{margin-top:18px;padding:14px;border-radius:9px;background:#fff8e6;color:#674d00;font-size:13px;line-height:1.5}@media(max-width:800px){.summary{grid-template-columns:1fr 1fr}.stats{grid-template-columns:1fr}.top,.head{display:block}}"
    doc = (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Relatório Consolidado HOT</title>'
        f'<style>{css}</style></head><body><main class="wrap">'
        f'<section class="hero"><div class="top"><div><div class="kicker">HOT TEST AUTOMATION</div><h1>Relatório Consolidado</h1><p>Casos de teste, checks de negócio e evidências da execução.</p></div><span class="status {ocls}">{overall}</span></div>'
        f'<div class="summary"><div><small>Casos de teste</small><strong>{total_cases}</strong></div><div><small>Casos aprovados</small><strong>{passed_cases}</strong></div><div><small>Casos falhos</small><strong>{failed_cases}</strong></div><div><small>Checks planejados</small><strong>{total_checks}</strong></div><div><small>Checks aprovados</small><strong>{passed_checks}</strong></div><div><small>Falhos / não executados</small><strong>{failed_checks} / {notrun_checks}</strong></div></div>'
        '<div class="note"><b>Regra do relatório:</b> um check só aparece como PASS quando o keyword correspondente foi realmente executado com sucesso no output.xml. Evidência visual fica associada ao check, mas screenshot sozinha não é contada como validação aprovada.</div></section>'
        + "".join(cards) +
        f'<footer style="color:#66737f;font-size:12px;text-align:center">Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</footer></main></body></html>'
    )
    CONSOLIDATED.write_text(doc, encoding="utf-8")

def main():
    tests = load_tests()
    results = {}
    for sid, cfg in CHECKS.items():
        test_status, rows, counts = scenario_result(sid, cfg, tests)
        results[sid] = (test_status, rows, counts)
        render_scenario(sid, cfg, test_status, rows, counts)
    render_consolidated(results)
    print("Relatórios com checks gerados.")
    print("Casos:", len(CHECKS))
    print("Checks planejados:", sum(len(v["checks"]) for v in CHECKS.values()))
    print("Consolidado:", CONSOLIDATED)

if __name__ == "__main__":
    main()
