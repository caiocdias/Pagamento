import os, re
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm

def read_float(prompt: str, min_=None, max_=None):
    while True:
        s = input(prompt).strip().replace(',', '.')
        try:
            x = float(s)
        except ValueError:
            print("Valor inválido. Tente de novo (ex.: 12.34 ou 12,34).")
            continue

        if min_ is not None and x < min_:
            print(f"O valor deve ser ≥ {min_}.")
            continue
        if max_ is not None and x > max_:
            print(f"O valor deve ser ≤ {max_}.")
            continue
        return x

def _fmt_brl(v):
    if pd.isna(v):
        return ""
    try:
        v = float(v)
    except Exception:
        return str(v)
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    sign = "-" if v < 0 else ""
    return f"{sign}R$ {s}"


def _safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]+', '_', str(name)).strip()

def _exportar_pdf_pessoa(pessoa, dfs_por_atv, start_date, end_date, pasta_out=".\\exported_data"):
    os.makedirs(pasta_out, exist_ok=True)
    arq = os.path.join(pasta_out, f"{_safe_filename(pessoa.nome)}.pdf")

    doc = SimpleDocTemplate(
        arq,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.5 * cm, bottomMargin=1.2 * cm
    )
    styles = getSampleStyleSheet()
    story = []

    # Cabeçalho
    titulo = Paragraph("<b>Relatório de Produção</b>", styles["Title"])
    periodo = f"{start_date:%d/%m/%Y} a {end_date:%d/%m/%Y}"
    info = Paragraph(
        f"<b>Nome:</b> {pessoa.nome}<br/>"
        f"<b>Email:</b> {pessoa.email}<br/>"
        f"<b>Chave Pix:</b> {pessoa.chave_pix}<br/>"
        f"<b>Período:</b> {periodo}<br/>"
        f"<b>Atividades exportadas:</b> {len(dfs_por_atv)}",
        styles["Normal"]
    )
    story.extend([titulo, Spacer(1, 0.25 * cm), info, Spacer(1, 0.6 * cm)])

    # Tabelas: um df abaixo do outro
    for i, df in enumerate(dfs_por_atv, 1):
        # Título da atividade
        atv_nome = None
        if "Ação" in df.columns and not df.empty:
            atv_nome = str(df["Ação"].iloc[0])
        cab = Paragraph(f"<b>{i}. {atv_nome or 'Atividade'}</b>", styles["Heading2"])
        story.extend([cab, Spacer(1, 0.15 * cm)])

        # Subtítulo: Redução/Comparação vindos de df.attrs
        redu = [x for x in (df.attrs.get("reduzir") or []) if x]
        comp = [x for x in (df.attrs.get("comparar") or []) if x]

        # pega valor/unidade
        vu = df.attrs.get("valor_unidade", None)
        unid = (df.attrs.get("unidade_pagamento") or "").upper()
        rotulo = "Valor unitário"
        if unid == "US":
            rotulo = "Valor por US"
        elif unid == "NS":
            rotulo = "Valor por NS"

        linha_valor = f"<b>{rotulo}:</b> {_fmt_brl(vu) if vu is not None else ''}"

        if redu or comp:
            linhas = []
            if redu:
                linhas.append(f"<b>Redução:</b> {', '.join(map(str, redu))}")
            if comp:
                linhas.append(f"<b>Comparação:</b> {', '.join(map(str, comp))}")
            # valor vem logo abaixo
            linhas.append(linha_valor)
            sub = Paragraph("<br/>".join(linhas), styles["Italic"])
            story.extend([sub, Spacer(1, 0.15 * cm)])
        else:
            # se não houver redução/comparação, exibe só o valor
            sub = Paragraph(linha_valor, styles["Italic"])
            story.extend([sub, Spacer(1, 0.15 * cm)])

        # Total monetário ANTES de formatar para string
        total_val = pd.to_numeric(df.get("Valor a Pagar"), errors="coerce").fillna(0).sum()

        # ----- Preparação de dados para a tabela -----
        df_fmt = df.copy()

        # 1) "Conclusão" só com data
        if "Conclusão" in df_fmt.columns:
            df_fmt["Conclusão"] = pd.to_datetime(df_fmt["Conclusão"], errors="coerce").dt.strftime("%d/%m/%Y")

        # 1.1) "Ação" como Paragraph para quebrar linhas (sem converter para str depois!)
        if "Ação" in df_fmt.columns:
            df_fmt["Ação"] = df_fmt["Ação"].apply(lambda x: Paragraph(str(x), styles["Normal"]))

        # 2) US, Redução, Comparação com 2 casas
        for col in ["US", "Redução", "Comparação"]:
            if col in df_fmt.columns:
                df_fmt[col] = pd.to_numeric(df_fmt[col], errors="coerce") \
                    .map(lambda v: "" if pd.isna(v) else f"{v:.2f}")

        # 2.1) Valor a Pagar em R$ (formato BRL)
        if "Valor a Pagar" in df_fmt.columns:
            df_fmt["Valor a Pagar"] = pd.to_numeric(df_fmt["Valor a Pagar"], errors="coerce").map(_fmt_brl)

        # 3) Outras datetimes (se houver) ficam com data+hora
        dt_cols = [c for c in df_fmt.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns
                   if c != "Conclusão"]
        for c in dt_cols:
            df_fmt[c] = df_fmt[c].dt.strftime("%d/%m/%Y %H:%M")

        # 4) Monta a matriz SEM converter Paragraph para string
        df_fmt = df_fmt.fillna("")

        header = list(df_fmt.columns)
        rows = []
        for _, row in df_fmt.iterrows():
            cells = []
            for cell in row:
                # Mantém Paragraph como está; demais converte para string
                if isinstance(cell, Paragraph):
                    cells.append(cell)
                else:
                    cells.append("" if pd.isna(cell) else str(cell))
            rows.append(cells)

        data = [header] + rows

        num_cols = len(header)
        avail_width = landscape(A4)[0] - (doc.leftMargin + doc.rightMargin)

        # Larguras: por padrão, divide igualmente
        col_widths = [avail_width / max(1, num_cols)] * num_cols

        # Dá ~35% da largura para "Ação" e divide o resto
        if "Ação" in header and num_cols > 1:
            j_acao = header.index("Ação")
            acao_w = avail_width * 0.35
            other_w = (avail_width - acao_w) / (num_cols - 1)
            col_widths = [other_w] * num_cols
            col_widths[j_acao] = acao_w

        # Adiciona linha de TOTAL ao data
        if "Valor a Pagar" in header:
            j_val = header.index("Valor a Pagar")
            total_row = [""] * num_cols
            total_row[j_val] = _fmt_brl(total_val)
            if j_val - 1 >= 0:
                total_row[j_val - 1] = "Total"
            data.append(total_row)

        tbl = Table(data, colWidths=col_widths, repeatRows=1)

        # Estilos
        table_style = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]

        # Alinhar à direita colunas numéricas/moeda
        for nome_col in ["US", "Redução", "Comparação", "Valor a Pagar"]:
            if nome_col in header:
                j = header.index(nome_col)
                table_style.append(("ALIGN", (j, 1), (j, -1), "RIGHT"))

        # Destacar a linha do TOTAL
        last_row = len(data) - 1
        if "Valor a Pagar" in header and last_row >= 1:
            table_style += [
                ("FONTNAME", (0, last_row), (-1, last_row), "Helvetica-Bold"),
                ("LINEABOVE", (0, last_row), (-1, last_row), 0.5, colors.black),
            ]

        tbl.setStyle(TableStyle(table_style))
        story.extend([tbl, Spacer(1, 0.5 * cm)])

    doc.build(story)
    return arq

