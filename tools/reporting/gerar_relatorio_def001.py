from pathlib import Path
import html, re
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT=Path(__file__).resolve().parents[2]
EVID=ROOT/"reports"/"evidencias"/"HOT-INV-DEF-001"
XML=ROOT/"reports"/"output.xml"
OUT=EVID/"relatorio_cenario.html"
SCENARIO="HOT-INV-DEF-001"
NAME="Defeito Dentro da Garantia e Sem Peça"

STEPS=[
("01","Nota Fiscal","Abrir Nota Fiscal, selecionar uma Nota Fiscal existente cujo Tipo já esteja preenchido automaticamente pelo sistema e clicar em Salvar.","Status: EM CADASTRO — Equipamento Funcional. Localização do Equipamento e Documentos exibidos. Botões Voltar, Salvar e Excluir disponíveis.",["02_nota_fiscal_salva.png"]),
("02","Localização do Equipamento","Abrir Localização do Equipamento. Selecionar Origem: Rio de Janeiro; informar Localização Atual do Ativo: Rio de Janeiro; selecionar Estado: Rio de Janeiro; clicar em Salvar.","Status permanece EM CADASTRO — Equipamento Funcional. Configurações do Equipamento é exibido.",["03_localizacao_salva.png"]),
("03","Configurações do Equipamento","Preencher Tipo de Equipamento, Imagem, Fabricante, Modelo, Processador, Geração do Processador, Memória, Tipo de Armazenamento e Capacidade de Armazenamento com opções válidas e clicar em Salvar.","Status permanece EM CADASTRO — Equipamento Funcional. Inclusão dos Ativos e Detalhes dos Números de Ativo/Serial ficam disponíveis.",["04_configuracoes_salvas.png"]),
("04","Inclusão do Ativo","Preencher Armário, Número do Ativo e Serial. Clicar em Adicionar, abrir Detalhes dos Números de Ativo/Serial, validar os dados incluídos e clicar em Salvar.","Cadastro concluído e retorno à listagem do Controle de Inventário.",["05_campos_ativo_preenchidos.png","06_apos_clicar_adicionar.png","07_detalhes_ativo_abertos.png","08_ativo_incluido_e_salvo.png"]),
("05","Buscar e Abrir o Ativo Cadastrado","Pesquisar usando o mesmo Serial criado anteriormente, digitando-o no campo de pesquisa; localizar o ativo e abri-lo.","Ativo localizado e aberto com Status EM ESTOQUE — Equipamento Funcional.",["09_lista_antes_pesquisa_serial.png","10_pesquisa_pelo_serial_preenchida.png","11_resultado_encontrado_pelo_serial.png","12_ativo_localizado_e_aberto.png","13_ativo_em_estoque_funcional.png"]),
("06","Regra de Negócio — Não preencher Funcionário","Não preencher informações de funcionário. Abrir Mais Opções e clicar em Ações.","Painel de Ações exibido.",["14_mais_opcoes_aberto.png","15_painel_acoes_aberto.png"]),
("07","Alterar Status para DEFEITO","No campo Alterar Status Para, selecionar DEFEITO.","Chamado HITSS, Laudo HITSS, Tipo de Defeito e Comentário ficam disponíveis.",["15_painel_acoes_aberto.png"]),
("08","Preencher Dados do Defeito","Preencher Chamado HITSS, anexar Laudo HITSS, selecionar Tipo de Defeito, informar comentário e clicar em Salvar.","Status DEFEITO — Equipamento com Defeito. Dados de Manutenção exibidos.",["16_defeito_preenchido_antes_salvar.png","17_status_defeito.png"]),
("09","Dados de Manutenção","Preencher Fornecedor, Chamado Fornecedor e anexar Laudo Fornecedor.","Dados de manutenção preenchidos e campo Está dentro da garantia? disponível.",["18_dados_manutencao_preenchidos.png"]),
("10","Equipamento Dentro da Garantia","Selecionar SIM para Está dentro da garantia?.","Campo Tem peça? é exibido.",["19_garantia_informada_antes_salvar.png"]),
("11","Sem Peça — Aguardando Peça","Selecionar NÃO para Tem peça? e clicar em Salvar.","Status AGUARDANDO PEÇA — Equipamento com Defeito.",["20_status_aguardando_peca.png"]),
("12","Peça Disponível — Aguardando Reparo","Alterar Tem peça? para SIM e clicar em Salvar.","Status AGUARDANDO REPARO — Equipamento com Defeito.",["21_peca_disponivel_antes_salvar.png","22_status_aguardando_reparo.png"]),
("13","Retorno ao Estoque","Abrir Mais Opções > Ações. Selecionar EM ESTOQUE. Comentário: Ativo disponível para uso. Clicar em Salvar.","Status final EM ESTOQUE — Equipamento Funcional.",["23_mais_opcoes_final_aberto.png","24_painel_acoes_final_aberto.png","25_retorno_estoque_preenchido_antes_salvar.png","26_status_final_em_estoque_funcional.png","99_teste_finalizado_com_sucesso.png"])
]

