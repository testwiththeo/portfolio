from pathlib import Path
from xml.sax.saxutils import escape
import zipfile

OUT_DIR = Path('public/docs')
OUT_DIR.mkdir(parents=True, exist_ok=True)

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

CONTENT_TYPES = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">
  <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>
  <Default Extension=\"xml\" ContentType=\"application/xml\"/>
  <Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>
  <Override PartName=\"/word/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/>
</Types>
""".strip()

ROOT_RELS = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">
  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>
</Relationships>
""".strip()

STYLES_XML = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<w:styles xmlns:w=\"{NS}\">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\"/>
        <w:sz w:val=\"22\"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>

  <w:style w:type=\"paragraph\" w:default=\"1\" w:styleId=\"Normal\">
    <w:name w:val=\"Normal\"/>
    <w:qFormat/>
  </w:style>

  <w:style w:type=\"paragraph\" w:styleId=\"Title\">t
    <w:name w:val=\"Title\"/>
    <w:basedOn w:val=\"Normal\"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after=\"220\"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val=\"40\"/>
    </w:rPr>
  </w:style>

  <w:style w:type=\"paragraph\" w:styleId=\"Heading1\">
    <w:name w:val=\"heading 1\"/>
    <w:basedOn w:val=\"Normal\"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before=\"180\" w:after=\"120\"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val=\"30\"/>
    </w:rPr>
  </w:style>

  <w:style w:type=\"paragraph\" w:styleId=\"Heading2\">
    <w:name w:val=\"heading 2\"/>
    <w:basedOn w:val=\"Normal\"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before=\"120\" w:after=\"80\"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val=\"24\"/>
    </w:rPr>
  </w:style>
</w:styles>
""".strip()


def p(text: str = "", style: str | None = None, bold: bool = False) -> str:
    if text == "":
        return "<w:p/>"
    style_xml = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    bold_xml = "<w:b/>" if bold else ""
    return (
        f"<w:p>{style_xml}<w:r><w:rPr>{bold_xml}</w:rPr>"
        f"<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r></w:p>"
    )


def bullet(text: str) -> str:
    return p(f"- {text}")


def table(rows: list[list[str]], header: bool = True) -> str:
    tr_xml = []
    for r_i, row in enumerate(rows):
        cells = []
        for cell in row:
            cell_text = escape(cell)
            if header and r_i == 0:
                cell_para = (
                    "<w:p><w:r><w:rPr><w:b/></w:rPr>"
                    f"<w:t xml:space=\"preserve\">{cell_text}</w:t></w:r></w:p>"
                )
            else:
                cell_para = f"<w:p><w:r><w:t xml:space=\"preserve\">{cell_text}</w:t></w:r></w:p>"
            cells.append(
                "<w:tc><w:tcPr><w:tcW w:w=\"0\" w:type=\"auto\"/></w:tcPr>"
                f"{cell_para}</w:tc>"
            )
        tr_xml.append(f"<w:tr>{''.join(cells)}</w:tr>")

    return (
        "<w:tbl>"
        "<w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"auto\"/>"
        "<w:left w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"auto\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"auto\"/>"
        "<w:right w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"auto\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"auto\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"auto\"/>"
        "</w:tblBorders></w:tblPr>"
        f"{''.join(tr_xml)}"
        "</w:tbl>"
    )


def document(parts: list[str]) -> str:
    body = "".join(parts)
    return f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<w:document xmlns:w=\"{NS}\">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w=\"12240\" w:h=\"15840\"/>
      <w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/>
      <w:cols w:space=\"708\"/>
      <w:docGrid w:linePitch=\"360\"/>
    </w:sectPr>
  </w:body>
</w:document>
""".strip()


def write_docx(filename: str, parts: list[str]) -> None:
    out = OUT_DIR / filename
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", ROOT_RELS)
        zf.writestr("word/styles.xml", STYLES_XML)
        zf.writestr("word/document.xml", document(parts))


