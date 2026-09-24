from pathlib import Path
import html,re,xml.etree.ElementTree as ET
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2]; EVID=ROOT/"reports"/"evidencias"/"HOT-INV-DEF-003"; XML=ROOT/"reports"/"output.xml"; OUT=EVID/"relatorio_cenario.html"
SID="HOT-INV-DEF-003"; NAME="Defeito Fora da Garantia + Reparo Aprovado"
STEPS=[
("01","Nota Fiscal","Selecionar Nota Fiscal existente com Tipo preenchido automaticamente e Salvar.","EM CADASTRO — Equipamento Funcional.",["02_nota_fiscal_salva.png"]),
("02","Localização","Preencher localização do equipamento e Salvar.","EM CADASTRO — Equipamento Funcional.",["03_localizacao_salva.png"]),
("03","Configurações","Preencher configurações válidas e Salvar.","Inclusão dos Ativos disponível.",["04_configuracoes_salvas.png"]),
("04","Inclusão do Ativo","Preencher Armário, Número do Ativo e Serial; Adicionar; validar Detalhes; Salvar.","Ativo cadastrado.",["05_campos_ativo_preenchidos.png","06_apos_clicar_adicionar.png","07_detalhes_ativo_abertos.png","08_ativo_incluido_e_salvo.png"]),
("05","Buscar e Abrir Ativo","Pesquisar pelo mesmo Serial e abrir o ativo.","EM ESTOQUE — Equipamento Funcional.",["09_lista_antes_pesquisa_serial.png","10_pesquisa_pelo_serial_preenchida.png","11_resultado_encontrado_pelo_serial.png","12_ativo_localizado_e_aberto.png","13_ativo_em_estoque_funcional.png"]),
("06","Regra — Não preencher Funcionário","Não preencher funcionário. Mais Opções > Ações.","Painel de Ações exibido.",["14_mais_opcoes_aberto.png","15_painel_acoes_aberto.png"]),
("07","Defeito","Alterar status para DEFEITO e preencher Chamado HITSS, Laudo HITSS, Tipo de Defeito e Comentário; Salvar.","DEFEITO — Equipamento com Defeito.",["16_defeito_preenchido_antes_salvar.png","17_status_defeito.png"]),
("08","Dados de Manutenção","Preencher Fornecedor, Chamado Fornecedor e Laudo Fornecedor.","Dados de manutenção preenchidos.",["18_dados_manutencao_preenchidos.png"]),
("09","Fora da Garantia + Reparo Aprovado","Selecionar Garantia = NÃO. Anexar 'Orcamento fora da garantia.pdf'. Após o upload, selecionar Reparo aprovado = SIM. Preencher Número do Pedido e Remessa do Reparo com 10 caracteres alfanuméricos randômicos. Salvar.","AGUARDANDO REPARO — Equipamento com Defeito.",["19_fora_da_garantia_orcamento_exibido.png","20_orcamento_anexado_reparo_aprovado_exibido.png","21_reparo_aprovado_campos_pedido_remessa_exibidos.png","22_pedido_e_remessa_preenchidos_antes_salvar.png","22_status_aguardando_reparo.png"]),
("10","Retorno ao Estoque","Mais Opções > Ações > EM ESTOQUE; comentário 'Ativo disponível para uso.'; Salvar.","EM ESTOQUE — Equipamento Funcional.",["23_mais_opcoes_final_aberto.png","24_painel_acoes_final_aberto.png","25_retorno_estoque_preenchido_antes_salvar.png","26_status_final_em_estoque_funcional.png","99_teste_finalizado_com_sucesso.png"])]
def status():
 try:
  root=ET.parse(XML).getroot()
  for t in root.findall(".//test"):
   if SID in t.get("name",""):
    s=t.find("status")
    if s is not None:return s.get("status","SEM RESULTADO")
 except:pass
 return "SEM RESULTADO"
def data():
 vals={"Serial":"-","Número do Ativo":"-","Número do Pedido":"-","Remessa do Reparo":"-"}
 if XML.exists():
  x=XML.read_text(encoding="utf-8",errors="ignore")
  pats={"Serial":r"Serial gerado para toda a execução:\s*([^<\r\n]+)","Número do Ativo":r"Número do ativo gerado para toda a execução:\s*([^<\r\n]+)","Número do Pedido":r"Número do pedido gerado para toda a execução:\s*([^<\r\n]+)"}
  for k,p in pats.items():
   m=re.search(p,x)
   if m:vals[k]=html.unescape(m.group(1)).strip()
 return vals
def image(n):
 if not(EVID/n).exists():return '<div class="missing">Evidência não encontrada: '+html.escape(n)+'</div>'
 return '<figure><a href="'+html.escape(n)+'"><img src="'+html.escape(n)+'"></a><figcaption>'+html.escape(n)+'</figcaption></figure>'
def main():
 EVID.mkdir(parents=True,exist_ok=True); st=status(); d=data(); cards=[]
 for n,title,act,exp,imgs in STEPS:
  cards.append(f'<section class="step"><header><span>{n}</span><h2>{html.escape(title)}</h2></header><div class="spec"><div><b>Ação</b><p>{html.escape(act)}</p></div><div><b>Resultado esperado</b><p>{html.escape(exp)}</p></div></div><h3>Evidências</h3>{"".join(image(i) for i in imgs)}</section>')
 cls="pass" if st=="PASS" else "fail" if st=="FAIL" else "neutral"
 css="*{box-sizing:border-box}body{margin:0;background:#f3f5f7;font-family:Arial;color:#18212b}.wrap{max-width:1400px;margin:auto;padding:28px}.hero,.step{background:white;border:1px solid #dce2e7;border-radius:14px;margin-bottom:18px;overflow:hidden}.hero{padding:26px}.top{display:flex;justify-content:space-between}.status{padding:10px 16px;border-radius:999px;color:white;font-weight:bold;height:max-content}.pass{background:#16834b}.fail{background:#b42318}.neutral{background:#66737f}.meta{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:18px}.meta div,.spec div{background:#f7f9fb;padding:13px;border-radius:9px}.meta small{display:block;color:#66737f}.step header{display:flex;gap:14px;align-items:center;padding:18px 20px;border-bottom:1px solid #e2e6ea}.step header span{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;background:#edf4fc;color:#2164aa;font-weight:bold}.spec{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:20px}.step h3{padding:0 20px;color:#66737f;font-size:13px}figure{padding:10px 20px;margin:0}img{display:block;max-width:100%;max-height:850px;margin:auto;border:1px solid #ddd;border-radius:8px}figcaption{font-size:11px;color:#73808c}.missing{margin:10px 20px;padding:12px;background:#fff1f0}"
 doc=f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{SID}</title><style>{css}</style></head><body><main class="wrap"><section class="hero"><div class="top"><div><h1>{SID}</h1><p>{NAME}</p></div><div class="status {cls}">{st}</div></div><div class="meta"><div><small>Serial</small>{html.escape(d["Serial"])}</div><div><small>Número do Ativo</small>{html.escape(d["Número do Ativo"])}</div><div><small>Número do Pedido</small>{html.escape(d["Número do Pedido"])}</div><div><small>Remessa do Reparo</small>{html.escape(d["Remessa do Reparo"])}</div><div><small>Gerado em</small>{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div></div></section>{"".join(cards)}</main></body></html>'
 OUT.write_text(doc,encoding="utf-8");print("Relatório gerado:",OUT)
if __name__=="__main__":main()
