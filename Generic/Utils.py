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

def _safe_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]+', '_', str(name)).strip()

def _exportar_pdf_pessoa(pessoa, dfs_por_atv, start_date, end_date, pasta_out=".\\exported_data"):
    os.makedirs(pasta_out, exist_ok=True)
    arq = os.path.join(pasta_out, f"{_safe_filename(pessoa.nome)}.pdf")

    doc = SimpleDocTemplate(
        arq,
        pagesize=landscape(A4),
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.2*cm
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
    story.extend([titulo, Spacer(1, 0.25*cm), info, Spacer(1, 0.6*cm)])

    # Tabelas: um df abaixo do outro
    for i, df in enumerate(dfs_por_atv, 1):
        atv_nome = None
        if "TACOES_DES" in df.columns and not df.empty:
            atv_nome = str(df["TACOES_DES"].iloc[0])
        cab = Paragraph(f"<b>{i}. {atv_nome or 'Atividade'}</b>", styles["Heading2"])
        story.extend([cab, Spacer(1, 0.15*cm)])

        # Prepara dados (formata datas, remove NaN)
        df_fmt = df.copy()
        for col in df_fmt.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
            df_fmt[col] = df_fmt[col].dt.strftime("%d/%m/%Y %H:%M")
        df_fmt = df_fmt.fillna("")

        data = [list(df_fmt.columns)] + df_fmt.astype(str).values.tolist()

        # Larguras: divide igualmente a largura disponível
        # (simples e robusto; se quiser, ajuste por conteúdo)
        num_cols = len(df_fmt.columns)
        avail_width = landscape(A4)[0] - (doc.leftMargin + doc.rightMargin)
        col_widths = [avail_width / max(1, num_cols)] * num_cols

        tbl = Table(data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]))
        story.extend([tbl, Spacer(1, 0.5*cm)])

    doc.build(story)
    return arq