def build_case_study() -> list[str]:
    parts: list[str] = []
    parts.append(p("QUALITY ASSURANCE CASE STUDY - SANITIZED DEMO", style="Title"))
    parts.append(p("Cross-Border Checkout Reliability", style="Heading1"))
    parts.append(table([
        ["Document Field", "Value"],
        ["Version", "1.0"],
        ["Prepared By", "Theodore - Software QA Engineer"],
        ["Date", "March 2026"],
        ["Classification", "Portfolio Sample (Sanitized)"],
    ]))

    parts.append(p("Executive Summary", style="Heading1"))
    parts.append(p("This case study documents a risk-driven QA strategy for a cross-border logistics checkout flow with payment callback dependencies and approval workflow complexity."))

    parts.append(p("Context", style="Heading1"))
    parts.append(bullet("Multi-currency checkout with dynamic conversion rules"))
    parts.append(bullet("Role-based approval before fulfillment"))
    parts.append(bullet("Cross-region API dependencies with retry behavior"))

    parts.append(p("Scope", style="Heading1"))
    parts.append(table([
        ["In Scope", "Out of Scope"],
        ["Checkout totals and conversion", "Marketing pages and CMS"],
        ["Approval workflow states", "Legacy archived orders"],
        ["Payment callback handling", "3rd party billing portal UI"],
    ]))

    parts.append(p("Risk Matrix", style="Heading1"))
    parts.append(table([
        ["Risk", "Likelihood", "Impact", "Mitigation"],
        ["Currency rounding mismatch", "Medium", "High", "Boundary-value matrix and DB assertion"],
        ["Approval race condition", "Medium", "High", "Concurrent-event scenario tests"],
        ["Callback retry inconsistency", "Low", "High", "Negative API tests and idempotency checks"],
    ]))

    parts.append(p("Test Strategy", style="Heading1"))
    parts.append(bullet("Risk-based prioritization for financial critical path"))
    parts.append(bullet("Matrix-driven test data for role, region, currency, and order state"))
    parts.append(bullet("API contract and negative testing for resilience"))
    parts.append(bullet("Release triage by severity, user impact, and rollback complexity"))

    parts.append(p("Key Findings", style="Heading1"))
    parts.append(table([
        ["Finding ID", "Severity", "Status", "Summary"],
        ["F-101", "Critical", "Resolved", "Rounding mismatch in two conversion scenarios"],
        ["F-104", "High", "Resolved", "Approval state race under callback concurrency"],
        ["F-109", "Medium", "Accepted", "Retry delay edge case under unstable network"],
    ]))

    parts.append(p("Impact and Release Recommendation", style="Heading1"))
    parts.append(bullet("Critical issues detected and resolved before production"))
    parts.append(bullet("Higher release confidence for checkout and approval flow"))
    parts.append(bullet("Recommendation: GO with monitoring guardrail for retry anomalies"))

    parts.append(p("Redaction Note", style="Heading1"))
    parts.append(p("All client names, internal IDs, endpoints, and personally identifiable data are masked for portfolio publication."))
    return parts


def build_automation_pack() -> list[str]:
    parts: list[str] = []
    parts.append(p("AUTOMATION TEST DEMO PACK - SANITIZED", style="Title"))
    parts.append(p("Regression Gate Automation", style="Heading1"))
    parts.append(table([
        ["Document Field", "Value"],
        ["Version", "1.0"],
        ["Owner", "Theodore - Automation QA"],
        ["Primary Stack", "Playwright, Newman, GitHub Actions"],
    ]))

    parts.append(p("Objective", style="Heading1"))
    parts.append(p("Reduce manual regression effort and improve release gate reliability through layered automation."))

    parts.append(p("Suite Inventory", style="Heading1"))
    parts.append(table([
        ["Suite", "Type", "Frequency", "Gate"],
        ["Critical Smoke", "UI + API", "Per Pull Request", "Blocking"],
        ["Regression Core", "UI End-to-End", "Nightly", "Non-blocking"],
        ["Contract Validation", "API", "Per Pull Request", "Blocking"],
    ]))

    parts.append(p("Pipeline Design", style="Heading1"))
    parts.append(bullet("PR stage: smoke plus contract checks with fast feedback"))
    parts.append(bullet("Nightly stage: broader regression to detect drift"))
    parts.append(bullet("Release stage: critical-path-only deterministic gate"))

    parts.append(p("Flaky Test Management", style="Heading1"))
    parts.append(bullet("Tag unstable tests and isolate from blocking gate"))
    parts.append(bullet("Track flaky rate weekly and assign remediation owner"))
    parts.append(bullet("Use retry only as diagnosis support, not as quality mask"))

    parts.append(p("Outcome Summary", style="Heading1"))
    parts.append(table([
        ["Area", "Before", "After"],
        ["Regression feedback speed", "Slow and manual", "Faster and repeatable"],
        ["Gate confidence", "Subjective", "Evidence-driven"],
        ["Failure traceability", "Scattered", "Linked to artifacts and logs"],
    ]))
    return parts


