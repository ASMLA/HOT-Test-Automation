from pathlib import Path
from datetime import datetime
import html
import re

STEP_META = {
    "01_controle_inventario_aberto": ("Acesso ao Controle de Inventário", "Tela de Controle de Inventário aberta e disponível para iniciar o cenário."),
    "02_nota_fiscal_salva": ("Preenchimento da Nota Fiscal", "Nota Fiscal selecionada com Tipo da Nota Fiscal já preenchido pelo sistema e cadastro salvo."),
    "03_localizacao_salva": ("Preenchimento da Localização", "Origem, localização atual do ativo e estado preenchidos e salvos."),
    "04_configuracoes_salvas": ("Configuração do Equipamento", "Configurações obrigatórias do equipamento preenchidas e salvas."),
    "05_campos_ativo_preenchidos": ("Inclusão do Ativo — Dados preenchidos", "Armário, Número do Ativo e Serial preenchidos antes da inclusão."),
    "06_apos_clicar_adicionar": ("Inclusão do Ativo — Adicionar", "Ação Adicionar executada para inserir o ativo na lista."),
    "07_detalhes_ativo_abertos": ("Inclusão do Ativo — Validação dos Detalhes", "Detalhes abertos para validar o mesmo Número do Ativo e Serial gerados para a execução."),
    "08_ativo_incluido_e_salvo": ("Inclusão do Ativo — Cadastro salvo", "Ativo incluído e cadastro salvo com sucesso."),
    "09_lista_antes_pesquisa_serial": ("Pesquisa do Ativo — Lista inicial", "Lista de inventário disponível antes de pesquisar o serial criado."),
    "10_pesquisa_pelo_serial_preenchida": ("Pesquisa do Ativo — Serial digitado", "O mesmo serial criado no cenário foi digitado caractere a caractere na pesquisa."),
    "11_resultado_encontrado_pelo_serial": ("Pesquisa do Ativo — Resultado localizado", "Ativo correspondente ao serial e número gerados foi localizado."),
    "12_ativo_localizado_e_aberto": ("Abertura do Ativo", "Ativo localizado foi aberto para continuidade do fluxo."),
    "13_ativo_em_estoque_funcional": ("Status Inicial do Ativo", "Ativo validado como EM ESTOQUE e Equipamento Funcional."),
    "14_mais_opcoes_aberto": ("Declaração de Defeito — Mais Opções", "Menu Mais Opções aberto sem associação prévia de funcionário."),
    "15_painel_acoes_aberto": ("Declaração de Defeito — Ações", "Painel de Ações aberto para alteração do status."),
    "16_defeito_preenchido_antes_salvar": ("Declaração de Defeito — Dados preenchidos", "Status DEFEITO, Chamado HITSS, Laudo HITSS, tipo de defeito e comentário preenchidos antes de salvar."),
    "17_status_defeito": ("Validação — Status DEFEITO", "Status validado como DEFEITO e Equipamento com Defeito."),
    "18_dados_manutencao_preenchidos": ("Dados de Manutenção", "Fornecedor, Chamado Fornecedor e Laudo Fornecedor preenchidos."),
    "19_garantia_informada_antes_salvar": ("Garantia — Dentro da garantia", "Equipamento marcado como dentro da garantia antes de salvar."),
    "20_status_aguardando_peca": ("Validação — AGUARDANDO PEÇA", "Status validado como AGUARDANDO PEÇA e Equipamento com Defeito."),
    "21_peca_disponivel_antes_salvar": ("Peça disponível", "Campo Tem peça? alterado para Sim antes de salvar."),
    "22_status_aguardando_reparo": ("Validação — AGUARDANDO REPARO", "Status validado como AGUARDANDO REPARO e Equipamento com Defeito."),
    "23_mais_opcoes_final_aberto": ("Retorno ao Estoque — Mais Opções", "Menu Mais Opções aberto para encerramento do fluxo."),
    "24_painel_acoes_final_aberto": ("Retorno ao Estoque — Ações", "Painel de Ações aberto para retorno ao estoque."),
    "25_retorno_estoque_preenchido_antes_salvar": ("Retorno ao Estoque — Dados preenchidos", "Status EM ESTOQUE e comentário final preenchidos antes de salvar."),
    "26_status_final_em_estoque_funcional": ("Validação Final", "Status final validado como EM ESTOQUE e Equipamento Funcional."),
    "99_teste_finalizado_com_sucesso": ("Resultado Final da Execução", "Cenário finalizado com sucesso."),
    "99_erro_estado_final": ("Estado Final no Momento da Falha", "Tela preservada no ponto em que a execução falhou."),
}

def _sort_key(path: Path):
    m = re.match(r"(\d+)_", path.stem)
    return (int(m.group(1)) if m else 9999, path.stem)

