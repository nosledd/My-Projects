# Deploy Fieldwork Certificate Generator on Vercel

This deployment is deliberately separate from the local-first automation app.
It provides only the deterministic certificate generator; it does not run
Gemma, Ollama, invoice extraction, chat, OCR, or the local job queue.

## Limits

- The PDF template and XLSX upload together must be below 4 MB.
- The generated ZIP must be below 4 MB.
- Files are sent once for preview and again only after explicit approval.
- Vercel functions do not retain uploads, pending previews, or outputs.

## Deploy

1. Push the repository changes to GitHub.
2. Sign in at https://vercel.com with GitHub and import `nosledd/My-Projects`.
3. Set **Root Directory** to `fieldwork`.
4. Leave the build command and output directory at their detected defaults.
5. Deploy.

The public URL is the Vercel project URL.  Test it with a small certificate
template and spreadsheet before sharing it.  This version has no accounts or
access controls, so do not use it with confidential documents.