def _unir_dfs_para_excel(dfs_por_atv: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Une a lista de dataframes de atividades em um único DF padronizado para Excel,
    garantindo mesmas colunas e tipos (datas/números).
    """
    prefer = ["NS", "Serviço", "Ação", "Conclusão", "US", "Redução", "Comparação", "Valor a Pagar"]

    # União de colunas presentes
    allcols = set()
    for d in dfs_por_atv:
        allcols.update(d.columns)

    # Ordem final: preferidas primeiro, depois extras
    cols_final = [c for c in prefer if c in allcols] + [c for c in allcols if c not in prefer]

    dfs_norm = []
    for d in dfs_por_atv:
        dd = d.copy()
        # adiciona colunas faltantes
        for c in cols_final:
            if c not in dd.columns:
                dd[c] = pd.NA
        dd = dd[cols_final]
        dfs_norm.append(dd)

    out = pd.concat(dfs_norm, ignore_index=True)

    # Tipos: numéricos + data
    for c in ["US", "Redução", "Comparação", "Valor a Pagar"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    if "Conclusão" in out.columns:
        out["Conclusão"] = pd.to_datetime(out["Conclusão"], errors="coerce")

    return out


def _safe_sheetname(name: str, used: set[str]) -> str:
    """
    Ajusta o nome da planilha para o Excel (<=31 chars, sem caracteres inválidos e único).
    """
    s = re.sub(r'[\[\]\*\?/\\:]', '_', str(name))[:31] or "Sheet"
    base = s
    i = 1
    while s in used:
        suffix = f"_{i}"
        s = (base[:31 - len(suffix)] + suffix) if len(base) + len(suffix) > 31 else base + suffix
        i += 1
    used.add(s)
    return s


def _exportar_xlsx(planilhas: dict, start_date, end_date, pasta_out=".\\exported_data") -> str:
    """
    Cria um único .xlsx em pasta_out, com uma aba por pessoa (key do dict).
    Cada aba contém todas as atividades (linhas) daquela pessoa.
    """
    os.makedirs(pasta_out, exist_ok=True)
    nome_arq = f"Relatorio_Gmax_{start_date:%Y-%m-%d}_a_{end_date:%Y-%m-%d}.xlsx"
    caminho = os.path.join(pasta_out, nome_arq)

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:
        wb = writer.book
        header_fmt = wb.add_format({"bold": True, "bg_color": "#D9D9D9", "border": 1})
        num2_fmt   = wb.add_format({"num_format": "#,##0.00", "align": "right"})
        money_fmt  = wb.add_format({"num_format": 'R$ #,##0.00', "align": "right"})
        date_fmt   = wb.add_format({"num_format": "dd/mm/yyyy"})
        wrap_fmt   = wb.add_format({"text_wrap": True})
        bold_fmt   = wb.add_format({"bold": True})
        money_bold = wb.add_format({"num_format": 'R$ #,##0.00', "bold": True})

        used_names = set()

        from xlsxwriter.utility import xl_col_to_name

        for pessoa_nome, dfp in planilhas.items():
            # escreve a aba
            sheet = _safe_sheetname(pessoa_nome, used_names)
            dfp.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]

            # formatos por coluna (se existirem)
            cols = list(dfp.columns)
            col_idx = {c: i for i, c in enumerate(cols)}

            # cabeçalho
            ws.set_row(0, None, header_fmt)
            ws.freeze_panes(1, 0)
            ws.autofilter(0, 0, len(dfp), len(cols) - 1)

            # larguras e formatos
            if "Ação" in col_idx:
                j = col_idx["Ação"]
                ws.set_column(j, j, 40, wrap_fmt)
            if "Serviço" in col_idx:
                ws.set_column(col_idx["Serviço"], col_idx["Serviço"], 12)
            if "NS" in col_idx:
                ws.set_column(col_idx["NS"], col_idx["NS"], 16)
            if "Conclusão" in col_idx:
                j = col_idx["Conclusão"]
                ws.set_column(j, j, 12, date_fmt)
            for c in ["US", "Redução", "Comparação"]:
                if c in col_idx:
                    ws.set_column(col_idx[c], col_idx[c], 12, num2_fmt)
            if "Valor a Pagar" in col_idx:
                j = col_idx["Valor a Pagar"]
                ws.set_column(j, j, 16, money_fmt)

                # total na última linha (visível e dinâmico com filtro)
                last = len(dfp) + 1  # 1-based (cabeçalho = linha 1)
                col_letter = xl_col_to_name(j)
                ws.write(last, max(0, j - 1), "Total", bold_fmt)
                ws.write_formula(last, j, f"=SUBTOTAL(9,{col_letter}2:{col_letter}{last})", money_bold)

        # metadados (opcional)
        wb.set_properties({
            "title":   f"Relatório de Produção ({start_date:%d/%m/%Y} a {end_date:%d/%m/%Y})",
            "author":  "Relatório Gmax",
            "subject": "Produção consolidada por pessoa"
        })

    return caminho