def status():
    try:
        root=ET.parse(XML).getroot()
        for t in root.findall(".//test"):
            if SCENARIO in t.get("name",""):
                s=t.find("status")
                if s is not None:return s.get("status","SEM RESULTADO")
    except: pass
    return "SEM RESULTADO"

def dados():
    serial=ativo="-"
    if XML.exists():
        x=XML.read_text(encoding="utf-8",errors="ignore")
        m=re.search(r"Serial gerado para toda a execução:\s*([^<\r\n]+)",x)
        if m: serial=html.unescape(m.group(1)).strip()
        m=re.search(r"Número do ativo gerado para toda a execução:\s*([^<\r\n]+)",x)
        if m: ativo=html.unescape(m.group(1)).strip()
    return serial,ativo

def image(name):
    if not (EVID/name).exists():
        return '<div class="missing">Evidência não encontrada nesta execução: '+html.escape(name)+'</div>'
    return '<figure><a href="'+html.escape(name)+'" target="_blank"><img src="'+html.escape(name)+'"></a><figcaption>'+html.escape(name)+'</figcaption></figure>'

def main():
    EVID.mkdir(parents=True,exist_ok=True)
    st=status(); serial,ativo=dados()
    cards=[]
    for n,title,action,expected,imgs in STEPS:
        gallery="".join(image(x) for x in imgs)
        cards.append(f"""<section class="step"><header><span class="num">{n}</span><h2>{html.escape(title)}</h2></header>
<div class="spec"><div><b>Ação</b><p>{html.escape(action)}</p></div><div><b>Resultado esperado</b><p>{html.escape(expected)}</p></div></div>
<h3>Evidências da etapa</h3>{gallery}</section>""")
    css="""*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#18212b;font-family:Arial,sans-serif}.wrap{max-width:1400px;margin:auto;padding:28px}.hero,.step{background:#fff;border:1px solid #dce2e7;border-radius:14px;margin-bottom:18px;overflow:hidden}.hero{padding:26px}.top{display:flex;justify-content:space-between;gap:20px}.kicker{font-size:12px;font-weight:800;color:#2767ad}.status{padding:10px 16px;border-radius:999px;background:#16834b;color:#fff;font-weight:800;height:max-content}.meta{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:20px}.meta div{background:#f7f9fb;padding:12px;border-radius:9px}.meta small{display:block;color:#66737f;font-weight:700}.step header{display:flex;align-items:center;gap:14px;padding:18px 20px;border-bottom:1px solid #e2e6ea}.num{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;background:#edf4fc;color:#2164aa;font-weight:800}.spec{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:20px}.spec div{border:1px solid #e1e6eb;border-radius:10px;padding:14px}.spec p{line-height:1.5}.step h3{padding:0 20px;color:#66737f;font-size:13px;text-transform:uppercase}figure{margin:0;padding:10px 20px 20px}img{display:block;max-width:100%;max-height:850px;margin:auto;border:1px solid #dce2e7;border-radius:8px}figcaption{font-size:11px;color:#73808c;margin-top:6px}.missing{margin:10px 20px;padding:14px;background:#fff1f0;border:1px solid #f0c7c3;border-radius:8px}@media(max-width:800px){.meta,.spec{grid-template-columns:1fr}}"""
    doc=f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{SCENARIO}</title><style>{css}</style></head><body><main class="wrap">
<section class="hero"><div class="top"><div><div class="kicker">RELATÓRIO DE CENÁRIO + EVIDÊNCIAS</div><h1>{SCENARIO}</h1><p>{NAME}</p></div><div class="status">{html.escape(st)}</div></div>
<div class="meta"><div><small>Serial</small>{html.escape(serial)}</div><div><small>Número do Ativo</small>{html.escape(ativo)}</div><div><small>Etapas</small>{len(STEPS)}</div><div><small>Gerado em</small>{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</div></div></section>
{''.join(cards)}</main></body></html>"""
    OUT.write_text(doc,encoding="utf-8")
    print("Relatório gerado:",OUT)

if __name__=="__main__":main()
