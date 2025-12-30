# 🛡️ Gatekeeper System Specification

> **Status:** Active  
> **Component:** AI Classifier / Pre-inference Check  
> **Safety Level:** Critical

---

## 1. Purpose
The **Gatekeeper** is a lightweight AI classifier that verifies whether an uploaded medical image matches the user-selected anatomical category (**brain**, **chest**, **bone**) before specialist analysis.

---

## 2. Input Contract `[MANDATORY]`
*The system must enforce these exact expectations before inference.*

### 📁 File Requirements
| Parameter | Specification |
| :--- | :--- |
| **Accepted Types** | `.png`, `.jpg` |
| **Color Format** | RGB only (3 channels) |

### 🖼️ Image Processing
* **Input Size:** Any size accepted at input.
* **Internal Resize:** Must be resized to **224×224**.
* **Value Range:** Normalized using **ImageNet statistics**.

> 🛑 **Constraint:** Any image that does not meet these requirements must be rejected by the backend before inference.

---

## 3. Class Definitions `[LOCKED FOREVER]`
*Strict mapping rules. These indices must never change.*

| Index ID | Label String |
| :---: | :--- |
| `0` | **brain** |
| `1` | **chest** |
| `2` | **bone** |

**Hardware Rules:**
1.  These string labels must be used in backend JSON.
2.  Any change requires **retraining** + **version bump**.

---

## 4. Output Contract
*The exact JSON structure for inference output.*

```json
{
  "detected_part": "brain | chest | bone",
  "confidence": 0.985
}
Notes:

Confidence: Softmax probability.

Range: 0.0 – 1.0.

Visibility: Backend may display or log confidence.

5. Mismatch Logic [CRITICAL SAFETY RULE]
Behavior: If the detected anatomical class does not match the user-selected class, the system must halt analysis immediately.

Canonical Error Response:

JSON

{
  "status": "error",
  "source": "gatekeeper",
  "user_selected": "brain",
  "detected_part": "chest",
  "message": "Mismatch: you selected brain, but the image looks like chest."
}
Clarification: > The Gatekeeper never overrides the user.

The Gatekeeper only blocks unsafe routing.