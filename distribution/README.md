# Reusable conversation kit

This kit adapts three existing worksheets for print and supplies French translations. It is for adult couples and contains no list of sexual activities. The explicit Yes/No/Maybe inventories elsewhere in this repository are not included.

## Files

- [English printable kit](couples-conversation-kit-en.pdf)
- [French printable kit](couples-conversation-kit-fr.pdf)
- Editable sources: [English](kit.en.json), [French](kit.fr.json)

You may copy, adapt and redistribute these resources under the repository's [MIT License](../LICENSE). Keep the original copyright and full license notice. A link to the source project is welcome; a promotional backlink is not an extra condition of the MIT License. Do not imply professional endorsement or a partnership without agreement.

No email address or account is needed to use these static files. No worksheet answers are transmitted by the PDFs. They are conversation prompts, not therapy, a diagnosis or an instruction to carry out an activity.

## Source material

- [Couple intimacy check-in](../worksheets/couple-intimacy-check-in.md)
- [Desire alignment](../worksheets/desire-alignment.md)
- [Before talking about desire](../worksheets/before-talking-about-desire.md)

The English edition lightly adapts headings for print. The French edition translates the same questions. Both add a short introduction and retain the full original license. These are paper worksheets; they do not reproduce the app's server-side matching or confidentiality behavior.

## Rebuild

Install ReportLab, then run python3 scripts/build_distribution_pdfs.py. The script uses Arial on macOS or DejaVu Sans on Linux; set PDF_FONT_REGULAR and PDF_FONT_BOLD to select other TTF fonts. Inspect every rendered page after changing the JSON sources.

## Publisher blurb

English: Three free worksheets to help adult couples prepare a conversation, notice how intimacy feels, and explore what Maybe means. Write privately, share what you choose, and go at your own pace. Printable and reusable under the MIT License.

Français : Trois feuilles gratuites pour préparer une conversation, faire le point sur votre intimité et préciser ce que signifie « Peut-être ». Écrivez pour vous, partagez ce que vous choisissez et avancez à votre rythme. Imprimables et réutilisables sous licence MIT.
