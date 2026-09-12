# Deploy Fieldwork on Render

This configuration deploys the deterministic Certificate Generator beta. It
does not expose Gemma-powered automation, because Gemma must be hosted
separately before it can be safely used by public visitors.

1. Sign in to Render with the GitHub account that owns `nosledd/My-Projects`.
2. Select **New** -> **Blueprint** and choose `My-Projects`.
3. Render finds `render.yaml` and creates the `fieldwork` web service.
4. Review the service and click **Apply**.
5. Wait for the `/health` check to pass, then open the generated `onrender.com`
   URL on both a phone and a PC.

The service stores uploads and generated ZIPs only temporarily. They are
removed after 60 minutes by default. Do not use this beta for confidential
documents, and do not turn on `AUTOMATION_ENABLE_GEMMA` until a separate,
secured model service is available.
