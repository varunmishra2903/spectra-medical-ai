\# Gatekeeper Model Specification



\## Input

\- Accepted formats: .png, .jpg, .dcm

\- Preprocessed size: 224 x 224 pixels (RGB)

\- Normalization: ImageNet mean/std



\## Classes

Exact label strings:

\- "brain"

\- "chest"

\- "bone"



\## Output

JSON structure:

\- `detected\_part` (string: "brain" | "chest" | "bone")

\- `confidence` (float, 0.0 – 1.0)



\## Constraints

\- Max model size: 30–50 MB

\- Target latency: < 0.5 s per image on CPU



\## Mismatch Logic

If `user\_selected != detected\_part`:



Return error JSON:

```json

{

&nbsp; "status": "error",

&nbsp; "source": "gatekeeper",

&nbsp; "user\_selected": "<brain|chest|bone>",

&nbsp; "detected\_part": "<brain|chest|bone>",

&nbsp; "message": "Mismatch: you selected <user\_selected>, but the image looks like <detected\_part>."

}



