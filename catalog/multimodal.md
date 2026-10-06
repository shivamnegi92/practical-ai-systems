# Multimodal application tools

> Build applications that handle images, audio, video, and interactive media.

[← Back to Practical AI Systems](../README.md)

## Catalog

Records are metadata-reviewed, not blanket endorsements.

| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |
|---|---|---|---|---|---|---|
| [Gradio](https://github.com/gradio-app/gradio) | Build interactive Python interfaces and demos for machine-learning applications. | quick model demos; human-in-the-loop prototypes | Production authentication, isolation, and scaling need separate engineering decisions. | framework | Apache-2.0 | metadata-reviewed |
| [OpenCV](https://github.com/opencv/opencv) | Computer-vision and image/video processing primitives for application pipelines. | image preprocessing; classical vision and video utilities | Core primitives need application-specific logic, tests, and review of optional modules. | library | Apache-2.0 | metadata-reviewed |
| [Streamlit](https://github.com/streamlit/streamlit) | Create interactive data and AI applications in Python with a compact development workflow. | data-facing prototypes; internal tools and interactive demos | Complex multi-user products may need a more conventional web architecture. | framework | Apache-2.0 | metadata-reviewed |

## Choosing well

Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.