def build_issue_report_pack() -> list[str]:
    parts: list[str] = []
    parts.append(p("ISSUE REPORT SAMPLE PACK - SANITIZED", style="Title"))
    parts.append(p("Critical Defect Reporting Template and Example", style="Heading1"))

    parts.append(p("Template Fields", style="Heading1"))
    parts.append(table([
        ["Field", "Description"],
        ["Title", "Short impact-focused bug title"],
        ["Environment", "Build, browser/device, backend version"],
        ["Preconditions", "Required setup before execution"],
        ["Steps to Reproduce", "Deterministic actions with data reference"],
        ["Expected vs Actual", "Clear behavior difference"],
        ["Severity and Priority", "Impact classification and urgency"],
        ["Evidence", "Logs, screenshots, payload, recording"],
    ]))

    parts.append(p("Sample Defect", style="Heading1"))
    parts.append(p("Bug ID: BUG-QA-1042 | Severity: High | Priority: P1"))
    parts.append(p("Title: Approval status not updated after payment callback retry"))
    parts.append(p("Environment: Staging v2026.03.18 | payment-service v2.7.4 | order-service v3.2.1"))
    parts.append(p("Preconditions: User role Approver, pending approval order, callback retry simulation enabled"))

    parts.append(p("Reproduction Steps", style="Heading2"))
    parts.append(bullet("Create order with approved payment method"))
    parts.append(bullet("Trigger callback timeout and retry event"))
    parts.append(bullet("Refresh dashboard and order detail"))

    parts.append(p("Expected vs Actual", style="Heading2"))
    parts.append(table([
        ["Expected", "Actual"],
        ["Order and approval status remain synchronized", "Order is Paid while approval remains Pending"],
    ]))

    parts.append(p("Impact Statement", style="Heading2"))
    parts.append(p("Approver cannot finalize order on time, creating operational delay for fulfillment."))

    parts.append(p("Evidence Checklist", style="Heading2"))
    parts.append(bullet("Console log excerpt (sanitized)"))
    parts.append(bullet("API response snapshot with masked identifiers"))
    parts.append(bullet("Screen recording attached in ticket"))
    return parts


def build_signoff_pack() -> list[str]:
    parts: list[str] = []
    parts.append(p("JIRA RELEASE SIGN-OFF NOTE - SANITIZED", style="Title"))
    parts.append(p("Release Candidate RC-2026.03.22", style="Heading1"))
    parts.append(table([
        ["Field", "Value"],
        ["QA Owner", "Theodore"],
        ["Decision", "CONDITIONAL GO"],
        ["Scope", "Checkout, approval workflow, callback processing"],
        ["Date", "March 2026"],
    ]))

    parts.append(p("Validation Checklist", style="Heading1"))
    parts.append(table([
        ["Check Item", "Status", "Notes"],
        ["Critical path test execution", "Pass", "All blocking scenarios validated"],
        ["API contract validation", "Pass", "No breaking schema drift"],
        ["Known critical defects", "Pass", "None open"],
        ["Rollback readiness", "Pass", "Procedure reviewed with engineering"],
        ["Monitoring readiness", "Pass", "Alert thresholds configured"],
    ]))

    parts.append(p("Known Non-Blocking Issues", style="Heading1"))
    parts.append(bullet("Two medium UI alignment issues"))
    parts.append(bullet("One low-priority localization wording issue"))

    parts.append(p("Residual Risk and Mitigation", style="Heading1"))
    parts.append(p("Residual risk remains low-to-medium for rare retry sequences under unstable network conditions."))
    parts.append(bullet("Monitor callback error rate for first 24 hours"))
    parts.append(bullet("Trigger rollback checklist if threshold is exceeded"))

    parts.append(p("Final QA Recommendation", style="Heading1"))
    parts.append(p("GO with active monitoring guardrails and rollback readiness confirmed."))
    return parts


write_docx('qa-case-study-demo.docx', build_case_study())
write_docx('automation-tests-demo.docx', build_automation_pack())
write_docx('issue-report-samples-demo.docx', build_issue_report_pack())
write_docx('jira-release-signoff-demo.docx', build_signoff_pack())

print('Professional QA DOCX pack generated successfully.')
