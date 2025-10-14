import os
import re
from typing import Optional, Tuple
from PyPDF2 import PdfReader
import win32com.client

class EmailGen:
    EMAIL_LINE_RE = re.compile(r"Email\s*:\s*(.+)", re.IGNORECASE)
    # e-mails (bem permissivo)
    EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
    # Período: dd/mm/aaaa a dd/mm/aaaa  (aceita 'a', '-', '–', 'até')
    PERIODO_RE = re.compile(
        r"Per[ií]odo\s*:\s*(\d{2}/\d{2}/\d{4})\s*(?:a|até|-|–)\s*(\d{2}/\d{2}/\d{4})",
        re.IGNORECASE,
    )
    NOME_RE = re.compile(r"Nome\s*:\s*(.+)", re.IGNORECASE)

    def __init__(self, subject_template: str | None = None, body_template: str | None = None):
        # Placeholders: {nome}, {periodo_inicio}, {periodo_fim}
        self.subject_template = subject_template or "Relatório de Produção - {nome} ({periodo_inicio} a {periodo_fim})"
        self.body_template = body_template or (
            "Bom dia,\n\n"
            "Segue em anexo, para conferência, o relatório de produção referente ao período de {periodo_inicio} a {periodo_fim}.\n"
            "Qualquer dúvida fico à disposição.\n\n"
        )

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        texts = []
        for page in reader.pages:
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            texts.append(t)
        return "\n".join(texts)

    def _parse_email(self, text: str) -> Optional[str]:
        m = self.EMAIL_LINE_RE.search(text)
        if m:
            candidate_line = m.group(1).splitlines()[0].strip()
            m2 = self.EMAIL_RE.search(candidate_line)
            if m2:
                return m2.group(0)
        m = self.EMAIL_RE.search(text)
        return m.group(0) if m else None

    def _parse_periodo(self, text: str) -> Optional[Tuple[str, str]]:
        m = self.PERIODO_RE.search(text)
        if not m:
            return None
        return m.group(1), m.group(2)

    def _parse_nome(self, text: str) -> Optional[str]:
        m = self.NOME_RE.search(text)
        if not m:
            return None
        return m.group(1).splitlines()[0].strip()

    def _create_outlook_mail(self, to_addr: str, subject: str, body: str, attachment_path: str):
        app = win32com.client.Dispatch("Outlook.Application")
        mail = app.CreateItem(0)
        if to_addr is None:
            to_addr = ''
        mail.To = to_addr
        mail.Subject = subject
        mail.Cc = "amilton.amaral@zenyprojetosoeste.com.br"
        mail.Body = body
        # Anexa o PDF
        mail.Attachments.Add(Source=os.path.abspath(attachment_path))
        # Apenas exibir (não enviar)
        mail.Display(False)
        return mail

    def process_folder(self, folder_path: str, recursive: bool = False, verbose: bool = True) -> None:
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Pasta não encontrada: {folder_path}")

        pdf_paths = []
        if recursive:
            for root, _, files in os.walk(folder_path):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        pdf_paths.append(os.path.join(root, f))
        else:
            for f in os.listdir(folder_path):
                if f.lower().endswith(".pdf"):
                    pdf_paths.append(os.path.join(folder_path, f))

        if verbose:
            print(f"Encontrados {len(pdf_paths)} PDF(s) em '{folder_path}'.")

        for pdf in pdf_paths:
            try:
                text = self._extract_text_from_pdf(pdf)
                email = self._parse_email(text)
                periodo = self._parse_periodo(text)
                nome = self._parse_nome(text) or "Colaborador"

                inicio, fim = periodo
                subject = self.subject_template.format(
                    nome=nome, periodo_inicio=inicio, periodo_fim=fim
                )
                body = self.body_template.format(
                    nome=nome, periodo_inicio=inicio, periodo_fim=fim
                )

                self._create_outlook_mail(email, subject, body, pdf)

                if verbose:
                    print(f"[OK] Email criado para {email} com anexo '{os.path.basename(pdf)}'")

            except Exception as e:
                if verbose:
                    print(f"[ERRO] {os.path.basename(pdf)} -> {e}")