def gerar_relatorio_evidencias(evidence_dir, scenario_id, scenario_name, status, serial="", numero_ativo=""):
    evidence_dir = Path(str(evidence_dir))
    evidence_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(evidence_dir.glob("*.png"), key=_sort_key)

    status_upper = str(status).upper()
    status_class = "pass" if status_upper == "PASS" else "fail"
    status_text = "PASSOU" if status_upper == "PASS" else "FALHOU"

    rows = []
    for img in files:
        title, expected = STEP_META.get(
            img.stem,
            (img.stem.replace("_", " ").title(), "Evidência registrada durante a execução.")
        )
        m = re.match(r"(\d+)_", img.stem)
        number = m.group(1) if m else "--"
        rows.append(f"""
        <section class="step">
          <div class="step-head">
            <div class="step-number">{html.escape(number)}</div>
            <div class="step-title-wrap">
              <h2>{html.escape(title)}</h2>
              <p>{html.escape(expected)}</p>
            </div>
            <div class="evidence-badge">EVIDÊNCIA {html.escape(number)}</div>
          </div>
          <div class="image-wrap">
            <a href="{html.escape(img.name)}" target="_blank">
              <img src="{html.escape(img.name)}" alt="{html.escape(title)}">
            </a>
          </div>
          <div class="file-name">{html.escape(img.name)}</div>
        </section>
        """)

    generated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html_doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(str(scenario_id))} - Relatório de Evidências</title>
<style>
:root {{
  --bg:#f4f6f8; --card:#fff; --text:#17212b; --muted:#65717c;
  --border:#dfe5ea; --pass:#147a42; --fail:#b42318; --accent:#1f5fae;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:Arial,Helvetica,sans-serif;line-height:1.45}}
.container{{max-width:1280px;margin:0 auto;padding:28px}}
.hero{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px;margin-bottom:22px}}
.hero-top{{display:flex;gap:20px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}}
.kicker{{font-size:12px;font-weight:700;letter-spacing:.12em;color:var(--accent);text-transform:uppercase}}
h1{{margin:6px 0 8px;font-size:30px}}
.subtitle{{color:var(--muted);margin:0}}
.status{{padding:10px 16px;border-radius:999px;color:white;font-weight:700}}
.status.pass{{background:var(--pass)}} .status.fail{{background:var(--fail)}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:22px}}
.meta-item{{background:#f8fafb;border:1px solid var(--border);border-radius:10px;padding:12px}}
.meta-label{{font-size:11px;color:var(--muted);text-transform:uppercase;font-weight:700}}
.meta-value{{margin-top:4px;font-weight:700;word-break:break-word}}
.summary{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 24px;margin-bottom:22px}}
.summary strong{{font-size:20px}}
.step{{background:var(--card);border:1px solid var(--border);border-radius:14px;margin:0 0 18px;overflow:hidden}}
.step-head{{display:grid;grid-template-columns:64px 1fr auto;gap:16px;align-items:center;padding:18px 20px;border-bottom:1px solid var(--border)}}
.step-number{{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#edf4fc;color:var(--accent);font-size:20px;font-weight:800}}
.step h2{{margin:0 0 5px;font-size:19px}}
.step p{{margin:0;color:var(--muted)}}
.evidence-badge{{font-size:11px;font-weight:800;letter-spacing:.06em;padding:7px 9px;border-radius:7px;background:#eef2f5;color:#52606d;white-space:nowrap}}
.image-wrap{{padding:18px;background:#fafbfc;text-align:center}}
.image-wrap img{{max-width:100%;max-height:780px;border:1px solid var(--border);border-radius:8px;box-shadow:0 3px 12px rgba(0,0,0,.08)}}
.file-name{{padding:9px 18px 13px;color:var(--muted);font-size:12px}}
.footer{{text-align:center;color:var(--muted);font-size:12px;padding:12px 0 30px}}
@media(max-width:720px){{.container{{padding:12px}}.step-head{{grid-template-columns:52px 1fr}}.evidence-badge{{grid-column:2}}}}
@media print{{body{{background:#fff}}.container{{max-width:none;padding:0}}.step,.hero,.summary{{break-inside:avoid;box-shadow:none}}}}
</style>
</head>
<body>
<div class="container">
  <header class="hero">
    <div class="hero-top">
      <div>
        <div class="kicker">Relatório Executivo de Teste + Evidências</div>
        <h1>{html.escape(str(scenario_id))}</h1>
        <p class="subtitle">{html.escape(str(scenario_name))}</p>
      </div>
      <div class="status {status_class}">{html.escape(status_text)}</div>
    </div>
    <div class="meta">
      <div class="meta-item"><div class="meta-label">Cenário</div><div class="meta-value">{html.escape(str(scenario_id))}</div></div>
      <div class="meta-item"><div class="meta-label">Serial</div><div class="meta-value">{html.escape(str(serial or "-"))}</div></div>
      <div class="meta-item"><div class="meta-label">Número do Ativo</div><div class="meta-value">{html.escape(str(numero_ativo or "-"))}</div></div>
      <div class="meta-item"><div class="meta-label">Gerado em</div><div class="meta-value">{html.escape(generated)}</div></div>
    </div>
  </header>

  <div class="summary">
    <strong>{len(files)} evidências registradas</strong><br>
    <span style="color:var(--muted)">Cada etapa abaixo apresenta a ação/validação de negócio e a respectiva evidência visual da mesma execução.</span>
  </div>

  {''.join(rows)}

  <div class="footer">HOT Test Automation • Relatório gerado automaticamente ao final da execução.</div>
</div>
</body>
</html>"""

    output = evidence_dir / "relatorio_evidencias.html"
    output.write_text(html_doc, encoding="utf-8")
    return str(output)
